from collections import Counter
from itertools import chain
import re
import typing

suitable_words_global = []
probable_letters = list("abcdefghhijklmnopqrstuvwxyz'")


def game():
    print("--HANGMAN--")
    attempts = 0
    template = ""
    guessed_word = 0
    right_letter = ""

    while not guessed_word or template.isalpha() or not suitable_words_global:
        template = get_template(template, right_letter)
        suitable_words = determine_words_by_template(template)
        print('\n' + str(len(suitable_words)) + ' suitable words')
        letters = most_likely_letter(suitable_words)  # list of most likely letters
        attempt, right_letter = acceptance_of_player(letters)
        if not attempt:
            wrong_word()
            return 0
        attempts += attempt
        guessed_word = try_to_guess(suitable_words, right_letter, template)
    summary(attempts, guessed_word)
    if not guessed_word:
        wrong_word()


def initial_template_of_word() -> str:
    """Початкове задання довжини файлу"""
    template = input("Show number of letters in your word (example: '_____'):  ")
    while not template.replace('_', ' ').isspace():
        template = input("\n--This sentence can contain only '_' symbol"
                         "\nTry to enter again (example: '_____'):  ")
    file_read(len(template))
    return template


def acceptance_of_player(letters: tuple):  # return attempts
    """Підтвердження користувачем заданої літери
       Проходження всіх можливих літер"""
    global probable_letters
    right_letter = ""
    attempts = 0
    rightness = 0
    for letter in letters:
        print(f"\nIn your word, with {letter[1]} probability, letter '{letter[0]}' might be!")
        rightness = input("Is it right? (Yes - 1, No - 0) ")
        while not rightness.isdigit():
            rightness = input("Incorrect answer. Make a choice: (Yes - 1, No - 0) ")
        attempts += 1
        if int(rightness) == 1:
            right_letter = letter[0]
            break
        else:
            probable_letters.remove(letter[0])
    if rightness == '0':
        return 0, 0
    return attempts, right_letter


def check_template(tested: str, etalon: str, letter: str) -> int:
    """Перевірка чи заданий користувачем шаблон є валідний
       звіряється на кількість символів та порівнюється з попередньо заданим шаблоноим"""
    if len(tested) != len(etalon):
        return 0
    for i in range(len(tested)):
        if tested[i] != etalon[i] and tested[i] != letter:
            return 0
    return 1


def get_template(template: str, right_letter: str) -> str:
    """Задання шаблону"""
    if template == "":
        return initial_template_of_word()
    else:
        temp = input(f"Please show where {right_letter} is/are. Your previous template: '{template}':  ")
        while not check_template(temp, template, right_letter):
            temp = input(f"You entered wrong row, check it again. "
                         f"Your previous row was {template}, it shouldn't be changed:  ")
        return temp


def file_read(length):
    f = open("D:\\DQE\\words.txt", "r")
    global suitable_words_global
    suitable_words_global = f.read().lower().split()
    suitable_words_global = [word for word in suitable_words_global if len(word) == length]
    f.close()


def determine_words_by_template(template: str) -> tuple:  # return suitable words
    """Визначення ймовірних слів, шляхом комунікації з глобальними змінними та їх переписання"""
    global suitable_words_global, probable_letters
    suitable_words = list(set(suitable_words_global))
    suitable_words = re.findall(template.replace('_', '.'), ''.join(suitable_words))
    suitable_words_global = suitable_words

    list_of_used_letters = list(set(chain.from_iterable(template.replace('_', ' ').strip())))
    probable_letters = [let for let in probable_letters if let not in list_of_used_letters]
    # deleting already used letters
    return tuple(suitable_words)


def most_likely_letter(checklist: tuple) -> typing.Tuple[str, int]:
    """Повертає літери з ймовірністю трапляння"""
    all_letters = list(chain.from_iterable(checklist))  # take all letters from source
    letters = only_distinct_letters(all_letters)
    total_letters_count = len(letters)
    probable_letters = probability_of_occurring(Counter(letters), total_letters_count)
    return probable_letters


def only_distinct_letters(letters: list) -> list:
    """Зі списку букв забираємо всі букви, що не можуть трапитись"""
    global already_found_letters
    letters = [let for let in letters if let in probable_letters]
    return letters


def probability_of_occurring(count: Counter, total_letters_count: int) -> tuple:
    """Вирахування ймовірності трапляння всіх унікальних(не використаних) букв"""
    list_of_probability = []
    for letter, frequency in dict(count.most_common()).items():  # sort counter by values and change in dictionary
        probability = round(frequency / total_letters_count * 100, 2)
        list_of_probability.append([letter, str(probability) + '%'])
    return tuple(list_of_probability)


def try_to_guess(suitable_words: tuple, letter: str, template: str) -> str:  # return guessed word or nothing
    """Спроба вгадати слово у випадку, якщо немає сенсу продовжувати"""
    if len(suitable_words) == 1:
        return suitable_words[0]
    if template.count('_') == 1:
        return template.replace('_', letter)


def summary(attempts: int, guessed_word: str):
    print(f'\nYour word is "{guessed_word}". I coped with it in {attempts} attempts ;)')


def wrong_word():
    print("Your word isn't in our dictionary. Play again :(")


if __name__ == '__main__':
    game()
