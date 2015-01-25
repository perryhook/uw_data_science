import sys


if __name__ == "__main__":
    file_1 = sys.argv[1]
    file_2 = sys.argv[2]

    with open(file_1, 'rb') as f:
        lines_1 = f.readlines()

    with open(file_2, 'rb') as f:
        lines_2 = f.readlines()

    lines_1.sort()
    lines_2.sort()

    left = len(lines_1) > len(lines_2)
    if lines_1 == lines_2:
        print "output is the same"
    elif left:
        print "output is not the same"
        count = 0
        for i in xrange(len(lines_2)):
            print "{} - {}".format(lines_1[i], lines_2[i])
            count += 1
        print "\nleftovers from lines_1 are: "
        print lines_1[count:]
    else:
        print "output is not the same"
        count = 0
        for i in xrange(len(lines_1)):
            print "{} - {}".format(lines_1[i], lines_2[i])
            count += 1
        print "\nleftovers from lines_2 are: "
        print lines_2[count:]
