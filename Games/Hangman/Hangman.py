import random
from words import words
from Hangmanvisual import lives_visual_dict
import string

def get_valid_word(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def forca():
    word = get_valid_word(words)
    letters = set(string.ascii_uppercase)
    word_letters = set(word)
    used_letters = set()
    lifes = 6

    while lifes > 0 and len(word_letters) > 0:
        if len(used_letters) == 0:
            print(lives_visual_dict[lifes])
            print(f"You have {lifes} lifes")
        else:
            print(lives_visual_dict[lifes])
            print(f"You have {lifes} lifes and already tried this letters: "," ".join(used_letters))

        display_word = [letter if letter in used_letters else '-' for letter in word]
        print("Word: ", " ".join(display_word))

        #Getting user input
        guess = input("Try a letter: ").upper()
        while guess in used_letters:
            print("Already tried this letter")
            guess = input("Try a letter: ").upper()

        if guess in letters:
            used_letters.add(guess)
            if guess in word_letters:
                word_letters.remove(guess)
            else:
                lifes = lifes - 1
                print("Letter not in the word")
        else:
            print("This is not a letter")

    #Return if the user has won or lose
    if lifes == 0:
        print(lives_visual_dict[lifes])
        print("You lost")
        print(word)
    else:
        print("You won! The word is: ",word)

forca()
