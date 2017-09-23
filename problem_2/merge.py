#!/bin/python

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
     
def main():
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

    print ""
    print "Total exposed time: " + str(exposed_time) + " minutes, " + str(round(exposed_time / 60, 2)) + " hours"
    

if __name__ == "__main__":
    main()
