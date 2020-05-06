from sys import argv
import re
from collections import Counter

script, file_name = argv

def count_words(file_name):
    try:
    	f=open(file_name, 'r')
    	book_content=f.read()
    	f.close()
    except (FileNotFoundError, IOError):
    		print('File name is not valid!\n Try to enter again')
    else:
        list_words=re.split(r'\s*[;,.?!-[\]{}()"\'\s]\s*', book_content.lower())

        c=Counter(list_words)
        for key, value in c.items():
                print(f"{key} {value} times")

count_words(file_name)