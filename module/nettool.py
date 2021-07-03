from whois import whois
import socket
import requests
import re

def whoiss(url):
    try:
        whoisresult = whois(url)
        return whoisresult
    except Exception as emror:
        json = {'error': str(emror)}
        return json

def dns_lookup(url):   
   try:
        urlfil = re.compile(r"https?://(www\.)?")
        fixed = urlfil.sub('', url).strip().strip('/')  
        domain_dns = {'domain':fixed}
        dnss = socket.gethostbyname(fixed)
        get_full = requests.get('https://ipinfo.io/{}/?token=a5791fcad3e4da'.format(dnss)).json()
        domain_dns.update(get_full)
        return domain_dns
   except Exception as emror:
        return emror
