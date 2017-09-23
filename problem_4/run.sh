#!/bin/sh

echo "*******************************************************************"
echo "Get the traffic for each node:"
python ./get_distance_matrix.py
python ./get_time_matrix.py
python ./get_shortest_path_matrix.py
python ./select_and_schedule_1.py
python ./select_and_schedule_2.py
python ./merge1.py
python ./get_node_traffic.py
echo "*******************************************************************"

echo "*******************************************************************"
echo "Get the increasing of whole exposed time for deleting each node:"
num=1
while [ "$num" -lt "63" ]
do 
    node=$num
    if [ "$num" -lt "10" ]
    then
        node=0$num
    fi

    cp ./linkfile.dat.bak ./linkfile.dat
    cp ./name_index.dat.bak ./name_index.dat
    cp ./coordfile.dat.bak ./coordfile.dat
    python ./delete_one_edge.py $node
    python ./get_distance_matrix.py
    python ./get_time_matrix.py
    python ./get_shortest_path_matrix.py
    python ./select_and_schedule_1.py
    python ./select_and_schedule_2.py
    python ./merge2.py $node
    
    num=`expr $num + 1`
done
    python ./get_increasing.py
echo "*******************************************************************"


