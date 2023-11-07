####        :     *temperatureApi.py      :           #
##  : Purpose: Using rPI, Libaries, GPIO, + DHT 22/ 11 Sensor. Get a very accurate Temperature/ Humidity % Reading A+
##  : Test-Part1: Was using SSH to just watch the terminal output.. But that got annoying quickly.
##  : Test-Part2: Problem was a bit harder; Because the GPIO / DHT_READ, sometimes can take 10-20 seconds
##  : Solution: Cache the data.. Takes a couple seconds on startup. But after.. it Means the API call doesn't sit there for 30-40 seconds, returning 501 randomly.
##  : Strugles: The DHT Sensor Library. Sometimes it timesout 4-10 times in a row. When not caching the data, it would update the data with Nulls, means the API call would return garbage data.
##  : Strugles-Ext: Should have used a class, but used globals instead as a stop gap. 
##  : Misc Struggle: Threading.Timers Stop after 1/2 Triggers. You need to restart the timer.
##  : Known Issue: The API call, is only providing Time for the Last refreshed. Not a full datetime value.. Things like Home Assitant can deal with it. But say, Grafana. Expects a proper datetime to plot it on a timeline.
####

#Declares / Imports
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import threading
from threading import Timer # These are not linked, can be called independantly
from threading import Thread
from datetime import datetime
from datetime import timedelta
from flask import Flask
from flask_restful import Resource, Api, reqparse

GPIO.setmode(GPIO.BCM)
sensor = Adafruit_DHT.DHT22
GPIO=4

global Retries
Retries = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Main Executed Code:

# Cache Refresh
def reData():
    global Retries
    #print(bcolors.OKCYAN + '>> Starting - ' + bcolors.WARNING + 'refresh cache...' + bcolors.ENDC)
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO)
        if humidity is not None and temperature is not None: # Success Values
            global hmdy, tmp, dt, overdue # must declare gobally when setting Values
            hmdy = humidity
            tmp = temperature
            dt = datetime.now()
            print('' + bcolors.OKCYAN + '>> Refreshed Cache!' + bcolors.ENDC)
            Retries = 0
            loop() # Restart Timer
            #break
        else:
            print(bcolors.WARNING + '>> Sensor Timeout (This is expected).. Retrying in 3 seconds.. - Retires: ' + str(Retries) + bcolors.ENDC)
            Retries += 1
            time.sleep(3)
            reData()
    except Exception as err:
        print('The issue', err)


# chkFired() Timer
def chkFired():
    try:
        #print(bcolors.WARNING + 'Threads ok?' + bcolors.ENDC + ' --->  ', threading.active_count())
        if Retries >= 5: print(bcolors.FAIL + '>> There has been more than 5 retires.. Did something fail!!?' + bcolors.ENDC)
        if dt:
            delta = datetime.now() - dt
            #print(bcolors.OKGREEN + '>> Time since last Refresh:', round(delta.total_seconds()), 'seconds', '' + bcolors.ENDC + '')
            if delta.total_seconds() >= 180: print(bcolors.WARNING + '>> That Refresh took over 2 1/2  minutes... that''s a bit slow...' + bcolors.ENDC)
    except Exception as err:
        print(err)
    finally:
        chkLoop() # When finished -> Restart chkLoop() ---- (Doesn't auto restart derp)
        #print(bcolors.BOLD + bcolors.OKGREEN + '** Woof **' + bcolors.ENDC)

# --- Timers --- #
# chkLoop() Timer
def chkLoop():
    chkT = Timer(100, chkFired) 
    try:
        chkT.start() # Start the timer
    except Exception as err:
        print(err)
    finally:
        pass

# cacheLoop() Timer
def loop():
    global t
    t = Timer(30, reData) # Refresh @30s. - Sensor fails often, 30 seconds is only if it passes. This calls: Fire Trigger => reData()
    try:
        t.start()         # Try to start Trigger ------ This might need a wait / block wait.. Maybe
    except Exception as err:
        print('Error found? ----->', err)
    finally:
        global Retries
        Retries = 0 # Reset.
        #print(bcolors.BOLD + bcolors.OKCYAN + '** Bark **' + bcolors.ENDC)

# : START -- Startup -- : #
def startup():
    global hmdy, tmp, dt, overdue
    hmdy = None
    tmp = None
    dt = datetime.now()
    print('>> STARTUP : Finished Globals')
    loop()      # Start main Refresh-Loop
    chkLoop()   # Start Monitor Checker
    print('>> STARTUP : '+ bcolors.OKCYAN + 'Loop()-Started ' + bcolors.ENDC + '')
    print('>> STARTUP : '+ bcolors.OKGREEN + 'chkLoop()-Started' + bcolors.ENDC + '')

# : END : #


######################################--   API (FLASK)   --#############################################
# -- Start Flask/ Api
app = Flask(__name__)
api = Api(app)

# -- The API Get call -- #
class DHT(Resource):
    def get(self):
        if hmdy is not None and tmp is not None:
            data = {'RefreshTime': datetime.strftime(dt, '%I:%M:%S'), 'temperature': tmp, 'humidity': hmdy}    ## Repalcing the strftime(dt, '%Y-%m-%d %H:%M:%S') Will give it a proper datetime out. Allows Grafana to work.
            return {'DHT': data}, 200 # 200 ok..
        else:
           return {'Failure': 'No Data Available'}, 503 # Giving 503 - Service Unavailable... 

# -- User Entry Point (type in browser)
api.add_resource(DHT,'/itemps')

def startAPI():
    print('-- Starting API Run Listener --')
    app.run(host="0.0.0.0")

# -- Iniit / Start Flask App
if __name__ == '__main__':
    thread = Thread(target=startAPI, args=()) ## Start the thread that is running the Flask App / API.
    thread.start()
    startup()                # Startup the backend Tasks (Not flask)
