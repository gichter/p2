import requests
import re
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/how-to-be-miserable-40-strategies-you-already-use_897/index.html"


response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
tds = soup.findAll('td')
title = soup.find('h1')
description = soup.findAll('p')[3].text
number_available = re.search(r'\d+', tds[5].text).group(0) ### searching the number in the string using regex
category = soup.findAll('a')[3].text
rating = soup.findAll('p')[2] ### TODO
image_url = "http://books.toscrape.com/" + soup.findAll('img')[0]['src'][6:] ### concatenating base url and image relative url
rating = soup.find('p', {'class': 'star-rating'})['class'][1] ### Looking for the star-rating class, and extracting the second class attribute (star rating 1-5)


book = {
    "product_page_url": url,
    "universal_product_code (upc)": tds[0].text,
    "title": title.text,
    "price_including_tax": tds[3].text[1:],
    "price_excluding_tax": tds[2].text[1:],
    "number_available": number_available,
    "product_description": description,
    "category": category,
    "review_rating": rating,
    "image_url": image_url,
}



###print(book)
### print(len(tds))
### print(tds)
###