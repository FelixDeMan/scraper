import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import argparse
import time


parser = argparse.ArgumentParser(description='Download product images from Hugo Boss website.')
parser.add_argument('--url', type=str, default=None,
                    help='URL of the product page to download images from')
parser.add_argument('--filename', type= str, default = None,
                    help='File with URLs of the product pages to download images from')
args = parser.parse_args()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def scrape_product_page(url):
    driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", chrome_options=options)
    # Launch the browser and open the given url in the webdriver
    url = args.url
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all image tags with class "pdp-images__adaptive-picture-image"
    image_tags = soup.find_all("img",{"class" :"pdp-images__adaptive-picture-image"})
    savedir = soup.find("h1", {"class":"pdp-stage__header-title font--h5 font--h4-m"}).get_text()
    print(type(savedir))
    savedir = savedir.replace(" ", "_").replace("\n", "").replace("'", "")
    print(savedir)
    category = soup.find_all("span", {"class":"breadcrumb__title--small"})[-1].get_text()
    category = category.replace("\n", "").replace("'", "")
    print(category)
    save_dir = f"./Hugo_Boss/{category}/{savedir}"
    # Create a folder to save the images
    #save_dir = "./Hugo_Boss/"+args.save_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Loop through the image tags and download each image
    for i, image_tag in enumerate(image_tags):
        image_url = image_tag['src']
        response = requests.get(image_url)
        image_name = f'{save_dir}/product_image_{i+1}.jpg'
        with open(image_name, 'wb') as f:
            f.write(response.content)
            print(f'Saved {image_name}')

    # Quit the ChromeDriver
    driver.quit()

def scrape_txtfile(filename):
    filename = args.filename
    #read urls from filename in a list without \n 
    with open(filename, 'r') as f:
        urls = f.read().splitlines()
    print(urls)

    driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", chrome_options=options)
    for url in urls:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Find all image tags with class "pdp-images__adaptive-picture-image"
        image_tags = soup.find_all("img",{"class" :"pdp-images__adaptive-picture-image"})
        savedir = soup.find("h1", {"class":"pdp-stage__header-title font--h5 font--h4-m"}).get_text()
        print(type(savedir))
        savedir = savedir.replace(" ", "_").replace("\n", "").replace("'", "")
        print(savedir)
        category = soup.find_all("span", {"class":"breadcrumb__title--small"})[-1].get_text()
        category = category.replace("\n", "").replace("'", "")
        print(category)
        save_dir = f"./Hugo_Boss/{category}/{savedir}"
        # Create a folder to save the images
        #save_dir = "./Hugo_Boss/"+args.save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Loop through the image tags and download each image
        for i, image_tag in enumerate(image_tags):
            image_url = image_tag['src']
            response = requests.get(image_url)
            image_name = f'{save_dir}/product_image_{i+1}.jpg'
            with open(image_name, 'wb') as f:
                f.write(response.content)
                print(f'Saved {image_name}')

    # Quit the ChromeDriver
    driver.quit()

if __name__ == "__main__":

    if args.url is not None:
        print("Scraping product page...")
        url = args.url
        scrape_product_page(url)

    
    elif args.filename is not None:
        print("Scraping product pages from file...")
        filename = args.filename
        scrape_txtfile(filename)
