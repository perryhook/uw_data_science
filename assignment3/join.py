import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    # table = record[0]
    order_id = record[1]
    # print "\nEmitting: {}:{}".format(order_id, (table, record[2:]))
    mr.emit_intermediate(order_id, record)


def reducer(order_id, records):
    # print "\nReducing order {}\n\tRecords: {}".format(order_id, records)
    order = records[0]
    for line_item in records[1:]:
        mr.emit(order + line_item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
