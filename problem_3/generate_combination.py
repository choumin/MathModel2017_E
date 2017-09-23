#!/bin/python

def main():
    f1 = "combinations_3.dat"
    sites = ['J04', 'J06', 'J08', 'J13', 'J14', 'J15']
    combinations = []
    for i in range(0, len(sites)):
        for j in range(i + 1, len(sites)):
            for k in range(j + 1, len(sites)):
                combinations.append([i, j, k])
    for i in range(0, len(sites)):
        for j in range(i + 1, len(sites)):
            combinations.append([i, j])
            combinations.append([j, i])
    fp = open(f1, 'w')
    for com in combinations:
        if len(com) == 3:
            s = sites[com[0]] + " " + sites[com[1]] + " " + sites[com[2]]
        elif len(com) == 2:
            s = sites[com[0]] + " " + sites[com[1]]
        fp.write(s + "\n") 

    fp.close()

if __name__ == "__main__":
    main()
