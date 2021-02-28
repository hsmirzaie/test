import os

Directory_Path = 'E:\\Arman\\Text Classification\\temporary'


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

def reader(filename, type = 'string'):
    data = []
    if type == 'string':
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                data.append(line)
    if type == 'int':
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                data.append(int(line[:-1]))
    return data


x_train = reader(os.path.join(Directory_Path,'x_train.txt'))
y_train = reader(os.path.join(Directory_Path,'y_train.txt'), type='int')
x_test = reader(os.path.join(Directory_Path,'x_test.txt'))
y_test = reader(os.path.join(Directory_Path,'y_test.txt'), type='int')
y_test_predicted = reader(os.path.join(Directory_Path,'y_test_predicted.txt'), type='int')


Mislabeled = [(i, x_test[i], y_test[i]) for i in range(len(y_test)) if y_test[i] != y_test_predicted[i]]
print(f'len(Mislabeled)= {len(Mislabeled)}')

positive = [(i, j) for (i, j, k) in Mislabeled if k==1]
negative = [(i, j) for (i, j, k) in Mislabeled if k==0]

#false positive
untruly_offensive = []

# false negative
untruly_nonoffensive = []

to_remove = []

for index in untruly_offensive:
    y_test[index] = 0

for index in untruly_nonoffensive:
    y_test[index] = 1

y_test = [j for i, j in enumerate(y_test) if not i in to_remove]
y_test_predicted = [j for i, j in enumerate(y_test_predicted) if not i in to_remove]
x_test =  [j for i, j in enumerate(x_test) if not i in to_remove]

Mislabeled = [(i, x_test[i], y_test[i]) for i in range(len(y_test)) if y_test[i] != y_test_predicted[i]]

print(f'len(Mislabeled)= {len(Mislabeled)}')

offensive = [j for i, j in enumerate(x_train) if y_train[i]==1]
nonoffensive = [j for i, j in enumerate(x_train) if y_train[i]==0]

offensive.extend([j for i, j in enumerate(x_test) if y_test[i]==1])
nonoffensive.extend([j for i, j in enumerate(x_test) if y_test[i]==0])


offensive = list(set(offensive))
nonoffensive = list(set(nonoffensive))

print(f'len(offensive)= {len(offensive)}')
print(f'len(nonoffensive)= {len(nonoffensive)}')

intersection = [item for item in offensive if item in nonoffensive]

with open(os.path.join(Directory_Path,'offensive_1.txt'), "w", encoding="utf_8") as f:
    for item in offensive:
        f.write("%s" % item)

with open(os.path.join(Directory_Path,'nonoffensive.txt'), "w", encoding="utf_8") as f:
    for item in nonoffensive:
        f.write("%s" % item)

print()