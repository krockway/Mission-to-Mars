#Webdriver manager wouldn't load in the next cell, this is a work around
import sys
get_ipython().system('pip install webdriver_manager')

# Import Splinter and BeautifulSoup & Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#Search for this specific tag (div) & attribute (list_text) & wait 1 sec to make sure page loads fully

#Parse info
html = browser.html
news_soup = soup(html, 'html.parser')
#Return the first thing that matches (ie on news page, the newest article)
slide_elem = news_soup.select_one('div.list_text')

#Scrape the title
slide_elem.find('div', class_ ='content_title')
#slide_elem holds a ton of info, find divs where the class is "content_title"

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#This gets rid of the code <> in the above ouput

#Scrape the summary text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button (2nd button on the page)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#.get(src) pulls the link

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# ### Create table

#Create DF to read the facts table html
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#Send the DF to HTML page
df.to_html()

#Shut down the automated browsers
browser.quit()

