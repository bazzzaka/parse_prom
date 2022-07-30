import csv
import requests
from bs4 import BeautifulSoup


def console_user():
    greeting = 'Парсер prom.ua готовий до роботи!'
    print(greeting)
    get_pages = int(input('Прошу ввести вас бажану кількість сторінок для парсингу (Наприклад: 5):'))
    get_name = input('Як назвати таблицю?')
    print(f'Замовлено сторінок для парсингу --> {get_pages}')
    print('Проводиться обробка інформації. Зачекайте будь ласка...')
    parser_prom(get_pages, get_name)

    print('Парсер завершив свою роботу. Дякую що скористались саме ним!')


def write_csv(data, name_csv):
    with open(f'{name_csv}.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow(
                (
                    item['name'],
                    item['price'],
                    item['city'],
                    item['link']
                )
            )


def parser_prom(pages, name_csv):
    data = list()
    title_for_table = {'name': 'Назва товару', 'price': 'Ціна', 'link': 'Лінк магазину', 'city': 'Доставка'}
    data.append(title_for_table)
    for page in range(0, pages):
        prom_url = 'https://prom.ua'
        url = 'https://prom.ua/ua/Krossovki-obuv-dlya-bega;{}'.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        card_with_data = soup.find_all('div', {'class': 'M3v0L DUxBc sMgZR _5R9j6 qzGRQ IM66u J5vFR hxTp1'})
        for n, i in enumerate(card_with_data, start=0):
            item_name = i.find('span', {'class': '_3Trjq htldP _7NHpZ h97_n'}).text.strip()
            item_price = i.find('span', {'data-qaid': 'product_price'}).text
            item_city = i.find('span', {'data-qaid': 'product_presence'}).text
            item_link = i.find('a', {'class': '_0cNvO jwtUM XCtBJ OX5sJ'}).get('href')
            item_link = prom_url + item_link
            item = {'name': item_name, 'price': item_price, 'link': item_link, 'city': item_city}
            data.append(item)
        write_csv(data, name_csv)


if __name__ == '__main__':
    console_user()
