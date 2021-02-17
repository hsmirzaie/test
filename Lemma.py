import os
from hazm import Lemmatizer
from parsivar import FindStems
import re
import matplotlib.pyplot as plt
import json


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
                input.append((components[1], components[3]))
                label.append(components[2])
            inputs.append(input)
            labels.append(label)
    return inputs, labels


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


    elif lib=='parsivar':
        stemmer = FindStems()
        for sentence in inputs:
            sent_labels_with_pos = []
            sent_labels_no_pos = []

            for (word, pos) in sentence:
                sent_labels_with_pos.append(stemmer.convert_to_stem(word, pos))
                sent_labels_no_pos.append(stemmer.convert_to_stem(word))

            for i in range(len(sentence)):
                if sentence[i][1] == 'V':
                    sent_labels_with_pos[i] = re.sub(r"&", r"#", sent_labels_with_pos[i])
                    sent_labels_no_pos[i] = re.sub(r"&", r"#", sent_labels_no_pos[i])

            predicted_labels_with_pos.append(sent_labels_with_pos)
            predicted_labels_no_pos.append(sent_labels_no_pos)

    precisions_with_pos = []
    precisions_no_pos = []
    all_truly_labeled_with_pos = []

    for i in range(len(labels)):
        truly_labeled_with_pos = [predicted_labels_with_pos[i][j] == labels[i][j] for j in range(len(labels[i]))]
        all_truly_labeled_with_pos.append(truly_labeled_with_pos)
        num_truly_labeled_with_pos = sum(truly_labeled_with_pos)
        truly_labeled_no_pos = [predicted_labels_no_pos[i][j] == labels[i][j] for j in range(len(labels[i]))]
        num_truly_labeled_no_pos = sum(truly_labeled_no_pos)

        precision_with_pos = num_truly_labeled_with_pos / len(labels[i])
        precision_no_pos = num_truly_labeled_no_pos / len(labels[i])
        precisions_with_pos.append(precision_with_pos)
        precisions_no_pos.append(precision_no_pos)

    per_pos = {}
    detailed_analyze = {}
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):

            if inputs[i][j][1] not in per_pos.keys():
                per_pos[inputs[i][j][1]] = {'true': 0, 'false': 0}

            if all_truly_labeled_with_pos[i][j]:
                per_pos[inputs[i][j][1]]['true'] += 1
            else:
                per_pos[inputs[i][j][1]]['false'] += 1

            if inputs[i][j][1] not in detailed_analyze.keys():
                detailed_analyze[inputs[i][j][1]] = {'true': [], 'false': []}

            if all_truly_labeled_with_pos[i][j]:
                detailed_analyze[inputs[i][j][1]]['true'].append(inputs[i][j][0])

            else:
                detailed_analyze[inputs[i][j][1]]['false'].append(inputs[i][j][0])


    accuracy_per_pos = {k: v['true']/(v['true'] + v['false']) for k, v in per_pos.items()}
    for k, v in detailed_analyze.items():
        v['true'] = set(v['true'])
        v['false'] = set(v['false'])
    precision_with_pos = sum(precisions_with_pos) / len(precisions_with_pos)
    precision_no_pos = sum(precisions_no_pos) / len(precisions_no_pos)
    return precision_with_pos, precision_no_pos, accuracy_per_pos, detailed_analyze


Directory_Path = 'E:\\Arman\\Persian NLP toolkit\\Lemma_PerDT'
train_Filename = 'train.conll.txt'
dev_Filename = 'dev.conll.txt'
test_Filename = 'test.conll.txt'

paths = [os.path.join(Directory_Path, train_Filename),
         os.path.join(Directory_Path, dev_Filename),
         os.path.join(Directory_Path, test_Filename)]

inputs, labels = extract_data(paths)

(hazm_precision_with_pos, hazm_precision_no_pos, hazm_accuracy_per_POS, hazm_detailed_analyze) = \
    Evaluate_lemmatizer(inputs, labels, lib='hazm')
(parsivar_precision_with_pos, parsivar_precision_no_pos, parsivar_accuracy_per_POS, parsivar_detailed_analyze) = \
    Evaluate_lemmatizer(inputs, labels, lib='parsivar')

print(f'hazm_precision_with_pos = {hazm_precision_with_pos}')
print(f'parsivar_precision_with_pos = {parsivar_precision_with_pos}')
print(f'hazm_precision_no_pos = {hazm_precision_no_pos}')
print(f'parsivar_precision_no_pos = {parsivar_precision_no_pos}')

"""

with open(os.path.join(Directory_Path, 'hazm_detailed_analyze.json'), 'w') as HAZM:
    json.dump(hazm_detailed_analyze, HAZM)

with open(os.path.join(Directory_Path, 'parsivar_detailed_analyze.json'), 'w') as PARSIVAR:
    json.dump(parsivar_detailed_analyze, PARSIVAR)


plt.xticks(rotation='vertical')
plt.bar(*zip(*hazm_accuracy_per_POS.items()))
plt.title('hazm_accuracy_per_POS')
plt.xlabel('POS')
plt.ylabel('accuracy')
for i, v in enumerate(hazm_accuracy_per_POS.values()):
    plt.text(i, v, str(round(v,2)), ha='center', va='bottom', fontsize='small')

plt.savefig(os.path.join(Directory_Path, 'hazm_accuracy_per_POS.png'), dpi=300, bbox_inches='tight')

plt.figure()
plt.xticks(rotation='vertical')
plt.bar(*zip(*parsivar_accuracy_per_POS.items()))
plt.title('parsivar_accuracy_per_POS')
plt.xlabel('POS')
plt.ylabel('accuracy')
for i, v in enumerate(parsivar_accuracy_per_POS.values()):
    plt.text(i, v, str(round(v,2)), ha='center', va='bottom', fontsize='small')

plt.savefig(os.path.join(Directory_Path, 'parsivar_accuracy_per_POS.png'), dpi=300, bbox_inches='tight')
"""