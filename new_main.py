#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from six.moves.urllib import parse
import urllib
import requests
from lxml import html
import re
import json
from gglsbl import SafeBrowsingList
from wordcloud import WordCloud
import io
import matplotlib.pyplot as plt
import tldextract
import base64

def scrapper(url):
    url = url.strip()
    url = "https://www.stuffnice.com/"
    url5 = url
    if "www" in url:
        url = url.replace("www.","")
        print(url)
    else:
        pass

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    final_report = []
    final_score = 0

    from .result_dict import result_dict

    domain =tldextract.extract(url).domain
    suffix = tldextract.extract(url).suffix
    subdomain = tldextract.extract(url).subdomain
    pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'
    # row 15 HTTPS test

    result = {
        'name': 'https_test',
        'message': '',
        'marks': ''
    }

    if "https" in url or "http" in url:
        print("if worked")

        a = url.split(":")
        a[0] = "https:"
        web = "".join(a)

        print("This is web  ", web)

        try:
            print("try of if worked")
            r = requests.get(web, headers=headers)
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            url = web
            result[
                'message'] = 'Félicitations. Votre site les données transitants par votre site sont sécurisées avec un certificat SSL'
            result['marks'] = 4
        except:

            a = url.split(":")
            a[0] = "http:"
            url3 = "".join(a)

            print("try of except worked")
            r = requests.get(url3, headers=headers, verify=False)
            url = url3
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = '''
                    Votre site ne dispose pas de certificat SSL. Les données qui y transitent peuvent donc être récupérés par des parties malveillantes. Google donne une grande importance à la sécurité des visiteurs.
                    '''
            result['marks'] = 0
            print("HTTPS didn't worked")
    else:
        print("else worked")
        try:
            url2 = 'https://' + url
            r = requests.get(url2, headers=headers)
            url = url2
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result[
                'message'] = 'Félicitations. Votre site les données transitants par votre site sont sécurisées avec un certificat SSL'
            result['marks'] = 4


        except:
            url1 = 'http://' + url
            print("from else except ", url1)
            r = requests.get(url1, headers=headers, verify=False)
            url = url1
            # req = urllib.request.Request(url, headers=headers)
            # r = urllib.request.urlopen(req)
            result['message'] = '''
                    Votre site ne dispose pas de certificat SSL. Les données qui y transitent peuvent donc être récupérés par des parties malveillantes. Google donne une grande importance à la sécurité des visiteurs.
                    '''
            result['marks'] = 0
    print(result)
    result_dict['https_test'] = result
    final_score = final_score + result['marks']

    soup = BeautifulSoup(r.text, "lxml")

    # This is for row 1 (title)
    try:
        title_content = soup.find('title').text
        title_ln = len(title_content)

        if title_ln < 70:
            result = {
                'name': 'title',
                'message': 'Félicitations votre site dispose d’un titre avec un nombre de caractères optimale soit moins de 70 caractères',
                'title_length': title_ln,
                'title_content': title_content,
                'marks': 5
            }
            final_score = final_score + 5
            result_dict['title'] = result
        elif title_ln > 70:
            result = {
                'name': 'title',
                'message': 'Votre titre est trop long, le nombre de caractères optimal est de 70 caractères, essayez de le raccourcir',
                'title_length': title_ln,
                'title_content': title_content,
                'marks': 2
            }
            final_score = final_score + 2
            result_dict['title'] = result
    except:
        result = {
            'name': 'title',
            'message': 'Votre site ne dispose pas de balise meta title. La balise <title> correspond au titre de votre page web. Il s’agit d’un champ essentiel à ne pas négliger dans le cadre d’une bonne stratégie d’optimisation du référencement naturel puisqu’elle est l’un des critères les plus importants pour les moteurs de recherche (Google, Bing...)',
            'title_length': 0,
            'marks': 0
        }
        final_score = final_score + 0
        result_dict['title'] = result
