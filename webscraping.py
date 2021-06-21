import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import os
import math

book_total_number = 0

response = requests.get("http://books.toscrape.com/")
soup = BeautifulSoup(response.text, 'html.parser')
categories = soup.find('ul', {'class': 'nav-list'})

for a in categories.select("li a"):
    url = "http://books.toscrape.com/" + a.get('href')
    category_name = url[51:].split("_")[0]
    if(category_name != "1/index.html"):
        
        print (category_name)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        pages = soup.findAll('strong')
        number_of_pages = (math.ceil(int(pages[1].text)/20)) # Nombre de pages dans une catégorie

        header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available",
            "product_description", "category", "review_rating", "image_url"]

        with open(category_name + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        while number_of_pages > 0:
            if(number_of_pages == 1):
                response = requests.get(url)
            else:
                response = requests.get(url[:-10] + "page-" + str(number_of_pages) + ".html")
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
            #print(url + 'page-' + str(number_of_pages) + '.html')
            number_of_pages -= 1

            for b in books:
                for a in b.select("h3 a"): 
                    book_url = "http://books.toscrape.com/catalogue/" + a.get('href')[9:]
                    response = requests.get(book_url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tds = soup.findAll('td')
                    title = soup.find('h1')
                    description = soup.findAll('p')[3].text
                    number_available = re.search(r'\d+', tds[5].text).group(0) ### searching the number in the string using regex
                    category = soup.findAll('a')[3].text
                    rating = soup.findAll('p')[2] ### TODO
                    image_url = "http://books.toscrape.com/" + soup.findAll('img')[0]['src'][6:] ### concatenating base url and image relative url
                    rating = soup.find('p', {'class': 'star-rating'})['class'][1] ### Looking for the star-rating class, and extracting the second class attribute (star rating 1-5)
                    
                    book = [ book_url, tds[0].text, title.text, tds[3].text[1:], tds[2].text[1:], number_available, description, category, rating, image_url ]
                    with open(category_name + '.csv', 'a', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        writer.writerow(book)
                        print(title.text)
                        book_total_number += 1


print("Nombre total de livres récupérés :" + str(book_total_number))
""" 
    print("http://books.toscrape.com/" + a.get('href'))

df = pd.DataFrame(list())
df.to_csv('book.csv')

with open('book.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
""" 