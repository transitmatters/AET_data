#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This will combine multiple AET CSVs to one single file.

"""
import matplotlib.pyplot as plt

import numpy as np

import time

print(time.ctime())

all_list = []

# files to be combined in the following list: 
# if using a bunch of AET files, it would be the AET list, hence the name

aet_list=['combined_short.csv','new_download.csv']

for item in aet_list:

    import csv
    
    csv_file = item
    

    with open(csv_file, newline='') as csvfile:
        csv = csv.reader(csvfile, delimiter=';', quotechar='|')

        for line in csv:
            
            new_line = []
            
            new_line.append(line[0])                        
            new_line.append(line[1])                        
            new_line.append(line[2])                        
            new_line.append(line[3])                        
            new_line.append(line[4])                        
            new_line.append(line[5])
            
            all_list.append(new_line)
     
    print(time.ctime())


import csv

with open('combined_mar_29.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';', lineterminator='\n')
    writer.writerows(all_list)

print(time.ctime())
