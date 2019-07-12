import requests
from bs4 import BeautifulSoup
import xlsxwriter as xls
result = requests.get('https://www.freelancer.com/messages/thread/122992513')
print(result.status_code)
print(result.headers)
src = result.text
print(src.title())

workbook = xls.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A',20)
worksheet.write('A1','python1')
worksheet.write('A2','python2')
workbook.close()
