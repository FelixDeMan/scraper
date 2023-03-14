import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import argparse


parser = argparse.ArgumentParser(description='Download product images from Hugo Boss website.')
parser.add_argument('--url', type=str, default='https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-ka-toen-met-logostiksel/hbeu50466684_260.html?cgid=21000',
                    help='URL of the product page to download images from')
parser.add_argument('--filename', type=str, default='https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-ka-toen-met-logostiksel/hbeu50466684_260.html?cgid=21000',
                    help='URL of the product page to download images from')
args = parser.parse_args()

def scrape_category_page(txtfile, url):
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", options=options)

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    real_product_urls = []

    # Time to manually Click accept cookies button
    time.sleep(5)

    #find if there is a next page
    next_page = driver.find_element(By.CSS_SELECTOR, "a.button.button--pagingbar.pagingbar__next.font--button")

    while next_page is not None:
        #Find all links to products, per category
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_urls = soup.find_all("a", {"class" : "js-product-tile__product-image widget-initialized"})
        for i, product_url in enumerate(product_urls):
            real_url = url.split(".com")[0]+(".com")+product_url["data-url"]
            if real_url not in real_product_urls:
                real_product_urls.append(real_url)
            else:
                print("Duplicate found: {}".format(real_url))
            #print(product_urls[i])
        
        next_page.click()
        print("Amount of urls: {}".format(len(real_product_urls)))
        #print(real_product_urls[0])
        #print(real_product_urls[0:10])
        #print(real_product_urls[-10:-1])
        print("clicked next page!")
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "a.button.button--pagingbar.pagingbar__next.font--button")
        except:
            next_page = None
            print("No more next pages!")

    with open(txtfile, 'w') as f:
        for real_url in real_product_urls:
            f.write("%s\n" % real_url)
    print("Done, urls written to {}".format(txtfile))
    driver.quit()

if __name__=="__main__":
    
    scrape_category_page(args.category_filename, args.url)

