import MapReduce
import sys

"""
Matrix Multiplication in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

K = 5
L = 5


def mapper(record):
    matrix = record[0]
    row = record[1]
    column = record[2]
    value = record[3]
    # first row of first matrix times first column of second matrix (dot prod)
    # result row 1 column 1 comes from A row 1 and B column 1
    # result row 1 column 2 comes from A row 1 and B column 2
    # etc
    if matrix == 'a':
        for k in xrange(K):
            mr.emit_intermediate((row, k), (matrix, column, value))
    elif matrix == 'b':
        for el in xrange(L):
            mr.emit_intermediate((el, column), (matrix, row, value))
    else:
        raise ValueError("there is no '{}' matrix".format(matrix))


def reducer(key, values):
    # initialize matrices to 0s (b/c input is sparse)
    A = [0] * 5
    B = [0] * 5
    dot_product = 0
    for value in values:  # update the appropriate matrix with a value
        if value[0] == 'a':
            A[value[1]] = value[2]
        elif value[0] == 'b':
            B[value[1]] = value[2]
        else:
            raise ValueError("there is no '{}' matrix".format(value[0]))
    for a, b in zip(A, B):
        dot_product += a * b

    i, j = key[0], key[1]
    mr.emit((i, j, dot_product))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
