from adafruit_ht16k33 import segments
import datetime
import board
import busio
import time

# User variables
version = "1.01"
addresses = [0x00,0x01,0x02,0x03,0x04]

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
print("3 ", end="")
tm_c = segments.Seg14x4(i2c, address=addresses[2]) # Address 2
print("4 ", end="")
tm_d = segments.Seg14x4(i2c, address=addresses[3]) # Address 3
print("5 ", end="")
tm_e = segments.Seg14x4(i2c, address=addresses[4]) # Address 4
print("Done.")

# Define functions.
# Define "split text between displays" function.
def printodisplays(stringtoprint):
    tm_a.print(stringtoprint[:4])
    tm_b.print(stringtoprint[4:8])
    tm_c.print(stringtoprint[8:12])
    tm_d.print(stringtoprint[12:16])
    tm_e.print(stringtoprint[16:20])
# Define "update time" function.
def updatetime(datetimeobject):
    datetimeobjectstr = datetimeobject.strftime("%Y-%m-%d  %H:%M:%S") # ISO 8601 Standard
    printodisplays(datetimeobjectstr)
# Define "update bitcoin price" function.
def updatebtc(price, currency):
    pricestring = str(price)
    printodisplays("Bitcoin: "+pricestring+currency)

# Display loading text.
print("Displaying startup text...")
printodisplays("[Open7SClock, xE0F9]")
time.sleep(1)
printodisplays("[[  Silicon v"+version+"  ]]")
time.sleep(1)


oldseconds = 99
# Start main program loop
while 1:
    now = datetime.datetime.now()
    if now.seconds != oldseconds:
        updatetime(now)
        oldseconds = now.seconds
    time.sleep(0.2)
