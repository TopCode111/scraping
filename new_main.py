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

        # This is for row 2 (meta @description)
        name = 'meta_description'
        length_var_name = 'meta_desc_len'
        try:
            meta_tag = soup.find("meta", {"name": "description"})
            desc_content = meta_tag['content']
            desc_text_ln = len(desc_content)
            # desc_text_ln = int(desc_text_ln)

            if desc_text_ln < 150:
                result = {
                    'name': name,
                    'message': 'Votre méta-description est trop courte, le nombre de caractère optimale doit être entre 150 et 250 caractères.',
                    length_var_name: desc_text_ln,
                    'desc_content': desc_content,
                    'marks': 1
                }
                final_score = final_score + result['marks']
                result_dict['meta_description'] = result
                print('try worked1')

            elif desc_text_ln > 150 and desc_text_ln < 250:
                result = {
                    'name': name,
                    'message': 'Félicitations votre site dispose d’une méta-description avec un nombre de caractère optimal entre 150 et 250 caractères',
                    length_var_name: desc_text_ln,
                    'desc_content': desc_content,
                    'marks': 5
                }
                final_score = final_score + result['marks']
                result_dict['meta_description'] = result
                print('try worked2')

            elif desc_text_ln > 250:
                result = {
                    'name': name,
                    'message': ' Votre méta-description est trop longue, essayez de la raccourcir, le nombre optimal est entre 150 et 250 caractères, le reste risque d’être tronqué sur l’affichage du résultat sur les moteurs de recherche.',
                    length_var_name: desc_text_ln,
                    'desc_content': desc_content,
                    'marks': 2
                }
                final_score = final_score + result['marks']
                result_dict['meta_description'] = result
                print('try worked3')
        except:
            result1 = {
                'name': name,
                'message': 'Votre site ne dispose pas de méta-description, La balise meta description manque sur votre page. Vous devez inclure cette balise afin de fournir une brève description de votre page pouvant être utilisée par les moteurs de recherche. Des méta-descriptions bien écrites et attrayantes peuvent également aider les taux de clics sur votre site dans les résultats de moteur de recherche.',
                length_var_name: 0,
                'marks': 0
            }
            final_score = final_score + result1['marks']
            result_dict['meta_description'] = result1
            print('except worked')
