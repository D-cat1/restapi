import requests
from bs4 import BeautifulSoup
import json


def generate_selective(id):
    ass = open('./module/dataephoto/textnoimg.json')
    habs = json.load(ass)
    for cekid in habs:
        if cekid["id"] == id:
            cekid["found"] = True
            return cekid

    return {'found' : False}
        
def gen(id, text, radio=None):
    humanss = {
    'Ibra-Country': 'unknow',
    'Ibra-Version-Code': '113',
    'Ibra-Language': 'en',
    'Ibra-Encrypt': '1',
    'Ibra-Os': 'android',
    'Ibra-App-Id': "ephoto",
    'Ibra-Category': '0',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'okhttp/4.4.0'}
    datatext = text.split(';')
    dasa = {'effect_id': id,
            'text[]': datatext
            }
    if radio is not None:
       dasa = {'effect_id': id,
            'text[]': datatext,
            'radio[]': radio
            }  
    #https://apipro.yogroup.net/api/search-effect/v15?line_per_page=40&page=1&search=glass get
    #https://apipro.yogroup.net/api/get-effect-category-list/v15 get
    #https://apipro.yogroup.net/api/get-effect-list/v15?line_per_page=20&category_id=57da028c0dde08c427920a06&page=1 get
    #https://appbuild1.yogroup.net/api/create-image/v15?effect_id=596b2d042ea7b95c02948890&text%5B%5D=has&text%5B%5D=hias&screen_width=768 post
    get_succ = requests.post('https://appbuild1.yogroup.net/api/create-image/v15', data=dasa,headers=humanss).json()
    if get_succ['success']:
        return get_succ
    else:
        return {'success': False}
