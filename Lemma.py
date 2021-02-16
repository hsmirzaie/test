import os
from hazm import Lemmatizer
from parsivar import FindStems
import re

def extract_data(paths):
    inputs = []
    labels = []
    for path in paths:
        input_data = open(path, "r", encoding="utf-8").read()
        for sentence in input_data.strip().split("\n\n"):
            input = []
            label = []
            tokens = sentence.strip().split("\n")
            for token in tokens:
                components = token.strip().split("\t")
                input.append((components[1],components[3]))
                label.append(components[2])
            inputs.append(input)
            labels.append(label)
    return inputs,labels


def Evaluate_lemmatizer(inputs, labels, lib='hazm'):
    predicted_labels_with_pos = []
    predicted_labels_no_pos = []

    if lib == 'hazm':
        lemmatizer = Lemmatizer()
        for sentence in inputs:
            sent_labels_with_pos = []
            sent_labels_no_pos = []
            for (word, pos) in sentence:
                sent_labels_with_pos.append(lemmatizer.lemmatize(word, pos))
                sent_labels_no_pos.append(lemmatizer.lemmatize(word))
            predicted_labels_with_pos.append(sent_labels_with_pos)
            predicted_labels_no_pos.append(sent_labels_no_pos)

    elif lib == 'parsivar':
        stemmer = FindStems()
        for sentence in inputs:
            sent_labels_with_pos = []
            sent_labels_no_pos = []
            for (word, pos) in sentence:
                sent_labels_with_pos.append(stemmer.convert_to_stem(word, pos))
                sent_labels_no_pos.append(stemmer.convert_to_stem(word))
            for i in range(len(sentence)):
                if sentence[i][1]=='V':
                    sent_labels_with_pos[i] = re.sub(r"&",r"#",sent_labels_with_pos[i])
                    sent_labels_no_pos[i] = re.sub(r"&", r"#", sent_labels_no_pos[i])

            predicted_labels_with_pos.append(sent_labels_with_pos)
            predicted_labels_no_pos.append(sent_labels_no_pos)


    precisions_with_pos = []
    precisions_no_pos = []

    for i in range(len(labels)):
        truly_labeled_with_pos = sum([predicted_labels_with_pos[i][j] == labels[i][j] for j in range(len(labels[i]))])
        truly_labeled_no_pos = sum([predicted_labels_no_pos[i][j] == labels[i][j] for j in range(len(labels[i]))])
        precision_with_pos = truly_labeled_with_pos / len(labels[i])
        precision_no_pos = truly_labeled_no_pos / len(labels[i])
        precisions_with_pos.append(precision_with_pos)
        precisions_no_pos.append(precision_no_pos)

    precision_with_pos = sum(precisions_with_pos) / len(precisions_with_pos)
    precision_no_pos = sum(precisions_no_pos) / len(precisions_no_pos)
    return (precision_with_pos,precision_no_pos)

Directory_Path = 'E:\\Arman\\Persian NLP toolkit\\Lemma_PerDT'
train_Filename = 'train.conll.txt'
dev_Filename = 'dev.conll.txt'
test_Filename = 'test.conll.txt'

paths = []
paths.append(os.path.join(Directory_Path, train_Filename))
paths.append(os.path.join(Directory_Path, dev_Filename))
paths.append(os.path.join(Directory_Path, test_Filename))


inputs, labels = extract_data(paths)

(parsivar_precision_with_pos, parsivar_precision_no_pos) = Evaluate_lemmatizer(inputs, labels, lib = 'parsivar')
(hazm_precision_with_pos, hazm_precision_no_pos) = Evaluate_lemmatizer(inputs, labels, lib = 'hazm')

print(f'hazm_precision_with_pos = {hazm_precision_with_pos}')
print(f'parsivar_precision_with_pos = {parsivar_precision_with_pos}')
print(f'hazm_precision_no_pos = {hazm_precision_no_pos}')
print(f'parsivar_precision_no_pos = {parsivar_precision_no_pos}')
