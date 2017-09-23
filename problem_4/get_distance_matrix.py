#!/bin/python

import math
#import numpy as np
import sys

class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

def get_distance(p1, p2):
    tmp1 = abs(p1.x - p2.x)
    tmp2 = abs(p1.y - p2.y)
    return round(math.sqrt(tmp1 * tmp1 + tmp2 * tmp2), 2)

def get_name(line):
    index = line.find(" ")
    return line[0 : index]

def get_x(line):
    index = line.find(" ")
    while line[index] == " ":
        index += 1
    end = line.find(" ", index)
    return line[index : end]

def get_y(line):
    index = line.rfind(" ")
    return line[index + 1 : ]

def get_point_set(filename):
    fp = open(filename)
    line = fp.readline()
    point_set = []
    while line:
        name = get_name(line)
        x = get_x(line)
        y = get_y(line)
        point = Point(name, int(x), int(y))
        point_set.append(point) 
        line = fp.readline()   
    
    fp.close()
    return point_set

def get_point_set2(fname):
    fp = open(fname)
    point_set = []
    line = fp.readline()
    while line:
        line = line.strip()
        points = line.split(' ')
        for point in points:
            index = point.find(',')
            if index != -1:
                pname = point[0 : index]
            else:
                pname = point
            if pname not in point_set:
                point_set.append(pname)
        line = fp.readline()

    fp.close()
    return point_set

def get_point_link(linkfile):
    fp = open(linkfile)
    line = fp.readline()
    point_link = {}
    while line:
        line = line.strip()
        index = line.find(" ")
        name = line[0 : index]
        points = line[index + 1 : ].split(" ")
        for i in range(0, len(points)):
            tmp = points[i].find(",")
            points[i] = points[i][0 : tmp]
            if points[i] not in point_link:
                point_link[points[i]] = []
                point_link[points[i]].append(points[i])
                point_link[points[i]].append(name)
            else:
                if name not in point_link[points[i]]:
                    point_link[points[i]].append(name)
        
        point_link[name] = points 
        point_link[name].append(name)
        
        line = fp.readline()
    fp.close()
    return point_link

def get_point_set3(name_index):
    point_set = []
    fp = open(name_index)
    line = fp.readline()
    while line:
        point_set.append(line.strip())
        line = fp.readline()
    fp.close()

    return point_set

def main():
    coordfile = "./coordfile.dat"
    linkfile = "./linkfile.dat" 
    name_index = "./name_index.dat"
    point_set = get_point_set(coordfile)

    point_link = get_point_link(linkfile)
    infinite_max = 1000000
    
    s = ""
    for point in point_set:
        s += '\t' + point.name
    s += '\n'
    for point in point_set:
        s += point.name + '\t'
        for point2 in point_set:
            if point.name not in point_link or point2.name not in point_link:
                s += "1000000\t"
                continue
            if point2.name in point_link[point.name] or point.name in point_link[point2.name]:
                s += str(get_distance(point, point2)) + '\t'
            else:
                s += "1000000\t"
        s += '\n'
    fp = open("./distance_matrix.dat", 'w')
    fp.write(s)
    fp.close()

    if len(sys.argv) > 1:
        print "Getting distance matrix done!"

if __name__ == "__main__":
    main()
