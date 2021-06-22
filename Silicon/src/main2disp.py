from adafruit_ht16k33 import segments
import datetime
from time import localtime, timezone, time
import board
import busio
import time
import math
import os
import json
import requests
import subprocess

# User variables
version = "1.01"
addresses = [0x72,0x71]
ip = "192.168.1.56"
mprisEnabled=True
# Initialise program.
# Start mpris webserver.
if mprisEnabled:
    print("Starting MPRIS² WebServer ", end="")
    subprocess.Popen(["python3","mprisserver.py"])
    print("Done.")
# Create the I2C interface.
print("Starting I²C interface... ", end="")
i2c = busio.I2C(board.SCL, board.SDA)
print("Done.")
# Initialise displays.
print("Initialising displays: ", end="")
print("1 ", end="")
tm_a = segments.Seg14x4(i2c, address=addresses[0]) # Address 0
print("2 ", end="")
tm_b = segments.Seg14x4(i2c, address=addresses[1]) # Address 1
print("Done.")

# Define functions.

# Define "internet time" function.

def itime():
    """Calculate and return Swatch Internet Time

    :returns: No. of beats (Swatch Internet Time)
    :rtype: float
    """
    currtime = time.time()
    h, m, s = localtime()[3:6]
    beats = ((h * 3600) + (m * 60) + s + (currtime-math.floor(currtime)) + timezone) / 86.4

    if beats > 1000:
        beats -= 1000
    elif beats < 0:
        beats += 1000

    return beats

# Define "split text between displays" function.
def printodisplays(stringtoprint):
    try:
        tm_a.print(stringtoprint[:4])
        tm_b.print(stringtoprint[4:8])
    except:
        printodisplays(stringtoprint)
# Define "update time" function.
def updatetime(datetimeobject, seperation):
    if seperation:
        datetimeobjectstr = datetimeobject.strftime("%H:%M:%S") # ISO 8601 Standard
    else:
        datetimeobjectstr = datetimeobject.strftime("%H %M %S") # ISO 8601 Standard
    printodisplays(datetimeobjectstr)
# Define "ping" function.
def ping():
    pcstate = os.system(f"ping -c 1 -w2 {ip} > /dev/null 2>&1") == 0
    printodisplays("PC is  ")
    time.sleep(1)
    if pcstate:
        printodisplays("Online ")
    else:
        printodisplays("Offline")
    time.sleep(1)

# Define "update bitcoin price" function.
def updatebtc(price, currency):
    pricestring = str(price)
    printodisplays("Bitcoin: "+pricestring+currency)

# Display loading text.
print("Displaying startup text...")
printodisplays("-[xE0F9]")
time.sleep(1)
printodisplays("-Silicon")
time.sleep(1)


oldseconds = 99
statecounter = 0
# Start main program loop
while 1:
    if statecounter >= 200:
        if statecounter < 400:
            printodisplays("@{0:0.3f}".format(itime()).replace(".","-"))
    if statecounter >= 400:
        if mprisEnabled:
            r = requests.get("http://127.0.0.1:4215/")
            rjson = json.loads(json.loads(r.content.decode("utf-8")).replace("\'","\""))
            mpristext = str(rjson['artist']).replace("\\n","")+" - "+str(rjson['title']).replace("\\n","")
            for x in range(len(mpristext)-8):
               printodisplays(mpristext[0+x:8+x])
               time.sleep(0.3)
            time.sleep(0.5)
        statecounter = 0
    if statecounter < 200:
        now = datetime.datetime.now()
        sep = math.floor(time.time()*2)%2
        updatetime(now,sep)
    time.sleep(0.05)
    statecounter = statecounter+1
