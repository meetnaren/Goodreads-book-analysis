from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

from requests import get

#Sometimes not including the header results in a failed response
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8'}

BASE_URL='https://www.goodreads.com'
LIST_URL='https://www.goodreads.com/list/show/1.Best_Books_Ever'
#LIST_URL='https://www.goodreads.com/list/best_of_year/2018?id=119307.Best_books_of_2018'

books={'URL':[]}

#the no. of pages this list has
num_pages=557

for i in range(1, num_pages):
  #time.sleep(120) #make sure you give enough time between page loads to not avoid server overload
  print(f'Reading page {i}')
  list_page_url=f'{LIST_URL}&page={i}'
  list_page=get(list_page_url, headers=hdr)
  list_soup = BeautifulSoup(list_page.content, 'html.parser')
  book_table=list_soup.find('table', attrs={'class':'tableList js-dataTooltip'})
  rows=book_table.find_all('tr')
  books['URL']+=[BASE_URL+r.find('a', attrs={'class':'bookTitle'}).attrs['href'] for r in rows]

books_df=pd.DataFrame.from_dict(books)
books_df.to_csv('books.csv')