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
            # This is for row 3 (meta @keywords)
        name = 'meta_keywords'
        length_var_name = 'meta_key_len'
        try:
            meta_tag = soup.find("meta", {"name": "keywords"})
            meta_key_content_ln = len(meta_tag['content'])
            # title_ln = int(meta_key_content_ln)

            if meta_key_content_ln:
                result = {
                    'name': name,
                    'message': 'Bravo vous avez spécifié des meta keywords . Vos mots-clés principaux doivent apparaître dans vos méta-tags pour vous aider à identifier le sujet de votre page Web dans les moteurs de recherche.',
                    length_var_name: meta_key_content_ln,
                    'marks': 1
                }
                final_score = final_score + result['marks']
                result_dict['meta_keywords'] = result
                print('try worked1')
        except:
            result = {
                'name': name,
                'message': 'Vos mots-clés principaux doivent apparaître dans vos méta-tags pour vous aider à identifier le sujet de votre page Web dans les moteurs de recherche.',
                length_var_name: 0,
                'marks': 0
            }
            final_score = final_score + result['marks']
            result_dict['meta_keywords'] = result
            print('except worked')
            # This is for row 4 (meta @robots)
        name = 'meta_robots'
        length_var_name = 'meta_robots_len'
        try:
            meta_tag = soup.find("meta", {"name": "robots"})
            meta_robots_content = len(meta_tag['content'])
            # title_ln = int(desc_text_ln)

            if meta_robots_content:
                result = {
                    'name': name,
                    'message': "Votre site dispose d'un fichier robots.txt",
                    length_var_name: meta_robots_content,
                    'marks': 4
                }
                final_score = final_score + result['marks']
                result_dict['meta_robots'] = result
                print('try worked1')
        except:
            result1 = {
                'name': name,
                'message': '''
                               Votre site n’a pas de robot.txt
                               Le robots.txt est un fichier texte utilisant un format précis qui permet à un Webmaster de contrôler quelles zones de son site un robot d'indexation est autorisé à analyser. Ce fichier texte sera disponible à une URL bien précise pour un site donné, par exemple http://www.monsite.com/robots.txt
                               Pour bien comprendre à quoi sert un robots.txt, il faut comprendre la manière dont fonctionnent les robots d'indexation des moteurs de recherche (appelés aussi Web spiders, Web crawlers ou Bots) tels que Google, Yahoo ou Bing. Voici leurs actions lorsqu'ils analysent un site tel que www.monsite.com : ils commencent par télécharger et analyser le fichier http://www.monsite.com/robots.txt.
                   ''',
                length_var_name: 0,
                'marks': 0
            }
            final_score = final_score + result1['marks']
            result_dict['meta_robots'] = result1
            print('except worked')
            # This is for row 5 (html lang)
        name = 'html_lang'
        length_var_name = 'html_lang'
        try:
            meta_tag = soup.find("html", {"lang": True})
            lang_text = meta_tag['lang']

            result = {
                'name': name,
                'message': "Félicitations. Vous avez spécifié une langue à votre page.",
                length_var_name: lang_text,
                'marks': 3
            }
            final_score = final_score + result['marks']
            result_dict['html_lang'] = result
            print('try worked1')
        except:
            result1 = {
                'name': name,
                'message': '''
                   Vous devriez spécifier une langue pour votre site, les moteurs de recherches ne comprennent pas quand un site dispose de plusieurs langues par exemple ayant des mots techniques en anglais et un contenu texte en français. Il faut donc bien spécifier la langue.
                   ''',
                length_var_name: 0,
                'marks': 0
            }
            final_score = final_score + result1['marks']
            result_dict['html_lang'] = result1
            print('except worked')

        # This is for row 6 (sitemap)
        url = url.strip()
        sitemap_url = url + '/sitemap.xml'
        print("Sitemap url ", sitemap_url)
        try:

            code = requests.get(sitemap_url, headers=headers).status_code

            name = 'sitemap'

            if code == 200:
                result = {
                    'name': name,
                    'message': "Félicitations, votre site dispose d’un fichier sitemap",
                    'marks': 2
                }
                final_score = final_score + result['marks']
                result_dict['sitemap'] = result

            else:
                result = {
                    'name': name,
                    'message': "Votre site Web ne dispose pas d'un fichier sitemap. Les sitemaps peuvent aider les robots à indexer votre contenu de manière plus complète et plus rapide. ",
                    'marks': 0
                }
                final_score = final_score + result['marks']
                result_dict['sitemap'] = result
        except:
            result = {
                'name': name,
                'message': "Votre site Web ne dispose pas d'un fichier sitemap. Les sitemaps peuvent aider les robots à indexer votre contenu de manière plus complète et plus rapide. ",
                'marks': 0
            }
            final_score = final_score + result['marks']
            result_dict['sitemap'] = result
            # This is for row 7 (google Analytics)
            searched_word = 'google-analytics'

            name = 'google_analytics'
            if searched_word in str(soup):
                print("Google analytics found")
                result = {
                    'name': name,
                    'message': "Félicitations, votre site dispose de l'outil Google Analytics",
                    'marks': 2
                }
                final_score = final_score + result['marks']
                result_dict['google_analytics'] = result

            else:
                result = {
                    'name': name,
                    'message': "Votre site ne dispose pas de l'outil Google Analytics.",
                    'marks': 0
                }
                final_score = final_score + result['marks']
                result_dict['google_analytics'] = result

            # This is for row 8 (page_cache)
            name = 'page_cache'
            length_var_name = 'page_cache_desc'
            try:
                meta_tag = soup.find("meta", {"http-equiv": "Cache-control"})
                lang_text = meta_tag['content']

                result = {
                    'name': name,
                    'message': "Vous avez activé le cache sur votre page, c'est très bien.",
                    length_var_name: lang_text,
                    'marks': 3
                }
                final_score = final_score + result['marks']
                result_dict['page_cache'] = result
                print('try worked1')
            except:
                result1 = {
                    'name': name,
                    'message': "Vous n'avez pas activé la mise en cache sur vos pages. La mise en cache permet un chargement plus rapide des pages.",
                    length_var_name: 0,
                    'marks': 0
                }
                final_score = final_score + result1['marks']
                result_dict['page_cache'] = result1
                print('except worked')
                # API_KEY = AIzaSyD_RLUOcTN1JAq8PL8zJ79X6-kmHIDy_uM
                # This is for row 9 (Google safe browsing api)

            api_key = 'AIzaSyCVylpWnsOwzUoeTGg7akZRod-4YbhXoPU'
            sbl = SafeBrowsingList(api_key)
            bl = sbl.lookup_url(url)

            name = 'google_safe_browsing'
            print("google_safe_browsing ", url)
            if bl is None:
                print("Website is safe")
                result = {
                    'name': name,
                    'message': "Votre site est considéré comme sécurisé.",
                    'marks': 2
                }
                final_score = final_score + result['marks']
                result_dict['google_safe_browsing'] = result

            else:
                result = {
                    'name': name,
                    'message': "Votre site n'est pas considéré comme sécurisé. Google et les autres moteurs de recherche prennent en compte le niveau de sécurité de votre site pour garantir la sécurité des visiteurs.",
                    'marks': 0,
                    'threats': bl
                }
                final_score = final_score + result['marks']
                result_dict['google_safe_browsing'] = result

            # This is for row 10 (responsive website test)
            name = 'responsive_test'
            length_var_name = 'responsive_test_desc'
            try:
                meta_tag = soup.find("meta", {"name": "viewport"})
                lang_text = meta_tag['content']

                result = {
                    'name': name,
                    'message': "Félicitations. Votre site est responsive.",
                    length_var_name: lang_text,
                    'marks': 4
                }
                final_score = final_score + result['marks']
                result_dict['responsive_test'] = result
                print('try worked1')
            except:
                result1 = {
                    'name': name,
                    'message': '''
                       Nous n'avons pas détécté que votre site internet était responsive, soit adapté au mobile. Google prend énormément en compte ce critère pour un bon référencement.
                       ''',
                    length_var_name: 0,
                    'marks': 0
                }
                final_score = final_score + result1['marks']
                result_dict['responsive_test'] = result1
                print('except worked')