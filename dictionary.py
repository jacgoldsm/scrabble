import requests
import os


fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")

try:
    with open(fp, "r") as f:
        words = f.read().split("\n")
except FileNotFoundError:
    all_words = (
        requests.get(
            "https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt"
        ).content
    ).decode("UTF-8")
    with open(fp, "w") as f:
        f.write(all_words)
    words = set(all_words.split("\n"))


def is_valid_word(word):
    return word.upper() in words


class WordNotFoundError(Exception):
    pass
