import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
import numpy as np

Directory_Path = 'E:\\Arman\\Text Classification'

def writer(data, filename, type = 'string'):
    parent_dir = os.path.join(Directory_Path, 'temporary')
    if type == 'string':
        with open(os.path.join(parent_dir, filename), "w", encoding='utf-8') as f:
            for item in data:
                f.write('%s' % item)
    if type == 'int':
        with open(os.path.join(parent_dir, filename), "w") as f:
            for item in data:
                f.write('%d\n' % item)



corpus = []
labels = []

with open(os.path.join(Directory_Path,'offensive.txt'), "r", encoding="utf-8") as f:
    for line in f.readlines():
        if line != '\n':
            corpus.append(line)
            labels.append(1)

with open(os.path.join(Directory_Path,'nonoffensive.txt'), "r", encoding="utf-8") as f:
    for line in f.readlines():
        if line != '\n':
            corpus.append(line)
            labels.append(0)


x_train, x_test, y_train, y_test = train_test_split(np.array(corpus), np.array(labels), test_size=0.2)

vectorizer = TfidfVectorizer(encoding='utf-8')
x_train_tfidf = vectorizer.fit_transform(x_train)
x_test_tfidf = vectorizer.transform(x_test)

clf = svm.LinearSVC()
clf.fit(x_train_tfidf, y_train)

y_test_predicted = clf.predict(x_test_tfidf)

writer(x_train, 'x_train.txt')
writer(y_train, 'y_train.txt', type='int')
writer(x_test, 'x_test.txt')
writer(y_test, 'y_test.txt', type='int')
writer(y_test_predicted, 'y_test_predicted.txt', type='int')

score = clf.score(x_test_tfidf, y_test)

print(score)