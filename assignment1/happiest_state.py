import sys
import json
import re
import requests
from pprint import pprint
import time


last_google_geo_time = None
state_codes = set(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                   'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                   'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                   'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                   'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
                   'DC', 'AS', 'GU', 'MP', 'PR', 'UM', 'VI'])


def update_google_geo_time():
    global last_google_geo_time
    last_google_geo_time = time.time()
    print "google geo API call at {}".format(last_google_geo_time)
    return last_google_geo_time


def get_sentiment_word_scores(sent_file):
    # build the dictionary of word scores
    word_scores = {}
#    highest_score = float("-inf")
#    highest_words = []
#    lowest_score = float("inf")
#    lowest_words = []
    with open(sent_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        word, score = line.split("\t")
        score = int(score)
        word_scores[word] = score
#        print "word: {}, score: {}".format(word, score)
        # TODO Could you create a decorator function to keep track of the
        # highest and lowest scoring words?
#        if score < lowest_score:
#            print "score < lowest_score"
#            lowest_score = score
#            lowest_words = [word]
#        elif score == lowest_score:
#            lowest_words.append(word)
#        elif score == highest_score:
#            highest_words.append(word)
#        elif score > highest_score:
#            highest_score = score
#            highest_words = [word]
#    print "highest score: {}".format(highest_score)
#    pprint(highest_words)
#    print "lowest score: {}".format(lowest_score)
#    pprint(lowest_words)
    return word_scores


def get_tweets(tweet_file, lang=u'en'):
    tweets = []
    with open(tweet_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        tweet = json.loads(line)
        tweet_text = tweet.get(u'text')
        if tweet_text is not None and tweet.get(u'lang') == lang:
            # pprint(tweet)
            tweet[u'text'] = tweet_text.encode('utf-8')
            tweets.append(tweet)
            # raw_input("\npress Enter\n")
    return tweets


def get_lowered_words(text):
    return re.findall(r"[\w']+", text.lower())


def score_tweet(word_scores, tweet):
    scored_words = word_scores.keys()  # get the scored words
    score = 0
    tweet_words = get_lowered_words(tweet[u'text'])
    for word in scored_words:
        count = tweet_words.count(word)
        if count > 0:
            score += word_scores[word] * count
    return score, tweet_words


def derive_sentiment(word_scores, tweets):
    new_word_scores = {}
    for tweet in tweets:
        # score the tweet and get the words from the tweet
        score, tweet_words = score_tweet(word_scores, tweet)
        set_tweet_words = set(tweet_words)
        for word in set_tweet_words:
            if word not in word_scores:
                if word not in new_word_scores:
                    new_word_scores[word] = [score]
                else:
                    new_word_scores.get(word).append(score)
    # do averaging
    new_word_scores, low_score, high_score = avg_word_scores(new_word_scores)
    # do normalizing
    new_word_scores = normalize_word_scores(
        new_word_scores,
        low_score,
        high_score)
    return new_word_scores


def print_score_dict(score_dict):
    for key in sorted(score_dict.keys(), reverse=True):
        value = score_dict.get(key)
        summed = sum(value)
        avg = float(sum(value)) / len(value)
        entry = "state: {},\nsum: {},\navg: {},\nraw values:{}\n\n"
        print entry.format(key, summed, avg, value)


def avg_word_scores(word_scores):
    low_score = float("inf")
    # low_word = ''
    high_score = float("-inf")
    # high_word = ''
    for word, score_list in word_scores.iteritems():
        avg_score = float(sum(score_list)) / len(score_list)
        word_scores[word] = avg_score
        if avg_score < low_score:
            low_score = avg_score
            # low_word = word
        if avg_score > high_score:
            high_score = avg_score
            # high_word = word
    #     print "{} {}".format(word, avg_score)
    # low_msg = "lowest tweet word: {} {}"
    # high_msg = "highest tweet word: {} {}"
    # print low_msg.format(low_word, low_score)
    # print high_msg.format(high_word, high_score)
    return word_scores, low_score, high_score


def normalize_word_scores(word_scores, low_score, high_score):
    neg_scaler = -5. / low_score
    pos_scaler = 5. / high_score
    zeros = []
    for word, score in word_scores.iteritems():
        if score < 0:
            new_score = int(round(neg_scaler * score))
            if new_score == 0:
                zeros.append(word)
            word_scores[word] = new_score
        elif score > 0:
            new_score = int(round(pos_scaler * score))
            if new_score == 0:
                zeros.append(word)
            word_scores[word] = new_score
        else:
            zeros.append(word)
    for word in zeros:
        word_scores.pop(word)
    return word_scores


def get_term_freq(tweets):
    word_freqs = {}
    total_words = 0
    for tweet in tweets:
        tweet_words = get_lowered_words(tweet[u'text'])
        for word in tweet_words:
            total_words += 1
            count = word_freqs.get(word)
            if count is not None:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    # max_word = ''
    # max_freq = 0
    for word, count in word_freqs.iteritems():
        freq = float(count) / total_words
        # if freq > max_freq:
        #     max_freq = freq
        #     max_word = word
        word_freqs[word] = freq
    # print "max word {} with freq: {}".format(max_word, max_freq)
    return word_freqs


def reverse_geo_state(lat, lng):
    call_delay = 0.25  # got over limit errors when set to 0.20
    last_time = last_google_geo_time
    state_code = None
    if last_google_geo_time is None:
        update_google_geo_time()
    else:
        time_dif = update_google_geo_time() - last_time
        print "time_dif is: {}".format(time_dif)
        if time_dif < call_delay:
            print 'sleeping for {}'.format(call_delay - time_dif)
            time.sleep(call_delay - time_dif)

    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}'
    resp = requests.get(url.format(lat, lng))
    if resp.status_code == 200:
        resp_dict = json.loads(resp.text)
        # pprint(resp_dict)
        # raw_input("\nPress Enter\n")
    else:
        print "\n BAD RESPONSE {}\n".format(resp.status_code)
    try:
        addr_comps = resp_dict[u'results'][0][u'address_components']
    except IndexError:
        pprint(resp_dict)
        raise IndexError('Wat')
    for i in xrange(len(addr_comps)):
        if u'administrative_area_level_1' in addr_comps[i].get(u'types'):
            state_code = addr_comps[i].get(u'short_name')
            if state_code in state_codes:
                print "\nFOUND STATE: {}".format(state_code)
            else:
                state_code = None
    return state_code


def find_state(tweet):
    state = None
    coords = tweet.get(u'coordinates')
    geo = tweet.get(u'geo')

    # error checking
    if (geo is None and coords is not None) or (
            coords is None and geo is not None):
        print "Wat? geo is {} and coords is {}".format(geo, coords)
        raw_input("press Enter to continue")
    # if we have geo tag
    if geo is not None:
        lat = geo.get(u'coordinates')[0]
        lng = geo.get(u'coordinates')[1]
        state = reverse_geo_state(lat, lng)
    # pprint(tweet)
    # user = tweet.get(u'user')
    # user_location = user.get(u'location')
    # user_TZ = user.get(u'time_zone')
    # print "user->location: {}".format(user_location)
    # print "user->time zone: {}".format(user_TZ)
    # place = tweet.get(u'place')
    # place_full_name = place.get(u'full_name')
    # raw_input("\nplease press Enter\n")
    return state


def get_happiest_states(sent_file, tweets):
    word_scores = get_sentiment_word_scores(sent_file)
    state_scores = {}
    for tweet in tweets:
        state = find_state(tweet)
        if state is not None:
            score, _ = score_tweet(word_scores, tweet)
            state_score = state_scores.setdefault(state, {u'raw': []})
            state_score['raw'].append(score)

    for data in state_scores.values():
        summed = sum(data['raw'])
        data[u'sum'] = summed
        mean = float(summed) / len(data[u'raw'])
        data[u'mean'] = mean
    return state_scores


def hw(sent_file, tweet_file):
    tweets = get_tweets(tweet_file)
    happiest_states = get_happiest_states(sent_file, tweets)
    # print_score_dict(happiest_states)
    pprint(happiest_states)


def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    hw(sent_file, tweet_file)
    # lines(sent_file)
    # lines(tweet_file)

if __name__ == '__main__':
    main()
