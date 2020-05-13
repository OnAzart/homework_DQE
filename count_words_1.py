from collections import Counter
import re
from sys import argv


script, file_name = argv

def count_words(file_name):
    try:
        f = open(file_name, 'r')
        book_content = f.read()
        f.close()
    except (FileNotFoundError, IOError):
            print('S O S\nFile name is not valid!\nTry to launch again')
    else:
        list_words = re.findall(r'\w+', 
            book_content.lower())

        c = Counter(list_words)
        c = dict(sorted(c.items()))
        for key, value in c.items():
               print(f"{key} - {value} times")

count_words(file_name)
