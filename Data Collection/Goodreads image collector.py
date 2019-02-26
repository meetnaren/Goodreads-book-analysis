import pandas as pd
import wget
import os

book_data=pd.read_csv('book_data.csv')
PATH='C:\\Python\\Python37-32\\Scripts\\code\\images\\'
files=os.listdir(PATH)
n=0
if len(files)>0:
    n=max([int(f[:-4]) for f in os.listdir(PATH)])+1

for i in range(n, len(book_data)):
    url=book_data.at[i, 'image_url']
    filename=f'{i}.jpg'
    if not pd.isna(url):
        wget.download(url, PATH+filename)
    if i%100==0:
        print(i)