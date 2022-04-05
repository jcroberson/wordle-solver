#########################           IMPORTS            #########################
from selenium.webdriver.common.by import By
from selenium import webdriver
from random import randint
import keyboard, time, csv
import numpy as np
#####################           RETRIEVING BANK           ######################
def retrieve_bank():
    """
    Loads in word bank as a list from a csv
    Outputs:
        word_bank - list: a list of all possible answer words
    """
    with open('PATH TO BANK 2') as file:
        reader = csv.reader(file)
        word_bank = list(reader)[0]
    return word_bank
#######################           TYPING WORD           ########################
def write_word(word: str):
    """
    Writes word and presses enter
    Inputs:
        word - string: the word to write
    """
    delay = 0.05 # delay between letters in seconds
    for char in word:
        keyboard.press_and_release(char)
        time.sleep(delay)
    keyboard.press_and_release('enter')
    time.sleep(delay)
######################           GETTING SCORES           ######################
def get_scores(scores: np.array, row: int):
    """
    Retrieves results for a certain word input on the website
    Inputs:
        scores - np.array: array to fill with scores
        row - int: which row to fill
    Outputs:
        scores - np.array: array filled with scores from specified row
    """
    let_array = np.array(driver.find_elements(By.TAG_NAME, 'span')).reshape(6,5)
    for letter in range(len(let_array[row])):
        if ('green' in let_array[row][letter].get_attribute("class")):
            scores[row, letter] = 2
        elif('yellow' in let_array[row][letter].get_attribute("class")):
            scores[row, letter] = 1
        else: 
            scores[row, letter] = 0
    return scores
#####################           WORD COMPARISON           ######################
def score_filter(word: str, scores: list, values: list):
    result = ""
    for value in values:
        for i in range(len(scores)):
            if scores[i] == value:
                result += word[i]
    return result

def two_compare(standard: str, contender: str, score: np.array):
    for index in np.where(score == 2)[0]:
        if standard[index] != contender[index]:
            return False
    return True

def one_compare(standard: str, contender: str, score: np.array):
    for index in np.where(score == 1)[0]:
        if not(standard[index] in contender) or standard[index] == contender[index]: # if it is present
            return False
        non_two_chars = score_filter(contender, score, [0, 1]) 
        if not(standard[index] in non_two_chars):# and not where a 2 is
            return False
    return True

def zero_compare(standard: str, contender: str, score: np.array):
    for index in np.where(score == 0)[0]: 
        # case when letter is present but 1 or 2
        if standard[index] in score_filter(standard, score, [1, 2]):
            if standard[index] == contender[index]:
                return False
        else:
            if standard[index] in contender: # if contender contains letter
                return False
    return True
####################           NARROWING ANSWERS           #####################
def clear_dross(guess: str, score: np.array, bank: list):
    bank_buffer = []
    for word in bank:
        if two_compare(guess, word, score):
            if one_compare(guess, word, score):
                if zero_compare(guess, word, score):
                    bank_buffer.append(word)
    return bank_buffer
#####################           OPENING WEBPAGE           ######################
# configured for Firefox
driver = webdriver.Firefox(
    executable_path = r'PATH TO DRIVER')
driver.get("https://octokatherine.github.io/word-master/")
##################           ESTABLISHING VARIABLES           ##################
solved = False
iteration = 0
scores = np.zeros([6, 5])
word_bank = retrieve_bank()
#########################           SOLVING           ##########################
keyboard.wait('esc')
for i in range(25):
    solved = False
    iteration = 0
    scores = np.zeros([6, 5])
    answers = word_bank.copy()
    while not solved and iteration <= 5:
        guess = answers[randint(0, len(answers)-1)]
        write_word(guess)
        scores = get_scores(scores, iteration)
        if scores[iteration].sum() == 10:
            print("won")
            break
        answers = clear_dross(guess, scores[iteration], answers)
        iteration += 1

    for i in range(2):
        keyboard.press_and_release('enter')
        time.sleep(1)
