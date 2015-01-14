import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    doc_id = record[0]
    text = record[1]
    words = text.split()
    for word in words:
        mr.emit_intermediate(word, doc_id)


def reducer(word, list_of_doc_ids):
    doc_id_set = set()
    for doc_id in list_of_doc_ids:
        doc_id_set.add(doc_id)
    mr.emit((word, list(doc_id_set)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
