import urllib2
import datetime
import re
from bs4 import BeautifulSoup
from bs4 import Tag
from slacker import Slacker

# credentials file not in git
import credentials

# today's date
date = datetime.datetime.today().strftime('%-m/%d/%Y')
validDay = "Mon\.|Tue\.|Wed\.|Thu(r)?(s)?\.|Fri\."
website = "http://www.texassports.com/schedule.aspx?path=baseball"

opener = urllib2.build_opener()
##add headers that make it look like I'm a browser
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
page = opener.open(website)
# turn page into html object
soup = BeautifulSoup(page, 'html.parser')
#print soup.prettify()

#get all home games
all_rows = soup.find_all('tr', class_='schedule_home_tr')

# see if any game is today
entryForToday = [t for t in all_rows if t.findAll('nobr',text=re.compile('.*({}).*'.format(date)))]

# hard coding for testing weekend
# entryForToday = [t for t in all_rows if t.findAll('nobr',text=re.compile('3/14/2017'))]

classForTime = "schedule_dgrd_time/result"
timeOfGame = "none";

if entryForToday:
    entryForToday = [t for t in entryForToday if t.findAll('td',
                                                            class_='schedule_dgrd_game_day_of_week',
                                                            text=re.compile('.*({}).*'.format(validDay)))]
    for elements in entryForToday:
        for element in elements:

            if isinstance(element, Tag):
                if element.attrs['class'][0] == classForTime:
                    timeOfGame = element.text
                    break

#send to slack channel
if timeOfGame == "none":
    message = "There is no game today!"
else:
    message = 'There\'s a game today that starts at ' + timeOfGame
slack = Slacker(credentials.slackAPIToken)
slack.chat.post_message(credentials.user, message)
