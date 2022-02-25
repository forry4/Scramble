import pandas as pd
import random
import time
from collections import Counter
from wordfreq import zipf_frequency, get_frequency_dict
import twl

dictionary = set()
words_dict = {}

def getDict():
    global dictionary
    #set imported dictionary to fit game requirements
    words = set(twl.iterator())
    words = {x for x in words if len(x)<11 and len(x) > 3 and zipf_frequency(x, 'en') > 1.5}
    print(words)
    print(len(words))
    dictionary = words
    return list(dictionary)

def scrambler(word, subwords, hidden, correct):
    #check if player has guessed all anagrams
    if correct == len(subwords):
        print(f'neato you did it and got all {correct} right!')
        print(hidden)
        return
    #scramble letters
    scrambled = list(word)
    random.shuffle(scrambled)
    scrambled = ''.join(scrambled)
    #display progress and request input
    print(f'SCRAMBLED: {scrambled.upper()}')
    print(f'HIDDEN: {hidden}')
    guess = input('GUESS OR GIVEUP: ').upper()
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
    #end game if player gives up
    if guess == 'GIVEUP':
        print(f'YOU GOT {correct}/{len(subwords)}')
        print(hidden)
        print(subwords)
        return
    #check if word is anagram
    if guess in subwords:
        #check if it hasnt been guessed yet
        if guess not in hidden:
            print(f'YOU GUESSED {guess}')
            #fill in hidden word array with guess
            hidden[subwords.index(guess)] = guess
            scrambler(word, subwords, hidden, correct + 1)
        else:
            print(f'YOU ALREADY GUESSED {guess}')
            scrambler(word, subwords, hidden, correct)
    else:
        print(f'{guess} IS NOT A WORD')
        scrambler(word, subwords, hidden, correct)

def return_anagrams(letters: str) -> list:

    global dictionary
    assert isinstance(letters, str)
    letters = letters.lower()
    letters_count = Counter(letters)
    anagrams = set()

    for word in dictionary:
        # Check if all the unique letters in word are in the
        # scrambled letters
        if not set(word) - set(letters):
            check_word = set()
            # Check if the count of each letter is less than or equal
            # to the count of that letter in scrambled letter input
            for k, v in Counter(word).items():
                if v <= letters_count[k]:
                    check_word.add(k)
            # Check if check_words is exactly equal to the unique letters
            # in the word of dictionary
            if check_word == set(word):
                anagrams.add(word)
                
    return sorted(list(anagrams), key=lambda x: len(x))

if __name__ == '__main__':
    #get full dictionary
    dictionary = getDict()
    print(dictionary)
    print(len(dictionary))
    word = ''
    subwords = []
    #look for random valid word that fits requirements to be playable
    for i in enumerate(dictionary):
        rand = random.randint(0,len(dictionary)-1)
        word = dictionary[rand]
        print(f'rand: {rand}, word: {word}, len: {len(word)}, freq: {zipf_frequency(word, "en")}')
        #check length and common-ness requirement
        if len(word) > 4 and zipf_frequency(word, 'en') > 3.5:
            temp = return_anagrams(word)
            print(f'anagrams: {len(temp)}')
            #check to see if it has a good number of anagrams
            if len(temp) > 7 and len(temp) < 31:
                #shuffle, sort, and make it uppercase
                random.shuffle(temp)
                temp = sorted(temp, key=len)
                temp = [x.upper() for x in temp]
                subwords = temp
                hidden = subwords.copy()
                break
    #make list of hidden words
    for i, words in enumerate(hidden):
        hidden[i] = '_'*len(hidden[i])
    print(f'word selected: {word}')
    print(f'subwords selected: {subwords}')
    print(f'hidden word: {hidden}\n\n\n\n\n\n\n\n\n\n\n')
    start = time.time()
    scrambler(word, subwords, hidden, 0)
    stop = time.time()
    print(f"Time Taken: {round(stop - start, 2)} seconds")
