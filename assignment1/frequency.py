import sys
import json
import re
# from pprint import pprint


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


def print_word_scores(word_scores):
    for word, score in word_scores.iteritems():
        print "{} {}".format(word, score)


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


def hw(sent_file, tweet_file):
    tweets = get_tweets(tweet_file)
    word_freqs = get_term_freq(tweets)
    print_word_scores(word_freqs)


def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    hw(sent_file, tweet_file)
    # lines(sent_file)
    # lines(tweet_file)

if __name__ == '__main__':
    main()
