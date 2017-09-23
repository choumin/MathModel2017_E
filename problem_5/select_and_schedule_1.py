#!/bin/python

#coding=utf-8

import sys

def get_floyd_matrix(fname):
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

def get_sites():
    fp = open("./name_index.dat")
    line = fp.readline()
    sites = []
    while line:
        name = line.strip()
        if name[0] == 'F':
            sites.append(name)
        line = fp.readline()

    fp.close()
    return sites

def get_nearest(matrix, name, sites):
    name_index, index_name = get_name_index()
    i = name_index[name]
    min_cost = 1000000
    min_site = ""
    for site in sites:
        j = name_index[site]
        if matrix[i][j] < min_cost:
            min_cost = matrix[i][j]
            min_site = site
    return min_site, min_cost

def get_spm(fname):
    spm = []
    fp = open(fname)
    line = fp.readline()
    while line:
        line = line.strip()
        spm.append(line.split(" "))
        line = fp.readline()
    fp.close()

    return spm

def get_time_matrix(fname):
    tm = []
    fp = open(fname)
    line = fp.readline()
    while line:
        line = line.strip()
        tm.append(line.split(" "))
        line = fp.readline()
    fp.close()

    return tm
    
def get_car_type(line):
    index = line.find(" ")
    return line[0 : index]

def get_cost(line):
    index = line.rfind(" ")
    return float(line[index + 1 : ])

def get_car_src(line):
    begin = line.find(" ")
    end = line.find(" ", begin + 1)
    return line[begin + 1 : end]

def get_car_dst(line):
    begin = line.find(" ")
    begin = line.find(" ", begin + 1)
    end = line.find(" ", begin + 1)
    return line[begin + 1 : end]

def get_shortest_path(spm, tm, src, dst):
    name_index, index_name = get_name_index()
    shortest_path = spm[name_index[src]][name_index[dst]]
    paths = shortest_path.split(",")
    pre_site = paths[0]
    sp = []
    for site in paths[1 : ]:
        sp.append([index_name[int(site)], float(tm[int(pre_site)][int(site)])])
        pre_site = site

    return sp
    
def schedule_method_1(select_file):
    fp = open(select_file)
    line = fp.readline()
    cars = []
    
    while line:
        line = line.strip()
        cars.append(line)
        line = fp.readline()
    fp.close()
    cars.reverse()
    last_begin = 0
    i = 0
    schedule_file = "./schedule_11.dat"
    fp = open(schedule_file, 'w')
    spa = get_spm("./SPA.dat")
    spb = get_spm("./SPB.dat")
    spc = get_spm("./SPC.dat")
    ta = get_time_matrix("./TA.dat")
    tb = get_time_matrix("./TB.dat")
    tc = get_time_matrix("./TC.dat")

    for car in cars:
        car_type = get_car_type(car)
        cost = get_cost(car)
        src = get_car_src(car)
        dst = get_car_dst(car)
        if i == 0:
            begin = 0
            i += 1
        else:
            begin = last_begin + (last_cost - cost)
        s = car_type + " " + src + " " + str(round(begin * 60, 1)) + " "
        if car_type[0] == 'A':
            shortest_path = get_shortest_path(spa, ta, src, dst)
        elif car_type[0] == 'B':
            shortest_path = get_shortest_path(spb, tb, src, dst)
        elif car_type[0] == 'C':
            shortest_path = get_shortest_path(spc, tc, src, dst)
        
        leave = begin
        for path in shortest_path:
            arrival = leave + path[1]
            leave = arrival
            s += path[0] + " " + str(round(arrival * 60, 1)) + " " + str(round(leave * 60, 1)) + " "
        fp.write(s + "\n")

        last_begin = begin
        last_cost = cost

    fp.close()

def select_method_1():
    FA = get_floyd_matrix("./FA.dat")
    FB = get_floyd_matrix("./FB.dat")
    FC = get_floyd_matrix("./FC.dat")
    sites = get_sites()
    count = 24
    flag = [0] * 6
    select_file = "./select_11.dat"
    fp = open(select_file, 'w')
    for i in range(count):
        choice = []
        if (flag[0] < 3):
            place, cost = get_nearest(FA, "D1", sites)
            choice.append([0, 'D1', 'A', flag[0], place, cost])
        if (flag[1] < 3):
            place, cost = get_nearest(FA, "D2", sites)
            choice.append([1, 'D2', 'A', flag[1] + 3, place, cost])

        if (flag[2] < 3):
            place, cost = get_nearest(FB, "D1", sites)
            choice.append([2, 'D1', 'B', flag[2], place, cost])
        if (flag[3] < 3):
            place, cost = get_nearest(FB, "D2", sites)
            choice.append([3, 'D2', 'B', flag[3] + 3, place, cost])
        
        if (flag[4] < 6):
            place, cost = get_nearest(FC, "D1", sites)
            choice.append([4, 'D1', 'C', flag[4], place, cost])
        if (flag[5] < 6):
            place, cost = get_nearest(FC, "D2", sites)
            choice.append([5, 'D2', 'C', flag[5] + 6, place, cost])
            
        tmp = sorted(choice, key=lambda elem: elem[5])[0]
        flag[tmp[0]] += 1
        s = tmp[2] + str(tmp[3]) + " " + tmp[1] + " " + tmp[4] + " " + str(tmp[5])
        sites.remove(tmp[4]) 
        fp.write(s + "\n")
    fp.close()
    schedule_method_1(select_file) 

def select(fm, src, sites, num):
    name_index, index_name = get_name_index()
    paths = []
    for i in range(0, len(fm[0])):
        if index_name[i] in sites:
            paths.append([i, float(fm[name_index[src]][i])])
    paths.sort(key=lambda path: path[1])
    points = []
    for i in range(0, num):
        points.append([src, index_name[paths[i][0]], paths[i][1]])

    return points

def schedule_method_2(select_file):
    fp = open(select_file)
    line = fp.readline()
    cars = []
    
    while line:
        line = line.strip()
        cars.append(line)
        line = fp.readline()
    fp.close()
    cars.reverse()
    last_begin = 0
    i = 0
    schedule_file = "./schedule_11.dat"
    fp = open(schedule_file, 'w')
    spa = get_spm("./SPA.dat")
    spb = get_spm("./SPB.dat")
    spc = get_spm("./SPC.dat")
    ta = get_time_matrix("./TA.dat")
    tb = get_time_matrix("./TB.dat")
    tc = get_time_matrix("./TC.dat")

    for car in cars:
        car_type = get_car_type(car)
        cost = get_cost(car)
        src = get_car_src(car)
        dst = get_car_dst(car)
        if i == 0:
            begin = 0
            i += 1
        else:
            begin = last_begin + (last_cost - cost)
        s = car_type + " " + src + " " + str(round(begin * 60, 1)) + " "
        if car_type[0] == 'A':
            shortest_path = get_shortest_path(spa, ta, src, dst)
        elif car_type[0] == 'B':
            shortest_path = get_shortest_path(spb, tb, src, dst)
        elif car_type[0] == 'C':
            shortest_path = get_shortest_path(spc, tc, src, dst)
        
        leave = begin
        for path in shortest_path:
            arrival = leave + path[1]
            leave = arrival
            s += path[0] + " " + str(round(arrival * 60, 1)) + " " + str(round(leave * 60, 1)) + " "
        fp.write(s + "\n")

        last_begin = begin
        last_cost = cost

    fp.close()

def select_method_2():
    FA = get_floyd_matrix("./FA.dat")
    FB = get_floyd_matrix("./FB.dat")
    FC = get_floyd_matrix("./FC.dat")
    sites = get_sites()
    count = 24
    flag = [0] * 6
    select_file = "./select_11.dat"
    fp = open(select_file, 'w')
    items = []

    c_count = 6
    i = 0
    c13 = select(FC, 'D1', sites, c_count)
    for c in c13:
        s = 'C' + str(i) + " " + c[0] + " " + c[1] + " " + str(c[2]) + "\n" 
        items.append([c[2], s])
        #fp.write(s)
        sites.remove(c[1])
        i += 1
    c13 = select(FC, 'D2', sites, c_count)
    for c in c13:
        s = 'C' + str(i) + " " + c[0] + " " + c[1] + " " + str(c[2]) + "\n" 
        items.append([c[2], s])
        #fp.write(s)
        sites.remove(c[1])
        i += 1

    b_count = 3
    i = 0
    b13 = select(FB, 'D1', sites, b_count)
    for b in b13:
        s = 'B' + str(i) + " " + b[0] + " " + b[1] + " " + str(b[2]) + "\n" 
        items.append([b[2], s])
        #fp.write(s)
        sites.remove(b[1])
        i += 1
    b13 = select(FB, 'D2', sites, b_count)
    for b in b13:
        s = 'B' + str(i) + " " + b[0] + " " + b[1] + " " + str(b[2]) + "\n" 
        items.append([b[2], s])
        #fp.write(s)
        sites.remove(b[1])
        i += 1

    a_count = 3
    i = 0
    a13 = select(FA, 'D1', sites, a_count)
    for a in a13:
        s = 'A' + str(i) + " " + a[0] + " " + a[1] + " " + str(a[2]) + "\n" 
        items.append([a[2], s])
        #fp.write(s)
        sites.remove(a[1])
        i += 1
    a13 = select(FA, 'D2', sites, a_count)
    for a in a13:
        s = 'A' + str(i) + " " + a[0] + " " + a[1] + " " + str(a[2]) + "\n" 
        items.append([a[2], s])
        #fp.write(s)
        sites.remove(a[1])
        i += 1
    items.sort(key=lambda item: item[0])
    for item in items:
        fp.write(item[1])
    fp.close()
    
    schedule_method_2(select_file) 

def main():
    if sys.argv[1] == '1':
        single_car = 1
    else:
        single_car = 0

    if single_car == 1:
        select_method_2()
    else:
        select_method_1()


if __name__ == "__main__":
    main()
