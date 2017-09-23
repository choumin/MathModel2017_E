#!/bin/python

import numpy as np
import sys

def get_distance_matrix(fname):
    fp = open(fname)
    line = fp.readline()
    line = fp.readline()
    matrix = []
    while line:
        line = line.strip()
        points = line.split('\t')
        #print points
        array = [float(points[i]) for i in range(1, len(points))]
        matrix.append(array)
        line = fp.readline()

    fp.close()
    #print len(matrix), len(matrix[0])
    return matrix

def get_name_index():
    fp = open("./name_index.dat")
    line = fp.readline()
    name_index = {}
    i = 0
    index_name = []
    while line:
        name = line.strip()
        name_index[name] = i
        index_name.append(name)
        line = fp.readline()
        i += 1

    fp.close()

    return name_index, index_name
            
def get_point_link(fname):
    fp = open(fname)
    line = fp.readline()
    point_link = {}
    while line:
        line = line.strip()
        index = line.find(" ")
        name = line[0 : index]
        points = line[index + 1 : ].split(" ")
        if name not in point_link:
            point_link[name] = []
            point_link[name].append([name, '*'])
        #if name == "Z03":
        #    print point_link[name]
        for i in range(0, len(points)):
            tmp = points[i].find(",")
            pname = points[i][0 : tmp]
            load = points[i][tmp + 1 : ]
            #points[i] = pname

            if pname not in point_link.keys():
                point_link[pname] = []
                point_link[pname].append([pname, '*'])
                point_link[pname].append([name, load])
            else:
                #if name not in point_link[pname]:
                point_link[pname].append([name, load])

            point_link[name].append([pname, load])
        #if name == "D1":
            #print point_link
        #    print point_link['Z03']
        #    print point_link['J09']
        #    print point_link['J10']
        #    print point_link['J11']
        
        line = fp.readline()
        
    fp.close()
    #print point_link
    #print point_link['Z03']
    #print point_link['J09']
    #print point_link['J10']
    #print point_link['J11']
    return point_link

def get_time_matrix(v0, v1, fname, dis_matrix, point_link):
    fp = open(fname, 'w')
    TA = []
    name_index, index_name = get_name_index()
    for i in range(0, len(dis_matrix)):
        TA.append([])
        for j in range(0, len(dis_matrix[0])):
            if dis_matrix[i][j] == 1000000 or dis_matrix[i][j] == 0:
                TA[i].append(dis_matrix[i][j])
            else:
                #print dis_matrix[i][j], i, j
                name1 = index_name[i]
                name2 = index_name[j]
                #print name1, name2
                #print point_link[name1]
                ok = False
                
                for elem in point_link[name1]:
                    if elem[0] == name2:
                        #print elem
                        ok = True
                        break
                #exit()
                if ok == False:
                    print "error!"
                    #print name1, name2
                    #print point_link[name1]
                    exit()

                if elem[1] == "0":
                    TA[i].append(round(dis_matrix[i][j] / v0, 6))
                elif elem[1] == "1":
                    TA[i].append(round(dis_matrix[i][j] / v1, 6))
            fp.write(str(TA[i][j]))
            if j != len(dis_matrix[0]) - 1:
                fp.write(" ")
        fp.write("\n")

    fp.close()

def main():
    dis_matrix_file = './distance_matrix.dat'
    link_file = "./linkfile.dat"
    va0 = 45
    va1 = 70
    vb0 = 35
    vb1 = 60
    vc0 = 30
    vc1 = 50
    
    point_link = get_point_link(link_file)
    dis_matrix = get_distance_matrix(dis_matrix_file)
    get_time_matrix(va0, va1, "./TA.dat", dis_matrix, point_link)
    get_time_matrix(vb0, vb1, "./TB.dat", dis_matrix, point_link)
    get_time_matrix(vc0, vc1, "./TC.dat", dis_matrix, point_link)

    if len(sys.argv) > 1:
        print "Getting time matrixs done!"

if __name__ == "__main__":
    main()
