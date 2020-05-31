import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta

url = "https://www.forexfactory.com/calendar?day=mar24.2020"

def get_week_result(url, input_text="USD"):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tb_rows = soup.find_all('tr', class_='calendar__row')
    final = []
    i = 0
    for row in tb_rows:
        x = []
        # print(row.find('span', class_='worse'))
        if row.find('td', class_='calendar__cell calendar__actual actual'):
            span = row.find('td', class_='actual')
            if span.find('span', class_='worse'):
                if row.find('td', class_='calendar__cell calendar__currency currency'):
                    i += 1
                    x.append(i)
                    x.append((row.find('td', class_='calendar__cell calendar__currency currency').text[1:4]))
                    x.append("bullish")
                    
                    date_ = row.find('td', class_='calendar__cell calendar__date date').find('span', class_='date')
                    if date_ != None:
                        date = date_
                    x.append(date.find().text[:])
                    
                    final.append(x)

            elif span.find('span', class_='better'):
                if row.find('td', class_='calendar__cell calendar__currency currency'):
                    i += 1
                    x.append(i)
                    x.append((row.find('td', class_='calendar__cell calendar__currency currency').text[1:4]))
                    x.append("bearish")
                    
                    date_ = row.find('td', class_='calendar__cell calendar__date date').find('span', class_='date')
                    if date_ != None:
                        date = date_
                    x.append(date.find().text[:])
                    
                    final.append(x)
                    
            else:
                if row.find('td', class_='calendar__cell calendar__currency currency'):
                    i += 1
                    x.append(i)
                    x.append((row.find('td', class_='calendar__cell calendar__currency currency').text[1:4]))
                    x.append("neutral")
                    
                    date_ = row.find('td', class_='calendar__cell calendar__date date').find('span', class_='date')
                    if date_ != None:
                        date = date_
                    x.append(date.find().text[:])
                    
                    final.append(x)
                    
# input_text = input("Input the Currency (Ex:- NZD, USD, JPY, AUD, JPY) : ")
    return final



input_text = input("Input the Currency (Ex:- NZD, USD, JPY, AUD, JPY) : ")
print("\n")

final_last = get_week_result("https://www.forexfactory.com/calendar?week=last", input_text)
final_this = get_week_result("https://www.forexfactory.com/calendar?week=this", input_text)

final_last
final_this
two_weeks_final = final_last + final_this

weekday = datetime.datetime.today().weekday()

today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)
week_ago_ = str(week_ago)
today_ = str(today)

print("Today is            : {:s}".format(today_))
# print("Day of the Week     : {:d}".format(weekday + 2))
print("This will give from : {:s} to {:s} \n".format(week_ago_, today_))

week = []

delta = today - week_ago       # as timedelta

for i in range(delta.days + 1):
    day = week_ago + timedelta(days=i)
    day = day.strftime("%b %d")
    week.append(str(day))
    
print("Dates Scrapped:", week[:-1])
# print(len(week[:-1]))
# week = week[:-1]
# week

weeks_final = []
for i in week:
    for j in two_weeks_final:
        if j[3] == i:
            weeks_final.append(j)

final = weeks_final

# print (final)

currency_events = []
for i in final:
    if(i[1]==input_text):
        currency_events.append(i[2])
# print (currency_events)

print ()
print ("Calculating output for " + input_text + " In past week" + "\n")

print("These are the {:d} events from past week in https://www.forexfactory.com \n".format(len(currency_events)))

output = 0
bearish = 0
bullish = 0
neutral = 0

for i in range(len(currency_events)):
    x = "event " + str(i+1) + " = "
    if(currency_events[i]=="bullish"):
        y = "actual > forecast = bullish = 1"
        output += 1
        bullish += 1
    if(currency_events[i]=="bearish"):
        y = "actual < forecast = bearish = -1"
        output -= 1
        bearish -= 1
    if(currency_events[i]=="neutral"):
        y = "actual = forecast = neutral = 0"
        neutral += 1
    print (x+y)

# final ouput 
print("\n")
print("Events Count : \n")
print("Bearish Event Count    : {:d}".format( -bearish))
print("Bullish Event Count    : {:d}".format( bullish))
print("Neutral Event Count    : {:d}".format( neutral))
print("Total Number of Events : {:d}".format( -bearish + bullish + neutral))
print("\n")
print("Events Value : \n")
print("Bearish Event value :   {:d} x -1   =  {:d} ".format(-bearish, bearish))
print("Bullish Event value :  +{:d} x  1   =   {:d}".format( bullish, bullish))
print("Neutral Event value :   {:d} x  0  =   0".format( neutral))
print("Total Event Value   :           =   {:d}".format(output))

print("\n")
print("Given Currency                : {:s}".format(input_text))
print("Output value of the past week : {:f}".format(output/len(currency_events)))
