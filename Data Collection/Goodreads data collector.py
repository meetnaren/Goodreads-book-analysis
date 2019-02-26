from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time
import os

from requests import get

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8'}

if not os.path.exists('book_data.csv'):
  book_data=pd.DataFrame(columns=[
    'image_url',
    'book_title',
    'book_authors',
    'book_rating',
    'book_rating_count',
    'book_review_count',
    'book_desc',
    'book_format',
    'book_edition',
    'book_pages',
    'book_isbn',
    'genres'
  ])

  book_data.to_csv('book_data.csv')

books=pd.read_csv('books.csv')
book_data=pd.read_csv('book_data.csv')

book_rows=[]
save_every=10

for i in range(len(book_data), len(books)):
    try:
        book_URL=books.at[i, 'URL']
        book_page=get(book_URL)
        book_soup=BeautifulSoup(book_page.content, 'html.parser')

        book=dict()

        #Save the URL of the image of the book cover to be downloaded later
        image_url=book_soup.find('img', attrs={'id':'coverImage'})
        if image_url:
            book['image_url']=image_url.attrs['src']
        else:
            book['image_url']=''

        #Title of the book
        book_title=book_soup.find('h1', attrs={'id':'bookTitle'})
        if book_title:
            book['book_title']=book_title.text.replace('\n','').strip()
        else:
            book['book_title']=''
        
        print(i, book['book_title'])

        #Author(s) of the book
        book['book_authors']='|'.join([a.find('span', attrs={'itemprop':'name'}).text for a in book_soup.find_all('a', attrs={'class':'authorName'})])
        
        #Rating given by users on goodreads
        book_rating=book_soup.find('span', attrs={'itemprop':'ratingValue'})
        if book_rating:
            book['book_rating']=book_rating.text.replace('\n','').strip()
        else:
            book['book_rating']=''
        book['book_rating_count']=book_soup.find('meta', attrs={'itemprop':'ratingCount'})['content']

        #No. of reviews for the book
        book['book_review_count']=book_soup.find('meta', attrs={'itemprop':'reviewCount'})['content']

        #A short description of the book, usually found on the back or inside cover of the book. Also called a blurb
        book_desc=book_soup.find('div', attrs={'class':'readable stacked'})
        if book_desc:
            book['book_desc']=book_desc.find_all('span')[-1].text
        else:
            book['book_desc']=''

        #Format of the book, e.g, paperback, hardcover, Kindle edition, etc.
        book_format=book_soup.find('div', attrs={'id':'details'}).find('span', attrs={'itemprop':'bookFormat'})
        if book_format:
            book['book_format']=book_format.text
        else:
            book['book_format']=''
        
        #Edition of the book
        book_edition=book_soup.find('div', attrs={'id':'details'}).find('span', attrs={'itemprop':'bookEdition'})
        if book_edition:
            book['book_edition']=book_edition.text
        else:
            book['book_edition']=''

        #No. of pages in the book
        book_pages=book_soup.find('div', attrs={'id':'details'}).find('span', attrs={'itemprop':'numberOfPages'})
        if book_pages:
            book['book_pages']=book_pages.text
        else:
            book['book_pages']=''
        
        #ISBN code of the book
        book_isbn=book_soup.find('div', attrs={'id':'bookDataBox'}).find('span', attrs={'itemprop':'isbn'})
        if book_isbn:
            book['book_isbn']=book_isbn.text
        else:
            book['book_isbn']=''

        #List of genres that the book belongs to. User supplied data.
        genres_list=book_soup.find_all('a', attrs={'class':'actionLinkLite bookPageGenreLink'})
        book['genres']='|'.join([i.text for i in genres_list])
        book_rows.append(book)

        if i%save_every==0:
            book_data.append(pd.DataFrame.from_dict(book_rows)).to_csv('book_data.csv', index=False)
            book_rows=[]
    except:
        book_data.append(pd.DataFrame.from_dict(book_rows)).to_csv('book_data.csv', index=False)
        book_rows=[]