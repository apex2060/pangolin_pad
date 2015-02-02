#!/usr/bin/python

# Elite:Dangerous Data Network client
# Dowloads data from community stream & filters out market prices by station

import zlib
import zmq.green as zmq
import simplejson
import sys

import time
import datetime
import pickle
import os

filepath = '/home/pi/Programs/elite/DATA/'
rawFile = '%sraw_data.dat' % filepath   # Hold raw json download

def fetch():
# Download json data
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.setsockopt(zmq.SUBSCRIBE, "")
    subscriber.connect('tcp://eddn-relay.elite-markets.net:9500')

    market_json = zlib.decompress(subscriber.recv())
    market_data = simplejson.loads(market_json)
    #print market_data
    save(data, rawFile) # Not sure of the format this is saved in. May be possible to splitlines?
    sys.stdout.flush()

def timestamp():
    timeNow = datetime.datetime.now()
    formatTime = timeNow.strftime('%H:%M')
    return formatTime

def save(data, filename):
# Save data to file for later use
    save_file = open(filename, 'wb')
    pickle.dump(data, save_file)
    save_file.close()

def load(filename):
# Load data from file
    load_file = open(filename, 'rb')
    data = pickle.load(load_file)
    save_file.close()
    return data

def extract():
    # Extract only market data from download
    raw_data = load(rawFile)
    marketExtract = []
    for a in b: # Need to loop through entries in the raw_data file. Split lines may be possible
        if raw_data['$schemaRef'] == "http://schemas.elite-markets.net/eddn/commodity/1"
        marketExtract.append(raw_data)
    return marketExtract

def filter(station):
    # Present data for specified station
    allMarkets = extract()
    stationData ={}
    # String manipulation process to check stationName = station
    for market in allMarkets:
            message = market["message"]
            if message["stationName"] == station:
                salesData = [message["buyPrice"], message["sellPrice"], message["demand"]]
                stationData{message["itemName"]: salesData}
    # stationName is in Title Case while station is UPPERCASE. How to fix this?
    return stationData # A dictionary of market data in the format: {prouct: [buy, sell, galacticAve, supply/demnd]} 

def mainMenu():
    loop = True
        print """ 
==============================
 ELITE:DANGEROUS DATA NETWORK
==============================
 Downloading Market Data...
------------------------------"""

    fetch() # Download latest data
    updateTime = timestamp() # Record time of last update

    while loop:
        os.system('clear')
        print """ 
==============================
 ELITE:DANGEROUS DATA NETWORK
==============================
 Main Menu      Updated: %s     
------------------------------
 1 > Select Station
 2 > Refresh Data""" % updateTime
        selection = raw_input('   > ')

# DISPLAY DATA
        if selection == '1':
            os.system('clear')
            # Take station name & display associated data
            print """ 
==============================
 ELITE:DANGEROUS DATA NETWORK
==============================
 Station Data   Updated: %s     
------------------------------""" % updateTime
            station = raw_input('Station: ')
            station = station.upper()

            try:
                market = filter(station)
                print """ 
ITEM        BUY     SELL    AVE     SUP/DEM"""
                for item, info in market.iteritems():
                print """ 
%s          %s      %s      %s      %s""" % (items, info[0], info[1], info[2], info[3])
            except:
                print 'Invalid station, please try again'
            proceed = raw_input('Press enter to continue') # Wait for user input to clear screen

# RE-DOWNLOAD DATA        
        elif selection == '2':
            os.system('clear')
            print """ 
==============================
 ELITE:DANGEROUS DATA NETWORK
==============================
 Downloading Market Data...
------------------------------"""

            fetch() # Download latest data
            updateTime = timestamp() # Record time of last update

# INVALID SELECTION        
        else:
            print 'Invalid selection, please try again.'

        time.sleep(1) # Regulate loop speed

if __name__ == '__main__':
    mainMenu()
