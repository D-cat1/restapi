from bs4 import BeautifulSoup
import requests
import cloudscraper

def mediafire(url):
    req_ke_link = requests.get(url=url).text
    scrap = BeautifulSoup(req_ke_link, 'html.parser')
    link = scrap.find_all(name='a', attrs={'id':'downloadButton'})
    title = scrap.find_all(name='div', attrs={'class':'dl-btn-label'})
    moreinf = scrap.select('ul[class="details"] > li > span')
    jsondata = dict()
    if len(link) == 0:
        jsondata['link_mati'] = True
        return jsondata    
    else:
        jsondata['link_mati'] = False
        jsondata['title'] = title[0]['title']
        jsondata['ukuran'] = moreinf[0].text
        jsondata['dibuat'] = moreinf[1].text
        jsondata['download_link'] = link[0]['href']
        return jsondata

def zippyshare(url):
    req_ke_link = requests.get(url=url).text
    scrap = BeautifulSoup(req_ke_link, 'html.parser')
    base_url = url.split('://')
    schema = base_url[0]
    servzippy = base_url[1].split('/')[0]
    math = scrap.select('div[id="lrbox"] > div')
    bsagain = BeautifulSoup(str(math[1]), 'html.parser')
    getsc = bsagain.find_all('script')
    jsondata = dict()
    zipfix = []
    for select in getsc:
        if select.string is not None:
            zipfix.append(select)

    if len(zipfix) == 0:
        jsondata['link_mati'] = True
        return jsondata    
    else:
        solve = zipfix[0].string.split('/" + (')
        id = solve[0].split('href = "')[1]
        line = solve[1].split(') + "')[1].split('";')[0]
        mathsolve = zipfix[0].string.split('/" + (')[1]
        mathsolve2 = eval(mathsolve.split(') + "')[0])
        infoo = []
        for get in math:
            if get.font is not None:
                infoo.append(get)

        infix = BeautifulSoup(str(infoo[0]), 'html.parser')
        infos = infix.findAll('font')
        jsondata['link_mati'] = False
        jsondata['title'] = infos[2].text
        jsondata['ukuran'] = infos[4].text
        jsondata['dibuat'] = infos[6].text
        jsondata['download_link'] = '{}://{}{}/{}{}'.format(schema, servzippy, id, mathsolve2, line)
        return jsondata

def anonfiles(link):
   anonscr = cloudscraper.create_scraper()
   htmlstr = anonscr.get(url=link)
   scrap = BeautifulSoup(htmlstr.text, 'html.parser')
   linka = scrap.select('a[id="download-url"]')
   jsondata = dict()
   if len(linka) == 0:
        jsondata['link_mati'] = True
        return jsondata
   else:
        id = link.split('/')[3]
        getinfo = requests.get('https://api.anonfiles.com/v2/file/{}/info'.format(id)).json()
        jsondata['title'] = getinfo["data"]["file"]["metadata"]["name"]
        jsondata['ukuran'] = getinfo["data"]["file"]["metadata"]["size"]["readable"]
        jsondata['download_link'] = linka[0]["href"]
        return jsondata

def sfile(links):
    header = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
    getsfile = requests.get(links, headers=header).text
    link = BeautifulSoup(getsfile, 'html.parser')
    direklink = link.find(name='a', attrs={'id':'download'})
    jsondata = dict()
    if direklink is None:
        jsondata['link_mati'] = True
        return jsondata
    else:
        info = link.find(name='meta', attrs={"name":"description"})
        link = direklink['href']
        nama = info["content"].replace("Download ", "").split(" diupload ")[0]
        tanggal = info["content"].replace("Download ", "").split(" pada ")[1].split(" di ")[0]
        typesss = info["content"].replace("Download ", "").split(" di folder ")[1].split(' ')[0]
        ukur = info["content"].replace("Download ", "").split(" di folder ")[1].replace('{} '.format(typesss), '').replace('B.', 'B')
        jsondata['title'] = nama
        jsondata['ukuran'] = ukur
        jsondata['dibuat'] = tanggal
        jsondata['tipe'] = typesss
        jsondata['download_link'] = link
        return jsondata