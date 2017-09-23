#!/bin/sh

echo "***********************************************"
echo "Optimization for single car: "  
echo ""
python ./get_distance_matrix.py
python ./get_time_matrix.py
python ./get_shortest_path_matrix.py
python ./select_and_schedule_1.py 1
python ./select_and_schedule_2.py 0
python ./merge.py
echo "***********************************************"
echo ""
echo ""


echo "***********************************************"
echo "Optimization using dispersing policy: " 
echo ""
python ./get_distance_matrix.py
python ./get_time_matrix.py
python ./get_shortest_path_matrix.py
python ./select_and_schedule_1.py 0
python ./select_and_schedule_2.py 1
python ./merge.py
echo "***********************************************"
echo ""
echo ""

echo "***********************************************"
echo "Optimization for sing car and using dispersing policy: "  
echo ""
python ./get_distance_matrix.py 
python ./get_time_matrix.py
python ./get_shortest_path_matrix.py
python ./select_and_schedule_1.py 1
python ./select_and_schedule_2.py 1
python ./merge.py
echo "***********************************************"
