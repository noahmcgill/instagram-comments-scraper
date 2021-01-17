#! /usr/bin/env python

from bs4 import BeautifulSoup
from csv import DictWriter
from datetime import datetime
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from sys import argv
import time

# Scraping functions

class Scrape:
    
    def __init__(self, s):
        self.soup = BeautifulSoup(s, 'lxml')
    
    def get_user(self):
        user = self.soup.find('a', {'class': 'ZIAjV'}).text
        return user

    def get_comment(self):
        find_span = self.soup.find_all('span')

        if len(find_span) == 2:
            comment_text = find_span[1].text
        else:
            comment_text = find_span[0].text
        
        return comment_text
    
    def get_datetime(self):
        dt = self.soup.find('time')['datetime']
        return dt
    
    def get_likes(self):
        likes = self.soup.find_all('button', {'class':'FH9sR'})[0].text

        if likes == 'Reply':
            num_likes = '0'
        else:
            num_likes = likes.split(' ')[0]
        
        return num_likes
    
# Selenium initialization

DRIVER_PATH = '/chromedriver' # CHANGE ME

chrome_options = Options()

chrome_options.add_argument('--disable-gpu')

chrome_options.add_argument('--headless')

chrome_options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

# Navigate to the post

POST_URL = argv[1]
driver.get(POST_URL)

# Parse additional args

if len(argv) == 5:
    try:
        specified_range = argv[2]
        specified_dt = argv[3] + ' ' + argv[4]
        specified_dt_convert = datetime.strptime(specified_dt, '%m/%d/%Y %H:%M')
        dt_specified = True
    except:
        dt_specified = False
        print('There was an error processing your datetime request. We\'ll pull all comments on this post, instead.')
else:
    dt_specified = False

# Dismiss login option

try:
    driver.find_element_by_class_name('xqRnw').send_keys(Keys.RETURN)
except:
    pass

time.sleep(1.5)

# Show all comments on the post

while True:
    try:
        driver.find_element_by_class_name('afkep').send_keys(Keys.RETURN)
        time.sleep(1.5)
    except:
        break

data = []

# Perform scrape

try:
    comments = driver.find_elements_by_class_name('C4VMK')
    for comment in comments:
        current = Scrape(comment.get_attribute('innerHTML'))

        # Convert datetime
        dt_convert = datetime.strptime(current.get_datetime(), '%Y-%m-%dT%H:%M:%S.%fZ')

        def appendData():
            data.append({'Datetime': dt_convert, 'User': current.get_user(), 'Comment': current.get_comment(), 'Likes': current.get_likes()})

        # Pass over comment if out of range if range is given, and append within-range comments
        if dt_specified:
            if specified_range == 'before':
                if dt_convert <= specified_dt_convert:
                    try:
                        appendData()
                    except:
                        pass
                else:
                    pass
            elif specified_range == 'after':
                if dt_convert >= specified_dt_convert:
                    try:
                        appendData()
                    except:
                        pass
                else:
                    pass
        else:
            try:
                appendData()
            except:
                pass
except:
    print('There was an error. Please try again.')

# Export to CSV

try:
    with open('comments.csv', 'w', encoding='utf-8-sig') as f:
        writer = DictWriter(f, fieldnames=['Datetime', 'User', 'Comment', 'Likes'])
        writer.writeheader()
        writer.writerows(data)
        print('Scrape complete. ' + str(len(data)) + ' comments exported to CSV.')
except:
    print('There was an error writing the comments to a CSV. It could be that no comments were found.')

# Close window

driver.close()