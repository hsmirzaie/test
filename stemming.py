# from parsivar import FindStems
# my_stemmer = FindStems()
# print(my_stemmer.convert_to_stem('درافتادن'))

# from hazm import Stemmer
# stemmer = Stemmer()
# print(stemmer.stem('کتاب‌ها'))

from hazm import Lemmatizer
lemmatizer = Lemmatizer()
print(lemmatizer.lemmatize("آبادگری"))