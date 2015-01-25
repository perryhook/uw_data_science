import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(friend_pair):
    sorted_pair = sorted(friend_pair)
    key = (sorted_pair[0], sorted_pair[1])
    # key is the people in the pair and we
    # emit the origin_friend in that pair.
    origin_friend = friend_pair[0]
    mr.emit_intermediate(key, origin_friend)


def reducer(pair_key, origin_friends):
    # if both are in the pair_key, it's
    # still symmetric
    for friend in pair_key:
        if friend not in origin_friends:
            mr.emit((pair_key[0], pair_key[1]))
            mr.emit((pair_key[1], pair_key[0]))
            break

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
