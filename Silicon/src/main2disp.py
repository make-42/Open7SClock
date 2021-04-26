from adafruit_ht16k33 import segments
import datetime
import board
import busio
import time
import math

# User variables
version = "1.01"
addresses = [0x71,0x72]
ip = "192.168.1.56"
# Initialise program.
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
# Define "split text between displays" function.
def printodisplays(stringtoprint):
    tm_a.print(stringtoprint[:4])
    tm_b.print(stringtoprint[4:8])

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
    if statecounter == 200:
        statecounter = 0
        ping()
    else:
        now = datetime.datetime.now()
        sep = math.floor(time.time()*2)%2
        updatetime(now,sep)
    time.sleep(0.05)
    statecounter = statecounter+1
