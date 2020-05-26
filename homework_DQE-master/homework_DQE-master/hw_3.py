import typing
import functools
from itertools import chain
from typing import List
from collections import Counter

T = typing.TypeVar('T', str, float)
already_found_letters = []
suitable_words_global = []


def game():
    attempts = 0
    template = ""
    guessed_word = 0
    right_letter = ""

    show_words()
    file_read()
    while not guessed_word or template.isalpha() or not suitable_words_global:
        template = get_template(template, right_letter)
        suitable_words = determine_words_by_template(template)
        letters = most_likely_letter(suitable_words)  # list of most likely variables
        attempt, right_letter = acceptance_of_player(template, letters)
        attempts += attempt
        guessed_word = try_to_guess(suitable_words, right_letter, template)
    summary(attempts, guessed_word)
    if not guessed_word:
        wrong_word()


def show_words():
    with open("D:\\DQE\\words.txt", "r") as f:
        data = f.read()
    print(data)


def initial_template_of_word() -> str:
    template = input("Show number of letters in your word (example: '_____'):  ")
    return template


def acceptance_of_player(letters: str):  # return attempts
    right_letter = ""
    attempts = 0
    for letter in letters:
        print(f"\nIn your word, with {letter[1]} probability, letter '{letter[0]}' might be!")
        rightness = input("Is it right? (Yes - 1, No - 0) ")
        while not rightness.isdigit():
            rightness = input("Incorrect answer. Make a choice: (Yes - 1, No - 0) ")
        attempts += 1
        if int(rightness) == 1:
            right_letter = letter[0]
            break
    return attempts, right_letter


def check_template(tested: str, etalon: str, letter: str)-> int:
    if len(tested) != len(etalon):
        return 0
    for i in range(len(tested)):
        if tested[i] != etalon[i] and tested[i] != letter:
            return 0
    return 1


def get_template(template: str, right_letter: str) -> str:
    if template == "":
        return initial_template_of_word()
    else:
        temp = input(f"Please show where {right_letter} is/are. Your previous template: '{template}':  ")
        while not check_template(temp, template, right_letter):
            temp = input(f"You entered wrong row, check it again. "
                         f"Your previous row was {template}, it shouldn't be changed:  ")
        return temp


def file_read():
    f = open("D:\\DQE\\words.txt", "r")
    global suitable_words_global
    suitable_words_global = f.read().lower().replace("'", "'").split()
    f.close()


def determine_words_by_template(template: str) -> tuple:  # return suitable words
    global suitable_words_global, already_found_letters
    suitable_words = suitable_words_global
    suitable_words = determine_by_letters(template, suitable_words)
    suitable_words_global = suitable_words
    already_found_letters = already_found_letters + list(set(chain.from_iterable(template.replace('_', ' ').strip())))
    return tuple(suitable_words)


def determine_by_letters(template: str, suitable_words: list) -> list:
    if template.replace('_', ' ').isspace():
        length = len(template)
        suitable_words = [word for word in suitable_words if len(word) == length]
    for i in range(len(template)):
        if (template[i].isalpha() or template[i] == "'") and template[i] not in already_found_letters:
            suitable_words = find_word_by_letter(i, template[i], suitable_words)
    return suitable_words


def find_word_by_letter(index: int, letter: str, source: list) -> tuple:
    right_list = []
    for word in source:
        if len(word) <= index:
            continue
        if word[index] == letter:
            right_list.append(word)
    return tuple(right_list)  # for being immutable


def most_likely_letter(checklist: tuple) -> tuple:  # specified type  List('T', str, float)
    all_letters = list(chain.from_iterable(checklist))  # take all letters from source
    total_letters_count = len(all_letters)
    letters = only_distinct_letters(all_letters)
    count = Counter(letters)
    probable_letters = probability_of_occurring(count, total_letters_count)
    return probable_letters


def only_distinct_letters(letters: str) -> str:
    global already_found_letters
    letters = [let for let in letters if let not in already_found_letters]
    return letters


def probability_of_occurring(count: Counter, total_letters_count: int) -> tuple:
    list_of_probability = []
    for letter, frequency in dict(count.most_common()).items():  # sort counter by values and change in dictionary
        probability = round(frequency / total_letters_count * 100, 2)
        list_of_probability.append([letter, str(probability) + '%'])
    return tuple(list_of_probability)


def try_to_guess(suitable_words: tuple, letter: str, template: str) -> str:  # return guessed word or nothing
    if len(suitable_words) == 1:
        return suitable_words[0]
    if template.count('_') == 1:
        return template.replace('_', letter)


def summary(attempts: int, guessed_word: str):
    print(f'\nYour word is "{guessed_word}". I coped with it in {attempts} attempts ;)')


def wrong_word():
    print("Your word isn't in our dictionary. Play again :(")


game()