# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
response = browser.is_element_present_by_css('div.list_text', wait_time=1)
fails = 0
while response == False:
    fails += 1
    if fails > 9:
        #print("Failed too many times quitting browser to try again.")
        browser.quit()
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        fails = 0
        response = browser.is_element_present_by_css(
            'div.list_text', wait_time=1)
    else:
        #print(f"Failed to get proper server response {fails} times, trying again.")
        browser.visit(url)
        response = browser.is_element_present_by_css(
            'div.list_text', wait_time=1)
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
# img_soup
# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel
# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
# img_url
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#df.head()
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
# df
df.to_html()
# 1. Use browser to visit the URL
url = 'https://marshemispheres.com/'
browser.visit(url)
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisoup = soup(html, 'html.parser')
#hemisoup
hemis = hemisoup.find('div', class_='collapsible results')
# I wanted to see if adding "_all" to find would work and it did. AND IT MADE A LIST WOOOOOOOO!
helement = hemis.find_all('a', class_='itemLink product-item')
for hemi in helement:
    lonk = hemi.get("href")
    link = url + lonk
    browser.visit(link)
    html = browser.html
    forsoup = soup(html, 'html.parser')
    imglonk = forsoup.find('img', class_='wide-image').get('src')
    imglink = url + imglonk
    # It took me an hour to realize I could use ".text" to retrieve text. Very neat.
    titl = forsoup.find('div', class_='cover').find('h2', class_='title').text
    hemisphere = {}
    hemisphere = {'img_url': imglink, 'title': titl}
    if hemisphere not in hemisphere_image_urls:
        hemisphere_image_urls.append(hemisphere)
browser.quit()