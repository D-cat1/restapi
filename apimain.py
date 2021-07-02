from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response
from module.jagokata import jagokatarnd
from module.direct import mediafire, zippyshare, anonfiles, sfile
from module.ytdownload import youtube
from module.islamic import suratJSON


def generate_error(code):
    html = """<!DOCTYPE html>
<html>
<head>
<style>
body, html {
  height: 100%;
}

.bg {

  background-image: url("https://http.cat/"""+str(code)+"""");


  height: 100%;

  background-position: center;
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
</style>
</head>
<body class=bg>
</body>
</html>"""
    return html


tags_metadata = [
    {
        "name": "Kata - Kata Bijak",
        "description": "menampilkan kata - kata bijak secara random",
    },
    {
        "name": "Direct Link",
        "description": "mengambil direct link dari beberapa situs",
    },
    {
        "name": "Media Ekstrak",
        "description": "mengambil media dan infonya dari situs seperti youtube, instagram, facebook, soundcloud, vidio",
    },
    {
        "name": "Surat",
        "description": "menampilkan surat sesusai nomor surat",
    },
    
]
app = FastAPI(title='Daffa Rest Api', redoc_url='/dokumentasi2', docs_url='/dokumentasi', openapi_tags=tags_metadata, openapi_url='/ehe')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return HTMLResponse(content=generate_error(400), status_code=400)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.status_code)
    return HTMLResponse(content=generate_error(exc.status_code), status_code=exc.status_code)


@app.get("/", include_in_schema=False)
def redirect_ke_dokumen_ini():
    return RedirectResponse("/dokumentasi")

@app.get("/katabijak", tags=["Kata - Kata Bijak"])
def random_kata_bijak():
    return JSONResponse(content=jagokatarnd())

@app.get("/direct/mediafire", tags=["Direct Link"])
def direct_link_dan_info_file_dari_mediafire(url):
    fixurl = url.split('?')[0]
    filter = fixurl.startswith("https://www.mediafire.com") or fixurl.startswith("http://www.mediafire.com")
    filter2 = fixurl.startswith("https://mediafire.com") or fixurl.startswith("http://mediafire.com")
    if filter or filter2:
        getdirek = mediafire(fixurl)
        return getdirek
    else:
        return HTMLResponse(content=generate_error(422), status_code=422)

@app.get("/direct/zippyshare", tags=["Direct Link"])
def direct_link_dan_info_file_dari_zipppyshare(url):
    fixurl = url.split('?')[0]
    bangsc = filtersch = fixurl.split('://')
    if len(bangsc) <= 1:
        return HTMLResponse(content=generate_error(422), status_code=422)
    else:
        bangsc[0].startswith('http')
        get_domain = bangsc[1].split('.')[1].startswith('zippyshare')
        print(get_domain)
        if filtersch and get_domain:
            getdirek = zippyshare(fixurl)
            return getdirek
        else:
            return HTMLResponse(content=generate_error(422), status_code=422)
    


@app.get("/direct/anonfiles", tags=["Direct Link"])
def direct_link_dan_info_file_dari_anonfiles(url):
    fixurl = url.split('?')[0]
    filter = fixurl.startswith("https://www.anonfiles.com") or fixurl.startswith("http://www.anonfiles.com")
    filter2 = fixurl.startswith("https://anonfiles.com") or fixurl.startswith("http://anonfiles.com")
    if filter or filter2:
        getdirek = anonfiles(fixurl)
        return getdirek
    else:
        return HTMLResponse(content=generate_error(422), status_code=422)

@app.get("/direct/sfile", tags=["Direct Link"])
def direct_link_dan_info_file_dari_sfile(url):
    fixurl = url.split('?')[0]
    filter = fixurl.startswith("https://www.sfile.mobi") or fixurl.startswith("http://www.sfile.mobi")
    filter2 = fixurl.startswith("https://sfile.mobi") or fixurl.startswith("http://sfile.mobi")
    if filter or filter2:
        getdirek = sfile(fixurl)
        return getdirek
    else:
        return HTMLResponse(content=generate_error(422), status_code=422)

@app.get("/streamdl", tags=["Media Ekstrak"])
def info_media_dan_link_download(link):
    aer = youtube(link)
    return aer


@app.get("/surat/{nomorsurat}", tags=["Surat"])
def menampilkan_surat_sesuai_nomor_surat(nomorsurat: int):
    return suratJSON(nomorsurat)







