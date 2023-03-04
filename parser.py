import requests
from bs4 import BeautifulSoup
import csv


CSV = 'condos.csv'
HOST = 'https://www.kijiji.ca'
URL = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


condos = []


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='info-container')

    for item in items:
        condos.append({
            'title': item.find('div', class_='title').find('a', class_='title').get_text(strip=True),
            'link': HOST + item.find('div', class_='title').find('a').get('href'),
            'description': item.find('div', class_='description').get_text(strip=True),
            'location': item.find('div', class_='location').find('span').get_text(strip=True),
            'date_posted': item.find('div', class_='location').find('span', class_='date-posted').get_text(),
            'price': item.find('div', class_='price').get_text(strip=True),
        })
    return condos


def save_info(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Condos', 'link', 'Description', 'Location', 'Date Posted', 'Price'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['description'], item['location'], item['date_posted'], item['price']])


def parser():
    PAGINATION = input('Укажите количество страниц для парсинга!:')
    PAGINATION = int(PAGINATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        condos = []
        for page in range(0, PAGINATION):
            print(f'Парсим странису: {page}')
            html = get_html(URL, params={'page': page})
            condos.extend(get_content(html.text))
            save_info(condos, CSV)
        print(f'Спарсились {page} странисы')
    else:
        print('url not found')


parser()


# html = get_html(URL)
# print(get_content(html.text))