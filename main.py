import tm1637
import time
import datetime

# init
tm_year = tm1637.TM1637(clk=11, dio=12) # GPIO 0 AND 1
tm_date = tm1637.TM1637(clk=13, dio=15) # GPIO 2 AND 3
tm_time = tm1637.TM1637(clk=16, dio=18) # GPIO 4 AND 5

# Define functions
def update(year, day, month, hour, minute):
    tm_year.number(year)
    tm_date.numbers(day,month)
    tm_time.numbers(hour,minute)

# Sample text
tm_year.show('   x')
tm_date.show('E0F9')
tm_time.write([0, 0, 0, 0])
time.sleep(1)

oldminute = 60

while 1:
    now = datetime.datetime.now()
    if now.minute != oldminute:
        update(now.year, now.day, now.month, now.hour, now.minute)
        oldminute = now.minute
	time.sleep(0.5)




