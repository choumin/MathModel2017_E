#!/bin/sh

python ./get_distance_matrix.py
python ./get_time_matrix.py
python ./get_shortest_path_matrix.py
python ./select_and_schedule_1.py
python ./select_and_schedule_2.py
python ./merge.py
