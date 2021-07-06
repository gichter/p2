import threading
import requests
import re
import csv
from bs4 import BeautifulSoup
import os, shutil, pathlib
import math
import datetime
from threading import Thread

begin_time = datetime.datetime.now()

def fetch_url(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def get_book_data(a):
    book_url = "http://books.toscrape.com/catalogue/" + a.get('href')[9:]
    soup = fetch_url(book_url)
    tds = soup.findAll('td')
    title = soup.find('h1')
    description = soup.findAll('p')[3].text
    number_available = re.search(r'\d+', tds[5].text).group(0) ### searching the number in the string using regex
    category = soup.findAll('a')[3].text
    rating = soup.findAll('p')[2] ### TODO
    image_url = "http://books.toscrape.com/" + soup.findAll('img')[0]['src'][6:] ### concatenating base url and image relative url
    rating = soup.find('p', {'class': 'star-rating'})['class'][1] ### Looking for the star-rating class, and extracting the second class attribute (star rating 1-5)
    image_reference = (title.text.replace('/', '_') + "_image.jpg")
    
    book = [ book_url, tds[0].text, title.text, tds[3].text[1:], tds[2].text[1:], number_available, description, category, rating, image_url, image_reference ]
    return book

def scrape_category(category_name, url):
        if(category_name != "1/index.html"):
            pathlib.Path(main_folder + '/' + category_name).mkdir(parents=True, exist_ok=True) 
            soup = (fetch_url(url))
            pages = soup.findAll('strong')
            number_of_pages = (math.ceil(int(pages[1].text)/20)) # Nombre de pages dans une catégorie
            header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available",
            "product_description", "category", "review_rating", "image_url"]
            with open(main_folder + '/' + category_name + '/' + category_name + '.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
            #total_number_of_category_books = int(pages[1].text)

            threads_page = []
            while number_of_pages > 0:
                t = Thread(target=scrape_page, args=(category_name, url, number_of_pages))
                threads_page.append(t)
                number_of_pages -= 1
                
            for x in threads_page:
                x.start()

            for x in threads_page:
                x.join()

def scrape_page(category_name, url, number_of_pages):
    if(number_of_pages == 1):
        soup = (fetch_url(url))
    else:
        soup = (fetch_url(url[:-10] + "page-" + str(number_of_pages) + ".html"))
    books = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    for b in books:
        for a in b.select("h3 a"): 
            book = get_book_data(a)
            print(book[2])
            with open(main_folder + '/' + category_name + '/' + category_name + '.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(book)    
            img_data = requests.get(book[9]).content
            with open(main_folder + '/' + category_name + '/' + book[10], 'wb') as handler:
                handler.write(img_data) 

print('Lancement du scraping...')

main_folder = 'Book Data'

if os.path.exists(main_folder):
    shutil.rmtree(main_folder)
os.mkdir(main_folder)

url = "http://books.toscrape.com/" 
soup = (fetch_url(url))
categories = soup.find('ul', {'class': 'nav-list'})

threads = []
for a in categories.select("li a"):
    url = "http://books.toscrape.com/" + a.get('href')
    category_name = url[51:].split("_")[0]
    t = Thread(target=scrape_category, args=(category_name, url))
    threads.append(t)
    
for x in threads:
    x.start()

for x in threads:
    x.join()

print("Temps d'execution du script : " + str(datetime.datetime.now() - begin_time))