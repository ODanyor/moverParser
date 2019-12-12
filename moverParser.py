#!/usr/bin/env python3

import  csv
import urllib.request
from bs4 import BeautifulSoup


BASE_URL = 'https://mover.uz/video/interesting/'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html)
    pages = soup.find('span', class_='ut')
    return int(pages.find_all('a')[-1].text)

def parse(html):
    soup = BeautifulSoup(html) #Allow to us to do some serachs of tags with our html file
    table = soup.find('div', class_='video-list vertical')
    #print(table.prettify())

    database = []

    for row in table.find_all('div', class_='info'):
        database.append({
            'title': row.find_all('h6')[0].a.text.strip(),
            'views': row.find_all('p')[0].text.strip().split(':')[1],
            'chanel': row.find_all('p')[1].a.text.strip()
        })
    return database

def save(database, path):
    with open(path, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Videos', 'Count of views', 'Autor'))

        for data in database:
            writer.writerow((data['title'], ', '.join(data['views']), data['chanel']))

def main():
    page_count = get_page_count(get_html(BASE_URL))
    print(f'Found {page_count} pages')
    database = []
    for page in range(1, page_count):
        formula = (page/page_count*100)
        print(f'Completed {formula}%')
        database.extend(parse(get_html(BASE_URL + f'?page={page}')))

    save(database, 'database.csv')

    #print(parse(get_html(BASE_URL)))

if __name__ == '__main__':
    main()