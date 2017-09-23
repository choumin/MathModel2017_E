#!/bin/python

import sys

def get_sn():
    fp = open("./sn.dat")
    line = fp.readline()
    line = line.strip()
    return line

def get_point_name(line):
    index = line.find(' ')
    return line[0 : index]

def get_near_points(line):
    index = line.find(' ')
    nps = []
    tmp = line[index + 1 : ].split(' ')
    for p in tmp:
        index = p.find(',')
        nps.append(p[0 : index])
    return nps
        
def get_dir(line):
    index = line.find(' ')
    nps = []
    tmp = line[index + 1 : ].split(' ')
    for p in tmp:
        index = p.find(',')
        nps.append(p[index + 1 : ])
    return nps
    
def modify_linkfile(edge_name):
    linkfile = "./linkfile.dat"
    fp = open(linkfile)
    line = fp.readline()
    content = []
    near_points = []
    #near_points.append(edge_name)
    link = {}
    while line:
        line = line.strip()
        pname = get_point_name(line)
        nps = get_near_points(line)
        link[pname] = []
        for n in nps:
            link[pname].append(n)
        content.append(line)
        line = fp.readline()
        if pname == edge_name:
            for n in nps:
                near_points.append(n)
        else:
            for n in nps:
                if n == edge_name:
                    near_points.append(pname)
    fp.close()
    #print near_points
    #for key in link:
    #    print key, link[key]

    fp = open(linkfile, 'w')
    flag = []
    for i in range(0, len(near_points)):
    #for np in near_points:
        np = near_points[i]
        ok = False
        #print np
        for key in link:
            #print key, link[key], np
            if key != edge_name and np in link[key]:
                #print "remove", np
                #near_points.remove(np)
                flag.append(np)
                ok = True
                break
        if ok == False:
            if np in link and len(link[np]) > 1:
                #near_points.remove(np)
                flag.append(np)
    for f in flag:
        near_points.remove(f)

    for line in content:
        ok = False
        pname = get_point_name(line)
        nps = get_near_points(line)
        ds = get_dir(line)
        for np in near_points:
            if np == pname:
                ok = True
                break
        if ok == True:
            continue
        s = pname
        i = 0
        for np1 in nps:
            ok = False
            for np2 in near_points:
                if np1 == np2:
                    ok = True
                    break
            if ok == True:
                i += 1
                continue
            s += " " + np1 + ',' + ds[i]
            i += 1
        fp.write(s + '\n')
        
    fp.close()

    return near_points
    
def modify_linkfile_2(edge_name):
    linkfile = "./linkfile.dat"
    near_points = []
    fp = open(linkfile)
    line = fp.readline()
    fp.close()

    #fp = open(linkfile, 'w')
    
    #fp.close()

    return near_points
            
def modify_name_index(edge_name, near_points):
    name_index = "./name_index.dat"
    fp = open(name_index)
    line = fp.readline()
    content = []
    while line:
        pname = line.strip()
        if pname in near_points or pname == edge_name:
            line = fp.readline()
            continue
        content.append(line)
        line = fp.readline()
    fp.close()

    fp = open(name_index, 'w')
    for line in content:
        fp.write(line)
    fp.close()
def modify_coordfile(edge_name, nps):
    coordfile = "./coordfile.dat"
    fp = open(coordfile)
    line = fp.readline()
    content = []
    while line:
        pname = get_point_name(line)
        if pname in nps or pname == edge_name:
            line = fp.readline()
            continue
        content.append(line)
        line = fp.readline()
    fp.close()

    fp = open(coordfile, 'w')
    for line in content:
        fp.write(line)
    fp.close()

def main():
    #sn = get_sn()
    sn = sys.argv[1]
    edge_name = 'J' + sn
    nps = modify_linkfile(edge_name)
    #print edge_name, nps
    modify_name_index(edge_name, nps)
    modify_coordfile(edge_name, nps)
    
if __name__ == "__main__":
    main()
