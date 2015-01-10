__author__ = 'DuthoitA'
#### Modification History ####
# 8/1 Tidy up and prepare for continual running
# 10/1 Improve error handling and load PrevObsdate from database
##############################

import urllib.request
from pymongo import *
import json
import time
from datetime import datetime
#
#Init
PrevObsTime = 0
x = 1
#
# Open Database
try:
    c = Connection(host="localhost", port=27017)
except:
    print('Could not connect to MongoDB')
    exit()
dbname=c["db"]
assert dbname.connection == c
Weather = dbname.weather
#
# Get last record so we can set previous observation time
DataCursor=Weather.find({}, {"Observation Time": 1}).sort('_id', DESCENDING).limit(1)
PrevObsTime = DataCursor[0]["Observation Time"]

# Main control loop
while x > 0:   # loop forover or unitil program sets x on
    try:
        response = urllib.request.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3761?res=hourly&key=d0b6d22a-e25b-4e0d-82bc-ecb57f75ea45')
    except:
        print("Error on read from Met Office")
    else:
        FCData = response.read()
        FCDataStr = FCData.decode('utf-8')
        FCData_Dic = json.loads(FCDataStr)

        # Unpack data
        SiteRep = (FCData_Dic['SiteRep'])
        Wx = (SiteRep['Wx'])
        Param = (Wx['Param'])
        DV = (SiteRep['DV'])
        Location = (DV['Location'])
        Period = (Location['Period'])
        ObsDate = Period[1]
        Value = (Period[0])
        Rep = (Value['Rep'])
        ObsComplete = (Rep[0])
        WeatherType = int(Rep[0]['W'])
        Visibility = int(Rep[0]['V'])
        Temperature = float(Rep[0]['T'])
        WindSpeed = int(Rep[0]['S'])
        WindDir = (Rep[0]['D'])
        DewPoint = (Rep[0]['Dp'])
        ObsTime = int(Rep[0]['$'])

        # Check if Observation has changed
        if ObsTime != PrevObsTime:

            Dataout={"Location": Location['name'],
                     "ObsDate": ObsDate['value'],
                  "WeatherType": WeatherType,
                  "Observation Time":ObsTime/60,
                     "Visibility": Visibility,
                     "Temperature": Temperature,
                     "WindSpeed=": WindSpeed,
                     "WindDir": WindDir,
                     "DewPoint": DewPoint,
                  }

            post_id = Weather.insert(Dataout)
            print(post_id, Dataout)
        else:
            print("Same time", ObsTime/60, datetime.now().time())

        PrevObsTime = ObsTime

    #
    # pause for a minute
        time.sleep(60)
