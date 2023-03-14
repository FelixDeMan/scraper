from boss_image_scraper import scrape_txtfile
from boss_url_scraper import scrape_category_page
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Download product images from Hugo Boss website.')
    parser.add_argument('--url', type=str, default='https://www.hugoboss.com/nl/regular-fit-trui-van-zuivere-ka-toen-met-logostiksel/hbeu50466684_260.html?cgid=21000',
                    help='URL of the product page to download images from')
    parser.add_argument('--filename', type=str, default='category.txt',
                    help='filename for text output, should contain category.txt') 
    option, unknown = parser.parse_known_args() 
    print(option)

    scrape_category_page(option.filename, option.url)
    scrape_txtfile(option.filename)
    print("DONE!")