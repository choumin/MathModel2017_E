#!/bin/python

#coding=utf-8


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

def get_cost(fm, src, z):
    name_index, index_name = get_name_index()
    return fm[name_index[src]][name_index[z]]
    
def get_car_type(line):
    index = line.find(" ")
    return line[0 : index]

def get_src(line):
    begin = line.find(" ")
    begin = line.find(" ", begin + 1)
    end = line.find(" ", begin + 1)
    return line[begin + 1 : end]

def get_full_path(fname, zarray):
    full_path = []
    fp = open(fname)
    line = fp.readline()
    fa = get_floyd_matrix("./FA.dat")
    fb = get_floyd_matrix("./FB.dat")
    fc = get_floyd_matrix("./FC.dat")
    while line:
        line = line.strip()
        car_type = get_car_type(line)
        src = get_src(line)
        for z in zarray:
            if car_type[0] == 'A':
                cost = get_cost(fa, src, z)
            elif car_type[0] == 'B':
                cost = get_cost(fb, src, z)
            else: 
                cost = get_cost(fc, src, z)
            full_path.append([car_type, src, z, cost])
        line = fp.readline()

    return full_path

def get_diff(queue, path):
    path1 = queue[len(queue) - 2]
    return path[3] - path1[3]

def get_whole_cost(full_path, src, z, queue):
    for path in full_path:
        if path[1] == src and path[2] == z:
            break
    if len(queue) < 2 or get_diff(queue, path) >= 10:
        return path, path[3]
    else:
        return path, path[3] + get_diff(queue, path)

def get_all_sites(fname):
    fp = open(fname)
    sites = []
    line = fp.readline()
    while line:
        line = line.strip()
        if line[0] == 'F':
            sites.append(line)
        line = fp.readline()
    fp.close()
    return sites

def get_available(zqueue):
    sites = get_all_sites("./name_index.dat")
    for z in zqueue:
        for path in zqueue[z]:
           sites.remove(path[1])
    #print "sizeof sites: ", len(sites)
    return sites

def get_min_cost(car_type, z, sites):
    fa = get_floyd_matrix("./FA.dat")
    fb = get_floyd_matrix("./FB.dat")
    fc = get_floyd_matrix("./FC.dat")
    
    if car_type[0] == 'A':
        fm = fa
    elif car_type[0] == 'B':
        fm = fb
    elif car_type[0] == 'C':
        fm = fc
    else:
        print "error!~~~~~~~~~~"
        exit()
    name_index, index_name = get_name_index()
    min_cost = 1000000
    min_dst = ""
    
    for site in sites:
        cost = fm[name_index[z]][name_index[site]]
        if cost < min_cost:
            min_cost = cost
            min_dst = site
    return min_cost, min_dst
    
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
        
def get_pre_time():
    fp = open("./schedule_11.dat")
    line = fp.readline()
    line = line.strip()
    index = line.rfind(" ")
    fp.close()
    return float(line[index + 1 : ])

def plan(zarray):

    ##24->6
    ##########################################################
    select_file = "./select_11.dat"
    full_path = get_full_path(select_file, zarray)
    full_path.sort(key=lambda elem : elem[3])
    zqueue = {}
    flag = {}
    for z in zarray:
        zqueue[z] = []
    for path in full_path:
        if path[1] in flag:
            continue
        z = path[2]
        if len(zqueue[z]) < 2 or get_diff(zqueue[z], path) >= 10:
            zqueue[z].append(path)
        else:
            min_z = ""
            min_cost = 1000000
            min_path = "" 
            for tmpz in zarray:
                tmpath, cost = get_whole_cost(full_path, path[1], tmpz, zqueue[tmpz])
                if cost < min_cost:
                    min_cost = cost
                    min_z = tmpz
                    min_path = tmpath
            z = min_z
            zqueue[z].append(min_path)
        flag[path[1]] = z
    ##########################################################

    ##6->24
    ##########################################################
    goal = {}
    goal_count = 24
    sites = get_available(zqueue)
    zqueue_index = {}
    for z in zarray:
        zqueue_index[z] = len(zqueue[z]) - 1
    #print zqueue_index

    while True:
        if len(goal) == goal_count:
            break
        min_z = ""
        min_cost = 1000000
        min_dst = ""
        for z in zarray:
            if zqueue_index[z] < 0:
                continue
            path = zqueue[z][zqueue_index[z]]
            cost, dst = get_min_cost(path[0], z, sites)
            if cost < min_cost:
                min_cost = cost
                min_z = z
                min_dst = dst 
        #print min_dst, len(goal)
        sites.remove(min_dst) 
        path = zqueue[min_z][zqueue_index[min_z]]
        goal[path[0]] = min_dst
        zqueue_index[min_z] -= 1
    #########################################################

    ##timeline
    ########################################################
    pre_time = get_pre_time() 
    zntime = {}
    for z in zarray:
        zntime[z] = pre_time

    spa = get_spm("./SPA.dat")
    spb = get_spm("./SPB.dat")
    spc = get_spm("./SPC.dat")
    ta = get_time_matrix("./TA.dat")
    tb = get_time_matrix("./TB.dat")
    tc = get_time_matrix("./TC.dat")

    fp_st = open("./security_time.dat", 'w') 
    fp_sche = open("./schedule_123.dat", 'w')

    charge_time = 10
    leave = pre_time
    for z in zarray:
        for path in zqueue[z]:
            leave = pre_time
            if path[0][0] == 'A':
                sp = get_shortest_path(spa, ta, path[1], path[2])
            elif path[0][0] == 'B':
                sp = get_shortest_path(spb, tb, path[1], path[2])
            elif path[0][0] == 'C':
                sp = get_shortest_path(spc, tc, path[1], path[2])
            else:
                print "ERROR!"
                exit()

            s = path[0] + " "

            i = 0
            for p in sp:
                arrival = leave + p[1] * 60 
                leave = arrival
                if i == len(sp) - 1:
                #if p[0][0] == 'Z':
                    s += p[0] + " " + str(round(arrival, 1)) + " "
                else:
                    s += p[0] + " " + str(round(arrival, 1)) + " " + str(round(leave, 1)) + " "
                i += 1
            
            if arrival < zntime[z]:
                wait = zntime[z] - arrival
            else:
                wait = 0
                zntime[z] = arrival
            zntime[z] += charge_time

            leave = arrival + wait + charge_time
            if wait > charge_time:
                sec_time = 2 * charge_time
            else:
                sec_time = wait + charge_time

            fp_st.write(path[0] + " " + str(sec_time) + "\n")
            
            s += str(round(leave, 1)) + " "

            if path[0][0] == 'A':
                sp = get_shortest_path(spa, ta, z, goal[path[0]])
            elif path[0][0] == 'B':
                sp = get_shortest_path(spb, tb, z, goal[path[0]])
            elif path[0][0] == 'C':
                sp = get_shortest_path(spc, tc, z, goal[path[0]])
            else:
                print "ERROR!"
                exit()
            for p in sp:
                arrival = leave + p[1] * 60
                leave = arrival
                s += p[0] + " " + str(round(arrival, 1)) + " " + str(round(leave, 1)) + " "
            fp_sche.write(s + "\n") 
            

    ########################################################    
    fp_st.close()
    fp_sche.close()
    
    #for z in zarray:
    #    print z
    #    for path in zqueue[z]:
    #        print path
    exposed_time = merge()

    return exposed_time

def get_car_type(line):
    index = line.find(" ")
    return line[0 : index]

def get_schedule(line):
    index = line.find(" ")
    return line[index + 1 :]

def get_start_time(line):
    elems = line.split(" ")
    return float(elems[2])

def get_end_time(line):
    index = line.rfind(" ")
    return float(line[index + 1 : ])

def get_sec_time(line):
    index = line.rfind(" ")
    return round(float(line[index + 1 : ]), 1)
     
def merge():
    f1 = "./schedule_11.dat"
    f2 = "./schedule_123.dat"
    f3 = "./security_time.dat"
    f4 = "./schedule_1123.dat"

    start = {}
    end = []
    car_plan = []
    fp = open(f1)
    line = fp.readline()
    fore_d = {}
    while line:
        line = line.strip()
        car_type = get_car_type(line) 
        car_plan.append(car_type)
        fore_d[car_type] = get_schedule(line)
        start[car_type] = get_start_time(line) 
        line = fp.readline()
    fp.close()

    fp = open(f2)
    line = fp.readline()
    later_d = {}
    while line:
        line = line.strip()
        car_type = get_car_type(line) 
        later_d[car_type] = get_schedule(line)
        end.append(get_end_time(line))
        line = fp.readline()
    fp.close()

    fp = open(f3)
    line = fp.readline()
    sec_time = {}
    while line:
        line = line.strip()
        car_type = get_car_type(line)
        sec_time[car_type] = get_sec_time(line)
        line = fp.readline()
    fp.close()

    all_time = {}
    real_time = {}
    longest = max(end)
    for car in car_plan:
        all_time[car] = longest - start[car]
        real_time[car] = all_time[car] - sec_time[car]


    fp = open(f4, 'w')
    for car in car_plan:
        fp.write(car + " " + fore_d[car] + " " + later_d[car] + " " + str(all_time[car]) + " " + str(sec_time[car]) + " " + str(real_time[car]) + "\n")
    exposed_time = sum([real_time[car] for car in real_time])
    fp.write("\n" + "Total exposed time: " + str(exposed_time) + " " + str(round(exposed_time / 60, 2)))
    fp.close()

    #print ""
    #print "Total exposed time: ", exposed_time, round(exposed_time / 60, 2)
    return exposed_time
    
def main():
    plan_set = [['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J25', 'J34'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J25', 'J36'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J25', 'J42'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J25', 'J49'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J34', 'J36'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J34', 'J42'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J34', 'J49'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J36', 'J42'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J36', 'J49'],
                ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06', 'J42', 'J49']
            ]
    #zarray = ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06']
    #zarray = ['Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06']
    cmp_result = "compare_result.dat"
    fp = open(cmp_result, "w")
     
    tmp = []
    for p in plan_set:
        exposed_time = plan(p)
        tmp.append([p[6] + "," + p[7], exposed_time])
        #print "Total exposed time: ", exposed_time, round(exposed_time / 60, 2)
        #print exposed_time, round(exposed_time / 60, 2), p
        s = str(exposed_time) + " minutes, " + str(round(exposed_time / 60, 2)) + " hours  " + str(p)
        print s 
        fp.write(s + '\n')
    fp.close()
    tmp.sort(key=lambda elem: elem[1])
    print "The newly added nodes is: " + tmp[0][0]


if __name__ == "__main__":
    main()
    
