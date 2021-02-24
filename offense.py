import os
import hazm
import re
from collections import Counter
import pandas as pd
import codecs
#import parsivar

#normalizer = parsivar.Normalizer()
normalizer = hazm.Normalizer()
Directory_Path = 'E:\\Arman\\Text Classification'



def clean(path):

    with open(path, "r", encoding="utf_8") as f:
        lines = f.readlines()

    normalized_lines = [normalizer.normalize(line) for line in lines]
    cleaned = []

    for line in normalized_lines:
        # line = normalizer.normalize(line)
        line = re.sub(r"[a-zA-Z0-9]", r"", line)
        line = re.sub(r"[^\u0600-\u06FF\u200c \s_#]", r"", line)
        line = re.sub(r"[#_]", r" ", line)
        line = re.sub(r"[\u06f0-\u06f9]", r"", line)
        line = re.sub(r"  +", r" ", line)

        cleaned.append(line)

    return cleaned

flatten = lambda t: [item for sublist in t for item in sublist]

# verbal_filename = 'persian-stopwords\\verbal'
# nonverbal_filename = 'persian-stopwords\\nonverbal'
persian_filename = 'persian-stopwords\\persian'
# verbal_stop = [normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,verbal_filename), encoding='utf-8').read().split('\n') if w]
# non_verbal_stop = [normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,nonverbal_filename), encoding='utf-8').read().split('\n') if w]
persian_stop = sorted(list(set([normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,persian_filename), encoding='utf-8').read().split('\n') if w])))
stopwords = persian_stop

"""
offensive_lexicon = []
with open(os.path.join(Directory_Path,'offensive_lexicon.txt'), "r", encoding="utf_8") as f:
    for line in f.readlines():
        offensive_lexicon.append(line[:-1])

cleaned = clean(os.path.join(Directory_Path,'bad.txt'))


bad_tokenized = [hazm.word_tokenize(line) for line in cleaned]

bad_vocabs = [vocab for vocab in flatten(bad_tokenized) if not vocab in stopwords]
bad_counter = Counter(bad_vocabs)
bad_vocabs = [vocab for vocab in bad_counter.keys() if bad_counter[vocab] > 300]


frequency = {}

for i, vocab in enumerate(bad_vocabs):
    if i % 500 == 0: print(i)
    if vocab not in frequency.keys():
        frequency[vocab] = 0
    for sentence in bad_tokenized:
        if vocab in sentence:
            frequency[vocab] += 1

print(f'len(frequency)= {len(frequency)}')

frequency = {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}
# pd.DataFrame.from_dict(data=frequency, orient='index').to_csv(os.path.join(Directory_Path,'sent_bad.csv'), sep='\t', header=False)


bad_data = []
for vocab in offensive_lexicon:
    start = len(bad_data)
    print(f'start= {start} \t vocab= {vocab}')
    for sentence in cleaned:
        if vocab in hazm.word_tokenize(sentence):
            if len(bad_data) - start <= frequency[vocab]//6:
                bad_data.append(sentence)

print(f'len(bad_data)= {len(bad_data)}')

with open(os.path.join(Directory_Path,'offensive.txt'), "w", encoding="utf_8") as f:
    for item in bad_data:
        f.write("%s\n" % item)

"""



cleaned = clean(os.path.join(Directory_Path,'good.txt'))

with open(os.path.join(Directory_Path,'nonoffensive.txt'), "w", encoding="utf_8") as f:
    for item in cleaned:
        f.write("%s\n" % item)


"""

good_tokenized = [hazm.word_tokenize(line) for line in cleaned]
good_vocabs = [vocab for vocab in flatten(good_tokenized) if not vocab in stopwords]
good_counter = Counter(good_vocabs)
good_vocabs = [vocab for vocab in good_counter.keys() if good_counter[vocab] > 300]



frequency = {}

for i, vocab in enumerate(good_vocabs):
    if i % 500 == 0: print(i)
    if vocab not in frequency.keys():
        frequency[vocab] = 0
    for sentence in good_tokenized:
        if vocab in sentence:
            frequency[vocab] += 1

print(len(frequency))

frequency = {k: v for k,v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}
pd.DataFrame.from_dict(data=frequency, orient='index').to_csv(os.path.join(Directory_Path,'sent_good.csv'), sep='\t', header=False)

"""

"""

cleaned = clean(os.path.join(Directory_Path,'good.txt'))
print(len(cleaned))
good_vocabs = []
for line in cleaned:
    line = hazm.word_tokenize(line)
    good_vocabs.extend(line)


good_vocabs = list(set([vocab for vocab in good_vocabs if not vocab in stopwords]))


good_counter = Counter(good_vocabs)
Total = sum(good_counter.values())
good_counter = {k: round(100*v/Total, 3) for k,v in sorted(good_counter.items(), key=lambda item: item[1], reverse=True)}

pd.DataFrame.from_dict(data=good_counter, orient='index').to_csv(os.path.join(Directory_Path,'good.csv'),sep='\t', header=False)


"""

