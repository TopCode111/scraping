import requests
from bs4 import BeautifulSoup
import xlsxwriter as xls
result = requests.get('https://www.freelancer.com/messages/thread/122992513')
print(result.status_code)
print(result.headers)
src = result.text
print(src.title())

