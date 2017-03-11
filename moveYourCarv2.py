import urllib2
import datetime
import re
from bs4 import BeautifulSoup

# today's date
date = datetime.datetime.today().strftime('%-m/%d/%Y')
validDay = "Mon\.|Tue\.|Wed\.|Thu(r)?(s)?\.|Fri\."
website = "http://www.texassports.com/schedule.aspx?path=baseball"

opener = urllib2.build_opener()
##add headers that make it look like I'm a browser
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
page = opener.open(website)
# turn page into html object
soup = BeautifulSoup(page)
#print soup.prettify()

#get all home games
all_rows = soup.find_all('tr', class_='schedule_home_tr')

# see if any game is today
entryForToday = [t for t in all_rows if t.findAll('nobr',text=re.compile('.*({}).*'.format(date)))]

# testing weekend
# entryForToday = [t for t in all_rows if t.findAll('nobr',text=re.compile('3/11/2017'))]

# print entryForToday
if entryForToday:
    entryIsWeekday = [t for t in entryForToday if t.findAll('td',
                                                            class_='schedule_dgrd_game_day_of_week',
                                                            text=re.compile('.*({}).*'.format(validDay)))]
    if entryIsWeekday:
        print 'entryIsWeekday'
        myClass = 'schedule_dgrd_time/result'
        timeOfGame = entryIsWeekday[0].contents[4]
        text = timeOfGame.content
        print timeOfGame

    else:
        print 'not weekday'