from bs4 import BeautifulSoup
import requests
from random import choice

def jagokatarnd():
    header =    {"referer": "https://www.google.com/",
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    menggok = requests.get('https://jagokata.com/kata-bijak/acak.html', headers=header).text
    quote = BeautifulSoup(menggok, 'html.parser')
    all = quote.find_all(name="q", attrs={"class":"fbquote"})
    dataquotes = quote.select('ul[id="citatenrijen"] > li[id!="googleinpage"]')
    ngaray = []
    for scrapq in dataquotes:
        qtag = scrapq.q.text
        qauthor = scrapq.div.a.text
        ngaray.append({'quote': qtag, 'author':qauthor})
    
    quotes = choice(ngaray)
    return quotes

