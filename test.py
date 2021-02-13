import os
import pandas as pd
import re
PATH_WIKI_XML = 'E:\\Arman\\venv\\'
FILENAME_ARTICLES = 'articles.csv'
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)
cols = ['id', 'title', 'article']
data = pd.read_csv(pathArticles, nrows=100, usecols=cols)
#print(data.head())
raw_text = data['article'].iloc[90]
print(raw_text)


# add a coment