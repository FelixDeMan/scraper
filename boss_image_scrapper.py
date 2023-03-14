
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
import wget

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument(
#"user-data-dir=C:\\Users\\MohibullahMansoorVir\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", chrome_options=options)

# Launch the browser and open the given url in the webdriver
site = 'https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-katoen-met-logostiksel/hbeu50466684_260.html?cgid=21000' #Change the website
driver.get(site) 
session = HTMLSession()
r = session.get(site)
soup = BeautifulSoup(driver.page_source, 'html.parser')

##Loop for smooth scrolling down the page
time.sleep(5)
total_height = int(driver.execute_script("return document.body.scrollHeight"))
for i in range(1, total_height, 30): #Please change the number "5" to adjust the scrolling speed
    driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(0.01)


image_tags = soup.find_all("img",{"class" :"pdp-images__adaptive-picture-image"}) #vogue

urls = [img.get('src') for img in image_tags]

save_dir = "./Hugo_Boss/orange_sweater"

os.makedirs(save_dir, exist_ok= True)

for i, url in enumerate(urls):
    wget.download(url, out="{}/{}.jpg".format(save_dir, i))
    # maintype= mimetypes.guess_type(urlparse(url).path, strict=False)[0]
    # print(maintype)
    # #if maintype not in ('image/png', 'image/jpeg', 'image/gif','image/jpg','image/svg', 'image/webp'):
    # #     url = url + '.jpg'
    # #     print(url)
    # filename = re.search(r'([\w|.|+|,|=|?|$|&_-]+[.](jpg|gif|png|svg|jpeg))', url) #vogue
    # filename_2 = re.sub("[/?=,$&]","_",filename.group()) #for the rest except s.Oliver
    # if len (filename_2) > 100:
    #     filename_2  = filename_2[(len(filename_2)) - 100 :]
    # with open(filename_2+'.jpg', 'wb') as f:
    #     if 'http' not in url:
    #         url = '{}{}'.format(site, url)
    #     r = session.get(url)    
    #     f.write(r.content)


print("Download complete, downloaded images can be found in current directory!")
driver.quit()

