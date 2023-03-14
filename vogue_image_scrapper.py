
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from requests_html import HTMLSession
import os
from urllib.parse import urlparse
import mimetypes

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument(
#"user-data-dir=C:\\Users\\MohibullahMansoorVir\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", chrome_options=options)

# Launch the browser and open the given url in the webdriver
site = 'https://www.vogue.com/fashion-shows/fall-2022-ready-to-wear/hugo-boss' #Change the website
driver.get(site) 
session = HTMLSession()
r = session.get(site)
soup = BeautifulSoup(driver.page_source, 'html.parser')

##Loop for smooth scrolling down the page
total_height = int(driver.execute_script("return document.body.scrollHeight"))
for i in range(1, total_height, 30): #Please change the number "5" to adjust the scrolling speed
    driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(0.1)


image_tags = soup.find_all("img",{"class" :"ResponsiveImageContainer-dmlCKO hWKgYV responsive-image__image","alt" : ""}) #vogue

urls = [img.get('src') for img in image_tags]
print(urls)

for url in urls:
    maintype= mimetypes.guess_type(urlparse(url).path)[0]
    if maintype not in ('image/png', 'image/jpeg', 'image/gif','image/jpg','image/svg'):
         url = url + '.jpg'
    filename = re.search(r'([\w|.|+|,|=|?|$|&_-]+[.](jpg|gif|png|svg|jpeg))', url) #vogue
    filename_2 = re.sub("[/?=,$&]","_",filename.group()) #for the rest except s.Oliver
    if len (filename_2) > 100:
        filename_2  = filename_2[(len(filename_2)) - 100 :]
    with open(filename_2, 'wb') as f:
        if 'http' not in url:
            url = '{}{}'.format(site, url)
        r = session.get(url)    
        f.write(r.content)


print("Download complete, downloaded images can be found in current directory!")
driver.quit()

