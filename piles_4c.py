#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This will extract percentiles from the main data file for the AET and direction
specified in like 20(ish), it could certainly be looped. Right now it is not
efficient (it calculates the percentiles each time) and there are also several
other areas where the code could be tightened up and/or made more efficient.

Requires two inputs:
    
    AET must be defined 
    direct must be defined
    
    Approximately in line 30
    
One additional input, in line 90 or so, if you wish to use weekends instead of
weekdays, use >5 instead of <6.

Finally, the current chart shows the first 18 days of march, but the coloring 
could be changed to be made it more legible, this is mostly a proof of concept.

"""
import matplotlib.pyplot as plt

import numpy as np

import csv

import time

from datetime import date

# select which AET and direction you want to use
# a list of AETs is found in a later section of this code

AET = 'AET07' # <-- Input AET
direct = 'EB' # <-- Input Direction

##########
#
# The most recent of these files can generally be found at ariofsevit.com/files/
#
##########

csv_file = 'combined_apr_24.csv'

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

# create a list for percentiles, 1-99 for volume, 1-90 for speed
# since 90 is almost always free flow, 95 and 99 tell us nothing
# speed since removed from this file
# there was a reason I called this tvs_list and I don't remember, it's not
#   short for televisions, though.


# weekdays vs weekends
        
        if line[0] == AET and line[1] == direct and doy < 6: # < 6 for weekdays only, use > 5 for weekends
                            
            tvs_list.append([line[3],int(line[4]),(float(line[5])),year])
                        
    for hour in hours:

        # I have other files which do speed/volume comparison, so that's still here
        # volume percentile, speed, piles, etc
        
        vpc_list = []
        spc_list = []
        piles = []
        
        for i in tvs_list:

            if i[0] == hour and i[3] < 2020: # create %iles for before covid
                vpc_list.append(i[1])
                spc_list.append(i[2])

    # do all the percentile calculations, then append it to all the list

        vpc_1 = np.percentile(vpc_list,1)
        vpc_5 = np.percentile(vpc_list,5)
        vpc_10 = np.percentile(vpc_list,10)
        vpc_50 = np.percentile(vpc_list,50)
        vpc_90 = np.percentile(vpc_list,90)
        vpc_95 = np.percentile(vpc_list,95)
        vpc_99 = np.percentile(vpc_list,99)

        spc_1 = np.percentile(spc_list,1)
        spc_5 = np.percentile(spc_list,5)
        spc_10 = np.percentile(spc_list,10)
        spc_50 = np.percentile(spc_list,50)
        spc_90 = np.percentile(spc_list,90)
    
        piles.append(hour)   
        piles.append(vpc_1)   
        piles.append(vpc_5)   
        piles.append(vpc_10)   
        piles.append(vpc_50)   
        piles.append(vpc_90)   
        piles.append(vpc_95)   
        piles.append(vpc_99)   
        piles.append(spc_1)   
        piles.append(spc_5)   
        piles.append(spc_10)   
        piles.append(spc_50)   
        piles.append(spc_90)   
        
        piles_list.append(piles)   

            

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

list_of_weeks = []

while b < 43: #raise this as more data becomes available

    week_list = []
        
    for i in range(a,b):
        
        day_list = []
        
        for line in march_data:
    
            if line[1] == i:
                            
                day_list.append((int(line[0][4])*4))
    
        week_list.append(day_list)
        
    week_avg = [sum(elem)/len(elem) for elem in zip(*week_list)]

    a += 7
    b += 7

    list_of_weeks.append(week_avg)

w1 = list_of_weeks[0]            
w2 = list_of_weeks[1]            
w3 = list_of_weeks[2]            
w4 = list_of_weeks[3]            
w5 = list_of_weeks[4]            
w6 = list_of_weeks[5]  
# create more weeks as data becomes available          

# create chart
# mostly from spd_vol_emorecomplex_15_grid.py
# speed data removed to just show volume
        
labels = [' ']
top1 = []
top5 = []
top10 = []
top50 = []
top90 = []
top95 = []        
v1 = []
v5 = []
v10 = []
v50 = []
v90 = []
v95 = []
v99 = []
vmedian = []

# create background data

for line in piles_list:
    
    lab_time = line[0].split(':')[1]
            
    if lab_time.split(' ')[0] == '00':
    
        labels.append(line[0].split(':')[0]+' '+line[0].split(' ')[-1])
    
    else:
    
        labels.append('')
    
    # create bottoms, for the stacked line chart
    # this could be done as a stacked area, too, but I have the code for bars, so …

    top1.append(float(line[1])*4)
    top5.append(float(line[2])*4)
    top10.append(float(line[3])*4)
    top50.append(float(line[4])*4)
    top90.append(float(line[5])*4)
    top95.append(float(line[6])*4)

    # create percentile ranges
    
    p15 = (float(line[2])*4) - (float(line[1])*4)
    p510 = (float(line[3])*4) - (float(line[2])*4)
    p1050 = (float(line[4])*4) - (float(line[3])*4)
    p5090 = (float(line[5])*4) - (float(line[4])*4)
    p9095 = (float(line[6])*4) - (float(line[5])*4)
    p9599 = (float(line[7])*4) - (float(line[6])*4)
    p050 = (float(line[4])*4)

    # add to lists
    
    v1.append(float(line[1])*4)
    v5.append(p15)
    v10.append(p510)
    v50.append(p1050)
    v90.append(p5090)
    v95.append(p9095)
    v99.append(p9599)
    vmedian.append(p050)
    
# create all the parameters for the charts

fig, ax1 = plt.subplots()

N = 96
ind = np.arange(N)    # the x locations for the groups
width = 1       # the width of the bars: can also be len(x) sequence
plt.title(loc+': weeks since March 1')
plt.xticks(ind, labels, rotation = 'vertical')

ax1.set_ylabel('Volume')

v1 = ax1.bar(ind, v1, width, color = '#ffffff', alpha = 0)
v2 = ax1.bar(ind, v5, width, bottom = top1, color = '#dddddd')
v3 = ax1.bar(ind, v10, width, bottom = top5, color = '#cccccc')
v4 = ax1.bar(ind, v50, width, bottom = top10, color = '#bbbbbb')
v5 = ax1.bar(ind, v90, width, bottom = top50, color = '#bbbbbb')
v6 = ax1.bar(ind, v95, width, bottom = top90, color = '#cccccc')
v7 = ax1.bar(ind, v99, width, bottom = top95, color = '#dddddd')
v8 = ax1.plot(ind, vmedian, linewidth = 1, color = '#000000')

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

ax1.legend((v8[0], e1[0],e2[0],e3[0],e4[0],e5[0],e6[0]),('Pre-covid median','Week 1','Week 2','Week 3', 'Week 4','Week 5','Week 6'),
loc='upper center', bbox_to_anchor=(0.5, -0.22),fancybox=True, shadow=True, ncol=4)

# determine decline from pre-covid data to week 6

median = sum(vmedian)/96

now = sum(w6)/96 #change w6 for other week of interest

decline = now/median

textstr = str(round(100*(1-decline),1))+'%\ndecline'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=12, 
         verticalalignment='top', bbox = props)
    
plt.savefig(AET+direct+'_Apr10.png', dpi = 300, bbox_inches='tight')

plt.show()

