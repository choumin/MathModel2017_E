#!/bin/python


def main():
    finc = "./increasing.dat"
    fp = open(finc)
    line = fp.readline()
    tmp = []
    while line:
        line = line.strip()
        tmp.append(line.split(" ")) 
        line = fp.readline()
    fp.close()

    #print tmp
    tmp.sort(key=lambda elem:float(elem[1]), reverse=True)
    #print ""
    #print tmp

    print "The top three fastest growing nodes are: ", tmp[0][0], tmp[1][0], tmp[2][0]

if __name__ == "__main__":
    main()
