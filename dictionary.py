import requests
import os
print(os.getcwd())
try:
    with open("./words.txt", 'r') as f:
        words = f.read().split("\n")
except FileNotFoundError:
    all_words = (requests.get("https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt").content).decode('UTF-8')
    with open("./words.txt", 'w') as f:
        f.write(all_words)
    words = set(all_words.split("\n"))


def is_valid_word(word):
    return word.upper() in words

class WordNotFoundError(Exception):
    pass