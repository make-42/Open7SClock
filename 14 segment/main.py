from adafruit_ht16k33 import segments
import datetime
import board
import busio
import time



# init
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
tm_a = segments.Seg14x4(i2c, address=0x01)
tm_b = segments.Seg14x4(i2c, address=0x02)
tm_c = segments.Seg14x4(i2c, address=0x03)
tm_d = segments.Seg14x4(i2c, address=0x04)
tm_e = segments.Seg14x4(i2c, address=0x05)

def printodisplays(stringtoprint):
    tm_a.print(stringtoprint[:4])
    tm_b.print(stringtoprint[4:8])
    tm_c.print(stringtoprint[8:12])
    tm_d.print(stringtoprint[12:16])
    tm_e.print(stringtoprint[16:20])

# Define functions
# Update time
def updatetime(datetimeobject):
    datetimeobjectstr = datetimeobject.strftime("%Y-%m-%d  %H:%M:%S") # ISO 8601 Standard
    printodisplays(datetimeobjectstr)

#Update bitcoin price
def updatebtc(price, currency):
    pricestring = str(price)
    printodisplays("Bitcoin: "+pricestring+currency)

# Sample text
printodisplays("[Open7SClock, xE0F9]")
time.sleep(1)


while 1:
    now = datetime.datetime.now()
    updatetime(now)
    time.sleep(0.2)
