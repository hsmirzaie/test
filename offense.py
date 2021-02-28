import os
import hazm
import parsivar
import re
import random
from collections import Counter
import pandas as pd
import codecs


Directory_Path = 'E:\\Arman\\Text Classification'


def clean(path):

    character_refinement_patterns = [
        (r'[a-zA-Z0-9]', ''),
        (r'(\u0631){3,}', r'\1'),
        (r'(\u0648){3,}', r'\1'),
        (r'(\u0633){3,}', r'\1'),
        (r'(\u06a9){3,}', r'\1'),
        (r'(\u0627){3,}', r'\1'),
        (r'(\u06cc){3,}', r'\1'),
        (r'(\u062e){3,}', r'\1'),
        (r'(\u0645){3,}', r'\1'),
        (r'(\u0646){3,}', r'\1'),
        (r'(\u0647){3,}', r'\1'),
        (r'(\u0639){3,}', r'\1'),
        (r'(\u0634){3,}', r'\1'),
        (r'\u0622', '\u0627'),
        (r'\u0651', ''),
        (r'[^\u0600-\u06FF\u200c \s_#]', ''),
        (r'[#_]', ' '),
        (r'[\u06f0-\u06f9]', ''),
        (r'  +', ' '),
    ]
    compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]
    character_refinement_patterns = compile_patterns(character_refinement_patterns)

    with open(path, "r", encoding="utf_8") as f:
        lines = f.readlines()

    normalizer = parsivar.Normalizer()
    normalized_lines = [normalizer.normalize(line) for line in lines]
    cleaned = []

    for line in normalized_lines:

        for pattern, repl in character_refinement_patterns:
            line = pattern.sub(repl, line)

        cleaned.append(line)

    return cleaned

flatten = lambda t: [item for sublist in t for item in sublist]


normalizer = parsivar.Normalizer()
# verbal_filename = 'persian-stopwords\\verbal'
# nonverbal_filename = 'persian-stopwords\\nonverbal'
persian_filename = 'persian-stopwords\\persian'
# verbal_stop = [normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,verbal_filename), encoding='utf-8').read().split('\n') if w]
# non_verbal_stop = [normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,nonverbal_filename), encoding='utf-8').read().split('\n') if w]
persian_stop = sorted(list(set([normalizer.normalize(w) for w in codecs.open(os.path.join(Directory_Path,persian_filename), encoding='utf-8').read().split('\n') if w])))
stopwords = persian_stop




offensive_lexicon = []
with open(os.path.join(Directory_Path,'offensive_lexicon.txt'), "r", encoding="utf_8") as f:
    for line in f.readlines():
        offensive_lexicon.append(line[:-1])


cleaned = clean(os.path.join(Directory_Path,'bad.txt'))

print(f'len(cleaned)= {len(cleaned)}')
cleaned = list(set(cleaned))
print(f'len(cleaned)= {len(cleaned)}')

"""
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


"""
lemmatizer = hazm.Lemmatizer()

offensive = []
less_offensive = []

for sentence in cleaned:
    words = [lemmatizer.lemmatize(word) for word in hazm.word_tokenize(sentence)]
    #intersection = [vocab for vocab in words if vocab in offensive_lexicon]
    check = any(item in words for item in offensive_lexicon)
    if check:
        offensive.append(sentence)
    else:
        less_offensive.append(sentence)


offensive = list(set(offensive))
less_offensive = list(set(less_offensive))

"""
for vocab in offensive_lexicon:
    start = len(bad_data)
    print(f'start= {start}')
    for sentence in cleaned:

        # if vocab in hazm.word_tokenize(sentence):
            # if len(bad_data) - start <= frequency[vocab]//6:
                # bad_data.append(sentence)
        if vocab not in hazm.word_tokenize(sentence):
            bad_data.append(sentence)
            
print(f'len(bad_data)= {len(bad_data)}')

"""

random.shuffle(offensive)

with open(os.path.join(Directory_Path,'offensive_1.txt'), "w", encoding="utf_8") as f:
    for item in offensive[:len(offensive)//3]:
        f.write("%s\n" % item)

with open(os.path.join(Directory_Path,'offensive_2.txt'), "w", encoding="utf_8") as f:
    for item in offensive[len(offensive)//3:]:
        f.write("%s\n" % item)

with open(os.path.join(Directory_Path,'less_offensive.txt'), "w", encoding="utf_8") as f:
    for item in less_offensive:
        f.write("%s\n" % item)


cleaned = clean(os.path.join(Directory_Path,'good.txt'))

print(f'len(cleaned)= {len(cleaned)}')
cleaned = list(set(cleaned))
print(f'len(cleaned)= {len(cleaned)}')

nonoffensive = []

for sentence in cleaned:
    words = [lemmatizer.lemmatize(word) for word in hazm.word_tokenize(sentence)]
    check = any(item in words for item in offensive_lexicon)
    if not check:
        nonoffensive.append(sentence)

with open(os.path.join(Directory_Path,'nonoffensive.txt'), "w", encoding="utf_8") as f:
    for item in nonoffensive:
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

