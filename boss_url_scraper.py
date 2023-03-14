import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import argparse

def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    print('/%s' % '/'.join(components))
    return '/%s' % '/'.join(components)


parser = argparse.ArgumentParser(description='Download product images from Hugo Boss website.')
parser.add_argument('--url', type=str, default='https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-ka-toen-met-logostiksel/hbeu50466684_260.html?cgid=21000',
                    help='URL of the product page to download images from')
parser.add_argument('--category', type=str, default='https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-ka-toen-met-logostiksel/hbeu50466684_260.html?cgid=21000',
                    help='URL of the product page to download images from')
args = parser.parse_args()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=r"C:\Users\Jan-FelixdeMan\Downloads\chromedriver_110\chromedriver.exe", options=options)

# Launch the browser and open the given url in the webdriver
url = args.url
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
txtfile = args.category+"_urls.txt"
with open(txtfile, 'w') as f:
    for real_url in real_product_urls:
        f.write("%s\n" % real_url)
print("Done, urls written to{}".format(txtfile))
#print(product_urls[0])
#image_tags = soup.find_all("img",{"class" :"pdp-images__adaptive-picture-image"})