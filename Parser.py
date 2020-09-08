import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0', 'accept':'*/*'}
HOST = 'https://auto.ria.com'

def get_html (url, params=None):
    r=requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
   soup = BeautifulSoup(html, 'html.parser')
   pagenation = soup.find_all('span', class_ = 'page-item mhide')
   if pagenation:
       return int(pagenation[-1].get_text())
   else:
       return 1



def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'proposition')
    print(items)

    cars = []
    for item in items:
        cars.append({

            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': item.find('span', class_='grey size13').get_text(),
            'region': item.find('svg', class_ ='svg-i16_pin').find_next('strong').get_text(),
            'link': HOST + item.find('h3', class_='proposition_name').find_next('a').get('href'),
        })
        print(cars)
def parse():
    html=get_html(URL)
    print(html.status_code)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
         print(f'Парсинг страницы{page} из {pages_count}...')
         html = get_html(URL, params={'page':page})

         cars.extend(get_content(html.text))
         #cars = get_content(html.text)
         print(cars)
        print(len(cars))

    else:
        print('Error')
parse()

