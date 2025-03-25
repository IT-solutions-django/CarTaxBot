from .models import Currency
import requests
from bs4 import BeautifulSoup


def update_exchange_rates() -> None: 
    url = 'https://www.cbr.ru/currency_base/daily/'
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml') 
    
    for currency in Currency:
        tr_element = soup.find(lambda tag: tag.name == "tr" and tag.find("td", string=currency.value))
        _, curr_code, quantity, _, exchange_rate_raw = map(lambda x: x.text, tr_element.find_all('td'))
        exchange_rate = float(exchange_rate_raw.replace(',', '.')) / int(quantity) 

        print(curr_code)
        print(float(exchange_rate_raw.replace(',', '.'))) 
        print(exchange_rate)