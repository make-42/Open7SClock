import web.bitcoin

import tm1637
import time
import datetime

# init
tm_year = tm1637.TM1637(clk=11, dio=12) # GPIO 0 AND 1
tm_date = tm1637.TM1637(clk=13, dio=15) # GPIO 2 AND 3
tm_time = tm1637.TM1637(clk=16, dio=18) # GPIO 4 AND 5

# Define functions
# Update time
def update(year, day, month, hour, minute):
    tm_year.number(year)
    tm_date.numbers(day,month)
    tm_time.numbers(hour,minute)

#Update bitcoin price
def updatebtc(price, currency):
    pricestring = str(price)[:8].replace('.', '-')
    tm_year.write([0b01111100, 0b01111000, 0b01011000, 0b00000000])
    tm_date.show(pricestring[:4])
    tm_time.show(pricestring[5:3]+currency)
    print("btc",pricestring+currency)

while 1:
    # Clock
    now = datetime.datetime.now()
    update(now.year, now.day, now.month, now.hour, now.minute)
    print(now.year, now.day, now.month, now.hour, now.minute)
    time.sleep(5)
    # Bitcoin price
    updatebtc(web.bitcoin.geteuroprice(),"E")
