import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import os

# os.remove('book.csv')

url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

for b in books:
    for a in b.select("h3 a"):
        print("http://books.toscrape.com/catalogue/" + a.get('href')[9:])




""" categories = soup.find('ul', {'class': 'nav-list'})

for a in categories.select("li a"):
    print("http://books.toscrape.com/" + a.get('href'))

"""
""" 
soup = BeautifulSoup(response.text, 'html.parser')
tds = soup.findAll('td')
title = soup.find('h1')
description = soup.findAll('p')[3].text
number_available = re.search(r'\d+', tds[5].text).group(0) ### searching the number in the string using regex
category = soup.findAll('a')[3].text
rating = soup.findAll('p')[2] ### TODO
image_url = "http://books.toscrape.com/" + soup.findAll('img')[0]['src'][6:] ### concatenating base url and image relative url
rating = soup.find('p', {'class': 'star-rating'})['class'][1] ### Looking for the star-rating class, and extracting the second class attribute (star rating 1-5)


df = pd.DataFrame(list())
df.to_csv('book.csv')

header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available",
    "product_description", "category", "review_rating", "image_url"]

book = [ url, tds[0].text, title.text, tds[3].text[1:], tds[2].text[1:], number_available, description, category, rating, image_url ]


with open('book.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(book)


with open('book.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
"""