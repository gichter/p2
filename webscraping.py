import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/how-to-be-miserable-40-strategies-you-already-use_897/index.html"


response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
tds = soup.findAll('td')
for td in tds:
    print(td.string)

###
### print(len(tds))
### print(tds)
###