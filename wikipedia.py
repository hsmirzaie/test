import xml.etree.ElementTree as ET
import codecs
import csv
import time
import os


PATH_WIKI_XML = 'E:\\Arman\\venv\\'
FILENAME_WIKI = 'fawiki-20210201-pages-articles-multistream.xml'
FILENAME_ARTICLES = 'articles.csv'

ENCODING = "utf-8"


# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    idx = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


pathWikiXML = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
pathArticles = os.path.join(PATH_WIKI_XML, FILENAME_ARTICLES)


totalCount = 0
articleCount = 0

title = None
start_time = time.time()

with codecs.open(pathArticles, "w", ENCODING) as articlesFH:
    articlesWriter = csv.writer(articlesFH, quoting=csv.QUOTE_MINIMAL)
    articlesWriter.writerow(['id', 'title', 'article'])

    for event, elem in ET.iterparse(pathWikiXML, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)

        if event == 'start':
            if tname == 'page':
                title = ''
                id = -1
                inrevision = False

            elif tname == 'revision':
                inrevision = True
                article = ''
        else:
            if tname == 'title':
                title = elem.text
            elif tname == 'id' and not inrevision:
                id = int(elem.text)
            elif tname == 'page':
                totalCount += 1
            elif tname == 'text':
                article = elem.text
                articleCount += 1
                articlesWriter.writerow([id, title, article])

                # if totalCount > 100:
                # break

                if totalCount > 1 and (totalCount % 100000) == 0:
                    print("{:,}".format(totalCount))

            elem.clear()

elapsed_time = time.time() - start_time

print("Total pages: {:,}".format(totalCount))
print("Article pages: {:,}".format(articleCount))
print("Elapsed time: {}".format(hms_string(elapsed_time)))
