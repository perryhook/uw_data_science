import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(friend_pair):
    mr.emit_intermediate(friend_pair[0], 1)
    # remember you can emit more than one pair per record


def reducer(key, value):
    mr.emit((key, sum(value)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
