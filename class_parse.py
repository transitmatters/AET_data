#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This file uses classification data to look at the numbers of different types 
of vehicles from the MHD website. This includes motorcycles, cars, buses, large
trucks and small trucks. 

Data go back to ~Jan 1, 2019; this only outputs data since Mar 1, 2020.

The following three parameters must be defined:
    
    use_this must be one of the following five lists:
        
        list_of_mcyc
        list_of_car
        list_of_bus
        list_of_struck (small trucks)
        list_of_ltruck (large trucks)

    AET (a list can be found later in the code)
    direct (the direction at the AET)
    
In addition, newer classification data may be available, if so, change the csv_file variable

I'll post new files to ariofsevit.com/files/AET/class
   
One additional input, in line 90 or so, if you wish to use weekends instead of
weekdays, use >5 instead of <6. By default this is set as <6, and other parameters
must be changed to use weekends.

Finally, the current chart shows the first six weeks after March 1, this could be
changed with some code changes.

The three parameters to define are in the following three lines of code:
"""

use_this = list_of_ltruck #<-- spyder may show this as "undefined" but it will be later in the code
AET = 'AET13' # <-- Input AET
direct = 'WB' # <-- Input Direction
csv_file = 'class_apr_29.csv'

import matplotlib.pyplot as plt

import numpy as np

import csv

import time

from datetime import date

# create 15 minute buckets

hours = [
'12:00 AM','12:15 AM','12:30 AM','12:45 AM','1:00 AM','1:15 AM','1:30 AM','1:45 AM',
'2:00 AM','2:15 AM','2:30 AM','2:45 AM','3:00 AM','3:15 AM','3:30 AM','3:45 AM',
'4:00 AM','4:15 AM','4:30 AM','4:45 AM','5:00 AM','5:15 AM','5:30 AM','5:45 AM',
'6:00 AM','6:15 AM','6:30 AM','6:45 AM','7:00 AM','7:15 AM','7:30 AM','7:45 AM',
'8:00 AM','8:15 AM','8:30 AM','8:45 AM','9:00 AM','9:15 AM','9:30 AM','9:45 AM',
'10:00 AM','10:15 AM','10:30 AM','10:45 AM','11:00 AM','11:15 AM','11:30 AM','11:45 AM',
'12:00 PM','12:15 PM','12:30 PM','12:45 PM','1:00 PM','1:15 PM','1:30 PM','1:45 PM',
'2:00 PM','2:15 PM','2:30 PM','2:45 PM','3:00 PM','3:15 PM','3:30 PM','3:45 PM',
'4:00 PM','4:15 PM','4:30 PM','4:45 PM','5:00 PM','5:15 PM','5:30 PM','5:45 PM',
'6:00 PM','6:15 PM','6:30 PM','6:45 PM','7:00 PM','7:15 PM','7:30 PM','7:45 PM',
'8:00 PM','8:15 PM','8:30 PM','8:45 PM','9:00 PM','9:15 PM','9:30 PM','9:45 PM',
'10:00 PM','10:15 PM','10:30 PM','10:45 PM','11:00 PM','11:15 PM','11:30 PM','11:45 PM'
]

# create a list of just March data for this AET
 
with open(csv_file, newline='') as csvfile:
    csv = csv.reader(csvfile, delimiter=';', quotechar='|')

# create empty lists
            
    march_data = []        
    tvs_list = []
    piles_list = []

# calculate weekday

    for line in csv:

        new_line = []
        
        year = int(line[2].split('-')[0])
        month = int(line[2].split('-')[1])
        day = int(line[2].split('-')[2])

        if year == 2020 and month == 3 and line[0] == AET and line[1] == direct:

            new_line.append(line)
            new_line.append(day)
            
            march_data.append(new_line)

        if year == 2020 and month == 4 and line[0] == AET and line[1] == direct:

            new_line.append(line)
            new_line.append(day+31)
            
            march_data.append(new_line)

        
        doy = date(year, month, day).weekday()


# Location text, just a lookup for titling

    if AET == 'AET09':
        loc = 'Edgell Rd, Framingham'
    if AET == 'AET08':
        loc = 'Southborough (Between Rt 9 and 495)'
    if AET == 'AET07':
        loc = 'Hopkinton (west of 495)'
    if AET == 'AET06':
        loc = 'Charlton'
    if AET == 'AET05':
        loc = 'Brimfield'
    if AET == 'AET04':
        loc = 'Ludlow'
    if AET == 'AET03':
        loc = 'Westfield'
    if AET == 'AET02':
        loc = 'Blandford'
    if AET == 'AET01':
        loc = 'Lee'
    if AET == 'AET15':
        loc = 'Tobin Bridge'
    if AET == 'AET16':
        loc = 'Sumner/Callahan Tunnel'
    if AET == 'AET10':
        loc = 'Weston'
    if AET == 'AET11':
        loc = 'Newtonville'
    if AET == 'AET12':
        loc = 'Everett St (Brighton)'
    if AET == 'AET13':
        loc = 'Comm Ave/BU Bridge'
    if AET == 'AET14':
        loc = 'Ted Williams Tunnel'

    if direct == 'EB':
        loc += ', Eastbound'     
    if direct == 'WB':
        loc += ', Westbound'  
    if direct == 'NB':
        loc += ', Northbound'     
    if direct == 'SB':
        loc += ', Southbound'  

# this code creates data for weeks after March 1
# a and b here are the start and end of each work week
# they would need to be changed for weekend data

a = 2
b = 7

list_of_mcyc = []
list_of_car = []
list_of_bus = []
list_of_struck = []
list_of_ltruck = []

while b < 43: #raise this as more data becomes available

    week_list_mcyc = []
    week_list_car = []
    week_list_bus = []
    week_list_struck = []
    week_list_ltruck = []
        
    for i in range(a,b):
        
        day_list_mcyc = []
        day_list_car = []
        day_list_bus = []
        day_list_struck = []
        day_list_ltruck = []
        
        for line in march_data:
    
            if line[1] == i:
                            
                day_list_mcyc.append((int(line[0][4]))*4)
                day_list_car.append((int(line[0][5]))*4)
                day_list_bus.append((int(line[0][6]))*4)
                day_list_struck.append((int(line[0][7]))*4)
                day_list_ltruck.append((int(line[0][8]))*4)
    
        week_list_mcyc.append(day_list_mcyc)
        week_list_car.append(day_list_car)
        week_list_bus.append(day_list_bus)
        week_list_struck.append(day_list_struck)
        week_list_ltruck.append(day_list_ltruck)
        
    week_avg_mcyc = [sum(elem)/len(elem) for elem in zip(*week_list_mcyc)]
    week_avg_car = [sum(elem)/len(elem) for elem in zip(*week_list_car)]
    week_avg_bus = [sum(elem)/len(elem) for elem in zip(*week_list_bus)]
    week_avg_struck = [sum(elem)/len(elem) for elem in zip(*week_list_struck)]
    week_avg_ltruck = [sum(elem)/len(elem) for elem in zip(*week_list_ltruck)]

    a += 7
    b += 7

    list_of_mcyc.append(week_avg_mcyc)
    list_of_car.append(week_avg_car)
    list_of_bus.append(week_avg_bus)
    list_of_struck.append(week_avg_struck)
    list_of_ltruck.append(week_avg_ltruck)

for i in use_this:
    
    if len(i) > 96:
        
        del(i[96:])

w1 = use_this[0]            
w2 = use_this[1]            
w3 = use_this[2]            
w4 = use_this[3]            
w5 = use_this[4]            
w6 = use_this[5]  
# create more weeks as data becomes available          

# create chart
# mostly from spd_vol_emorecomplex_15_grid.py
# speed data removed to just show volume
        
labels = [' ']

# create background data

for i in hours:
    
    lab_time = i.split(':')[1]
            
    if lab_time.split(' ')[0] == '00':
    
        labels.append(i.split(':')[0]+' '+i.split(' ')[-1])
    
    else:
    
        labels.append('')
    
    # create bottoms, for the stacked line chart
    # this could be done as a stacked area, too, but I have the code for bars, so …

    
# create all the parameters for the charts

fig, ax1 = plt.subplots()

N = 96
ind = np.arange(N)    # the x locations for the groups
width = 1       # the width of the bars: can also be len(x) sequence
plt.title(loc+': weeks since March 1')
plt.xticks(ind, labels, rotation = 'vertical')

ax1.set_ylabel('Volume')

#ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis if you need/want
# this is for the speed/volume chart, with just volumes, meh.
##ax2.set_ylabel('Speed')
#ax2.set_ylim(0,7500)

# there is probably a good way to get color gradations on this
# I should ask @splillo how he makes his charts

# Weekdays
                      
e1 = ax1.plot(ind, w1, linewidth = 2, color = 'red')
e2 = ax1.plot(ind, w2, linewidth = 2, color = 'orange')
e3 = ax1.plot(ind, w3, linewidth = 2, color = '#ffd500')
e4 = ax1.plot(ind, w4, linewidth = 2, color = 'green')
e5 = ax1.plot(ind, w5, linewidth = 2, color = 'blue')
e6 = ax1.plot(ind, w6, linewidth = 2, color = 'purple')
# create more lines as more data becomes available


box = ax1.get_position()
ax1.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# ax1.set_ylim(0,7500) # use this to set the axes to the same max for all vol charts
ax1.set_axisbelow(True)
ax1.grid(color='gray', linestyle='-', linewidth=0.5, axis = 'y', zorder=0)

#ax1.legend((v2[0],v3[0],v4[0],v5[0],v6[0],v7[0], s1[0], s2[0], s4[0], s6[0]),
#('Volume: 1st – 5th %ile','5th – 10th %ile','10th – 50th %ile', '50th – 90th %ile', '90th – 95th %ile', '95th – 99th %ile', '5th %ile speed','10th %ile speed','25th %ile speed', 'Median speed','75th %ile speed', '90th %ile speed'),
#loc='upper center', bbox_to_anchor=(0.5, -0.3),
#          fancybox=True, shadow=True, ncol=3)

ax1.legend((e1[0],e2[0],e3[0],e4[0],e5[0],e6[0]),('Week 1','Week 2','Week 3', 'Week 4','Week 5','Week 6'),
loc='upper center', bbox_to_anchor=(0.5, -0.22),fancybox=True, shadow=True, ncol=4)

# determine decline from pre-covid data to week 6

sum_list = [sum(w1),sum(w2),sum(w3),sum(w4),sum(w5),sum(w6)]

high = max(sum_list)

high_wk = sum_list.index(high)+1

low = min(sum_list) #change w6 for other week of interest

low_wk = sum_list.index(low)+1

decline = low/high

textstr = 'High: week '+str(high_wk)+'\n' + 'Low: week '+str(low_wk)+'\n'+ str(round(100*(1-decline),1))+'% decline'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

ax1.text(0.72, 0.95, textstr, transform=ax1.transAxes, fontsize=12, 
         verticalalignment='top', bbox = props)
    
plt.savefig(AET+direct+'_Apr10.png', dpi = 300, bbox_inches='tight') #<-- you can change the date here

plt.show()

