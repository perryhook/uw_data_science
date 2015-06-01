import sys


def readlines_sorted(file_name):
    with open(file_name, 'rb') as f:
        lines = f.readlines()
    lines.sort()
    return lines


def print_different_lines(lines_1, lines_2):
    print "output is not the same"
    count = 0
    for i in xrange(len(lines_2)):
        print "{} - {}".format(lines_1[i], lines_2[i])
        count += 1
    print "\nleftovers are: "
    print lines_1[count:]


if __name__ == "__main__":
    file_1 = sys.argv[1]
    file_2 = sys.argv[2]

    lines_1 = readlines_sorted(file_1)
    lines_2 = readlines_sorted(file_2)

    left = len(lines_1) > len(lines_2)
    if lines_1 == lines_2:
        print "output is the same"
    elif left:
        print_different_lines(lines_1, lines_2)
    else:
        print_different_lines(lines_2, lines_1)
