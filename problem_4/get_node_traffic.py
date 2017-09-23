#!/bin/python

def main():
    retf = "./schedule_1123.dat"
    fp = open(retf)
    line = fp.readline()

    traffic = {} 
    while line:
        tmp = line.split(" ")
        for elem in tmp:
            if elem[0] == 'J':
                traffic.setdefault(elem, 0)
                traffic[elem] += 1
        line = fp.readline()
    tmp = []
    for key in traffic:
        tmp.append([key, traffic[key]])
    tmp.sort(key=lambda elem: elem[1], reverse=True)
    for elem in tmp:
        print elem[0] + ' ' + str(elem[1])
    print "The top three heaviest nodes are: ", tmp[0][0], tmp[1][0], tmp[2][0]
        
    fp.close()

if __name__ == "__main__":
    main()
