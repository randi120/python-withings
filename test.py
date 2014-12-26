#!/usr/bin/env python
"""
Test script
"""
import os
import ConfigParser
import datetime
from withings import * 

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(["withings.conf", os.path.expanduser("~/fitbit/withings.conf")])

if __name__ == '__main__':

    c_key = CONFIG.get('client','client_key')
    c_sec = CONFIG.get('client','client_secret')

    u_key = CONFIG.get('user','user_key')
    u_sec = CONFIG.get('user','user_secret')
    u_id  = CONFIG.get('user','user_id')
   
    #print c_key
    #print c_sec
    #print u_key
    #print u_sec 
    #print u_id

    creds = WithingsCredentials(
                                access_token=u_key,
                                access_token_secret = u_sec,
                                consumer_key = c_key,
                                consumer_secret = c_sec,
                                user_id = u_id
                                )

    client = WithingsApi(creds)

    day_start = datetime.datetime(2014,12,18,0,0)
    day_end = datetime.datetime(2014,12,19,0,0)
    ds_epoch = (day_start - datetime.datetime(1970,1,1)).total_seconds()
    de_epoch = (day_end - datetime.datetime(1970,1,1)).total_seconds()
    
    print "++++++ sleep data ++++++++"
    sleep = client.get_sleep(startdate=ds_epoch, enddate=de_epoch)
    for i in sleep.data['series']:
        print i
    print "sleep state: 0-awake, 1-light, 2-deep, 3-REM"
    
    print "++++++ sleep data (summary)++++++++"
    sleepSummary = client.get_sleep_summary(startdateymd=day_start.strftime('%Y-%m-%d'), enddateymd=day_end.strftime('%Y-%m-%d') )
    print sleepSummary.data['series'][0]

    print "++++++ measurement data ++++++++"
    #meas = client.get_measures(startdate=ds_epoch, enddate=de_epoch)
    meas = client.get_measures(lastupdate=ds_epoch) #everything since last date
    for i in meas: 
        print i.data

    print "++++++ activity data ++++++++"
    act = client.get_activities(startdateymd=day_start.strftime("%Y-%m-%d"), enddateymd=day_start.strftime("%Y-%m-%d"))
    for i in act:
        print i.data



    #client.get_intraday(startdate='1419206400', enddate='1419292799') #this requries special permission. I already emailed them. 
