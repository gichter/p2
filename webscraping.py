import requests
import re
import csv
from bs4 import BeautifulSoup
import os, shutil, pathlib
import math



print('Lancement du scraping...')

books_max_number = 0
book_total_number = 0
main_folder = 'Book Data'

if os.path.exists(main_folder):
    shutil.rmtree(main_folder)
os.mkdir(main_folder)

url = "http://books.toscrape.com/" 
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
categories = soup.find('ul', {'class': 'nav-list'})
books_max_number = int(soup.findAll('strong')[0].text)


for a in categories.select("li a"):
    url = "http://books.toscrape.com/" + a.get('href')
    category_name = url[51:].split("_")[0]
    if(category_name != "1/index.html"):
        pathlib.Path(main_folder + '/' + category_name).mkdir(parents=True, exist_ok=True) 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        pages = soup.findAll('strong')
        number_of_pages = (math.ceil(int(pages[1].text)/20)) # Nombre de pages dans une catégorie
        header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available",
            "product_description", "category", "review_rating", "image_url"]
        with open(main_folder + '/' + category_name + '/' + category_name + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        while number_of_pages > 0:
            if(number_of_pages == 1):
                response = requests.get(url)
            else:
                response = requests.get(url[:-10] + "page-" + str(number_of_pages) + ".html")
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
            number_of_pages -= 1
            number_of_category_books = 0
            total_number_of_category_books = int(pages[1].text)
            for b in books:
                number_of_category_books += 1
                for a in b.select("h3 a"): 
                    book_url = "http://books.toscrape.com/catalogue/" + a.get('href')[9:]
                    response = requests.get(book_url)
                    soup = BeautifulSoup(response.content, 'html.parser')
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
                    with open(main_folder + '/' + category_name + '/' + category_name + '.csv', 'a', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        writer.writerow(book)
                        book_total_number += 1                    
                    img_data = requests.get(image_url).content
                    with open(main_folder + '/' + category_name + '/' + image_reference, 'wb') as handler:
                        handler.write(img_data)
                    
                    os.system('clear')
                    print ('Scraping de la catégorie "' + category_name + '" (' + pages[1].text + ' livres)\n')
                    print(title.text + '\n')

                    category_progress_bar = '[{0}{1}] {2}%\n'
                    category_progress = math.floor(number_of_category_books * 100/total_number_of_category_books)
                    print(category_progress_bar.format('#' * category_progress, '-' * (100 - category_progress), category_progress))

                    progress_bar = '[{0}{1}] {2}%'
                    total_progress = math.floor(book_total_number * 100/books_max_number)
                    print(progress_bar.format('#' * total_progress, '-' * (100 - total_progress), total_progress))

print("Nombre total de livres récupérés :" + str(book_total_number))