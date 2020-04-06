#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 16:25:10 2018

@author: ofsevit

This creates a shorter file which only has volume and speed
This also assigns a day of week to each day
Good for a few days at a time, but to rescrape months/years of data, using
a different file yields better results because it is easier to find errors
when they arise, which they will, because selenium

Probably a good step would be to add a "download date" parameter to each line
so that bad data could be sorted out, but for now, this works.
"""

# list of all AET sites

list_to_scrape = [
'AET14_EB','AET13_EB','AET12_EB','AET11_EB','AET10_EB',
'AET09_EB','AET08_EB','AET07_EB','AET06_EB','AET05_EB',
'AET04_EB','AET03_EB','AET02_EB','AET01_EB','AET14_WB',
'AET13_WB','AET12_WB','AET11_WB','AET10_WB','AET09_WB',
'AET08_WB','AET07_WB','AET06_WB','AET05_WB','AET04_WB',
'AET03_WB','AET02_WB','AET01_WB','AET15_NB','AET15_SB',
'AET16_NB','AET16_SB'
]

all_rows = []

#scrapes lists one by one, which is easier for error handling

for i in list_to_scrape:    

    import csv
    
    import time
    
    from datetime import date
    
    from selenium import webdriver
    
    import matplotlib.pyplot as plt
    
    import numpy as np
    
    #from selenium.webdriver.common.keys import Keys
    
    from bs4 import BeautifulSoup as soup
    
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    
    # open MHD homepage; otherwise receives a time out error
    
    browser.get('https://mhd.ms2soft.com/tcds/tsearch.asp?loc=Mhd&mod=')
    
    # open the specific first page you want to scrape; replace this URL
    
    input_url = 'https://mhd.ms2soft.com/tcds/tcount_gcs.asp?offset=0&id=7022534&a=96&local_id_dir='+i+'&jump_date=2019-10-23&speedDate=2019-10-30&sdate=9/28/2018&classDate=&gapDate=&count_type=speed&int=15' # blank space, baby
    
    browser.get(input_url)

    # Go to most recent data on site, with error handling
    # this is in here multiple times because it doesn't always work so 
    # basically it gives it several chances to work. Because selenium sucks
    try:
        browser.find_element_by_xpath('//*[@title="Most Recent"]').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@title="Most Recent"]').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@title="Most Recent"]').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@title="Most Recent"]').click()
    except:
        pass
    
    # find the most recent date scraped, using the most recent file
    # there is probably a more efficient way to do this, but it seems to work at least
    
    date_to = ''
    
    csv_loc = 'combined_mar_29.csv' # <-- change this file name as needed!
    # look in http://ariofsevit.com/files/AET/ for the large file
    
    with open(csv_loc, newline='') as csvfile:
        csv = csv.reader(csvfile, delimiter=';', quotechar='|')
        
        dates = []
        
        AET = i.split('_')[0]
        
        for line in csv:
        
            if line[0] == AET:
                
                dates.append(line[2])
                
        date_to = (max(dates))
            
    # define how many pages you want to scrape; use this if you want to limit how far back to go
    # not really an issue if you have date_to; moreso if you want to redownload the whole dataset
    # NB different AET sites have slightly different data sets; some days are missing for each
    # anyway, keep it at 200 or whatever unless youre looking back more than a few months
    
    iterations = 200
    
    # create an empty list in which to put all the data    
    
    while iterations > 0:
        
        # find the date of the URL
    
        current_url = browser.current_url
        
        date_url = current_url
        
        date_long = date_url.split('=')[5] #<-- THIS MAY CHANGE BASED ON THE INPUT URL, generally 5
        
        date_text = date_long.split('&')[0]
        
        if date_text == date_to:
            
            break #break when you've gotten as far back as the last data
        
        # create a py date from the date in the data
        
        year = int(date_text.split('-')[0])
        month = int(date_text.split('-')[1])
        day = int(date_text.split('-')[2])
        
        day_of_week = date(year, month, day).weekday()
    
        #hand off to BS
        soup1=soup(browser.page_source, 'html.parser')
        
        # find the table with values in it
        
        table = soup1.find("table",{"class":"frmNew"})
        
        rows = table.find_all('tr')
    
        # create an empty list for each day, necessary to then delete rows w/o data
        
    #   create a short list for each date, start adding items to the list
        day_short = []
        
        for row in rows:
            
            cells = row.find_all('td')
            cell_list = []
            short_list = []
            step = 0
            speed_tot = 0
            speed = 0
            cell_list.append(date_text)
            short_list.append(i.split('_')[0])
            short_list.append(i.split('_')[1])
            short_list.append(date_text)
            for cell in cells:
                cell_list.append(cell.get_text())
    
        # calculate speed based on speed buckets
    
                if step == 2:
                    speed_tot += int(cell.get_text())*(7.5)
                if step > 2:
                    speed_tot += int(cell.get_text())*(7.5+5*step)
                step += 1
    
        # last item in list is volume, so don't count this
        # len > 5 to exclude calculating for lines w/o data, which will throw errors
    
            if len(cell_list)>5:
                speed_tot -= int(cell_list[-1])*(7.5+5*(step-1))
            if len(cell_list)>5:
                try:
                    speed = speed_tot / int(cell_list[-1])
                except:
                    speed = 0
            cell_list.append(speed)
            
            # append the rest o the stuff

            short_list.append(cell_list[1])
            short_list.append(cell_list[-2])
            short_list.append(cell_list[-1])

            day_short.append(short_list)
        #    print(len(day_of_rows)) # use this to check progress if interested
        
        # delete rows that don't have values in them
        
        del day_short[0],day_short[0],day_short[-1]
        
        # append the data to the full data list
        
        for row in day_short:
            all_rows.append(row)
        
        # cycle to the next page, with error handling
        
        print(AET,' ',len(all_rows))
        
        try:
            browser.find_element_by_xpath('//*[@title="Older"]').click()
        except:
            pass
        
        # reduce interations by 1, again, only used with iterations
        iterations -= 1
    
#        # print statement to show progress is being made
        # reasonably useful for big data pulls
#        if iterations%10 == 0:
#            print(iterations,time.time())
#            print(date_text)
    
        # write to new csv
        # this way if things go awry, you haven't messed up the main CSV
        # there is then code to combine them
        # although this could probably be changed
    
    import csv
        
    with open('new_mar_30.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerows(all_rows)
        
    browser.quit()     