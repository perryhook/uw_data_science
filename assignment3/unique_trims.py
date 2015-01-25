import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    sequence = record[1]
    mr.emit_intermediate(sequence[0:2], sequence[:-10])


def reducer(key, values):
    # at least with the data provide, my without_set method
    # is a little faster 7/9 times, but that's not very
    # scientific
    def without_set(values):
        values.sort()  # forces duplicates to be adjacent
        mr.emit(values[0])  # the first one is never a duplicate
        for i in xrange(1, len(values)):  # loop over the records
            prev_seq = values[i-1]
            this_seq = values[i]
            if compare_one_by_one(prev_seq, this_seq):
                mr.emit(this_seq)

    def with_set(values):
        values.sort()
        no_dupes = set()
        for seq in values:
            no_dupes.add(seq)
        # print "{}: {}".format(key, values)
        for seq in no_dupes:
            mr.emit(seq)
    # import time
    # wo_start = time.clock()
    without_set(values)
    # wo_stop = time.clock()
    # wo_time = wo_stop - wo_start
    # print "w/o_set time: {}".format(wo_time)
    # w_start = time.clock()

    # with_set(values)
    # w_stop = time.clock()
    # w_time = w_stop - w_start
    # print "with_set time: {}".format(w_time)

    # wo_faster = wo_time < w_time
    # equal = wo_time == w_time
    # if equal:
    #     print "same time"
    # elif wo_faster:
    #     print "w/o set was faster"
    # else:
    #     print "with set was faster"


def compare_one_by_one(prev_seq, this_seq):
    '''
    returns true if this_seq is different than prev_seq
    '''
    length = len(prev_seq)
    if length == len(this_seq):  # if equal lengths, look harder
        for j in xrange(length):    # compare letter by letter
            if prev_seq[j] != this_seq[j]:  # if different
                return True
        return False
    else:  # else they're not equal length & must be different
        return True

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
