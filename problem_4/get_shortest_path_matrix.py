#!/bin/python
#coding=utf-8

import sys
def floyd(graph):
    length = len(graph)
    path = {}

    for i in xrange(length):
        path.setdefault(i, {})
        for j in xrange(length):
            if i == j:
                continue

            path[i].setdefault(j, [i,j])
            new_node = None

            for k in xrange(length):
                if k == j:
                    continue
                #new_node = None

                new_len = graph[i][k] + graph[k][j]
                #if i == 2 and j == 1:
                #    print k, graph[i][j]
                if graph[i][j] > new_len:
                    graph[i][j] = new_len
                    graph[j][i] = new_len
                    new_node = k
            if new_node != None:
                #for p in path[i][k]:
                #    path[i][j].insert(-1, p)
                path[i][j].insert(-1, new_node)

    return graph, path

def floyd2(graph):
    length = len(graph)
    path = {}

    for k in range(length):
        for i in range(length):
            path.setdefault(i, {})
            for j in range(length):
                path[i].setdefault(j, [i,j])
                new_len = graph[i][k] + graph[k][j]
                if new_len < graph[i][j]:
                    graph[i][j] = new_len
                    #path[i][j] = []
                    #for elem in path[i][k]:
                    #    path[i][j].append(elem)
                    #for s in len(path[)
                    path[i][j] = path[i][k] + path[k][j][1 : ]
                    #path[i][j].insert(-1, k)

    return graph, path

def get_time_matrix(fname):
    matrix = []
    fp = open(fname)
    line = fp.readline()
    while line:
        line = line.strip()
        points = line.split(" ")
        array = [float(points[i]) for i in range(0, len(points))]
        matrix.append(array)
        line = fp.readline()

    fp.close()
    #print len(matrix), len(matrix[0])
    return matrix

def get_floyd_matrix(f1, f2, f3):
    matrix = get_time_matrix(f1)
    graph, path = floyd2(matrix)
    fp2 = open(f2, 'w') 
    fp3 = open(f3, 'w')
    for i in range(0, len(graph)):
        for j in range(0, len(graph[0])):
            #生成弗洛伊德矩阵
            fp2.write(str(graph[i][j]))
            #生成最短路径矩阵
            if j not in path[i]:
                fp3.write(str(j))
            else:
                sp = ""
                for k in range(0, len(path[i][j])):
                    sp += str(path[i][j][k])
                    if k != len(path[i][j]) - 1:
                        sp += ","
                fp3.write(sp)
                 
            if j != len(graph[0]) - 1:
                fp2.write(" ")
                fp3.write(" ")

        fp2.write("\n")
        fp3.write("\n")
        
    fp2.close()
    fp3.close()

def main():
    get_floyd_matrix("./TA.dat", "./FA.dat", "./SPA.dat")
    get_floyd_matrix("./TB.dat", "./FB.dat", "./SPB.dat")
    get_floyd_matrix("./TC.dat", "./FC.dat", "./SPC.dat")

    if len(sys.argv) > 1:
        print "Getting shortest path matrixs done!"
    
if __name__ == "__main__":
    main()
