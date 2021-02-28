import os
from hazm import *
lemmatizer = Lemmatizer()

list = [
'سکس',
'سکسی',
'سکصی',
'سسکی',
'دیوس',
'دیوث',
'دیوص',
'کون',
'کونیا',
'کونیاش',
'کیون',
'کیر',
'کیرمو',
'کیرتو',
'کیرشو',
'کس',
'کص',
'کسکش',
'کصکش',
'کوس',
'جنس',
'اشغال',
'کثافت',
'واژن',
'جنده',
'مادرجنده',
'خارجنده',
'خارکسده',
'خارکصده',
'خارکوسده',
'خل',
'تحریک',
'خر',
'الت',
'جون',
'پاره',
'تناسلی',
'سگ',
'ارضا',
'ارگاسم',
'خراب',
'جق',
'ساک',
'لخت',
'ممه',
'خفه',
'تخم',
'احمق',
'کودن',
'دخول',
'کاندوم',
'چل',
'حشر',
'شهوت',
'تلمبه',
'انزال',
'لیس',
'ننه',
'ابم',
'بیشعور',
'مقاربت',
'آمیزش',
'مقعد',
'کلیتوریس',
'اسپرم'
]
Directory_Path = 'E:\\Arman\\Text Classification'
# with open(os.path.join(Directory_Path,'offensive_lexicon.txt'), "w", encoding="utf_8") as f:
    # f.write("\n".join(item for item in list))

with open(os.path.join(Directory_Path,'offensive_lexicon.txt'), "w", encoding="utf_8") as f:
    for item in list:
        f.write("%s\n" % item)

list = []
with open(os.path.join(Directory_Path,'offensive_lexicon.txt'), "r", encoding="utf_8") as f:
    for line in f.readlines():
        list.append(line[:-1])

lemmas = [lemmatizer.lemmatize(i) for i in list]

a = [list[i] for i in range(len(list)) if lemmas[i]!=list[i]]
print(len(list))
