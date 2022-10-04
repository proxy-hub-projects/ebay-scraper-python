from bs4 import BeautifulSoup
import json
import cloudscraper
import os

## Input from the user in the terminal
product_serach = input('Enter Product name you want to get data==>>  ')

## This will fetch the current path of this script that we will use to write the json file
current_path = os.path.dirname(os.path.realpath(__file__))
#print(current_path)

# Proxy list defined
proxy = {
    "http": "http://USERNAME:PASSWORD@IP:PORT",
    "https": "http://USERNAME:PASSWORD@IP:PORT"}

# Created the cloudscraper instance 
scraper = cloudscraper.create_scraper() 

# Testing and printing the proxy it use in this run
proxy_test = scraper.get("http://ip.seeip.org/jsonip?",proxies=proxy).text
print(proxy_test)




def ebay_serach_result_pages_result():
    ebay_listing_html = scraper.get("https://www.ebay.com/sch/i.html?_nkw="+str(product_serach),proxies=proxy).text
    soup = BeautifulSoup(ebay_listing_html)
   

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        data.append({
            'item': {'title': title, 'link': link, 'price': price},
            'condition': condition,
            'top_rated': top_rated,
            'reviews': reviews,
            'watchers_or_sold': watchers_sold,
            'buy_now_extention': exctention_buy_now,
            'delivery': {'shipping': shipping, 'location': location},
            'bids': {'count': bid_count, 'time_left': bid_time_left},
        })

    # This will print the output in the terminal if you don't want that commit this line below
    print(json.dumps(data, indent = 2, ensure_ascii = False))

    # Output the data in json file
    with open('listing.json', 'w') as file_obj:
        json.dump(data,file_obj)

if __name__ == "__main__":
    ebay_serach_result_pages_result()


