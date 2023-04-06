import itertools
import string
import requests

class WordleSolver:
    def __init__(self):
        self.__arr_all_words: list = requests.get('https://slc.is/data/wordles.txt').text.split("\n")
        self.arr_possible_letters: list = list(string.ascii_lowercase)
        self.dict_decided: dict = {1:"", 2: "", 3: "", 4: "", 5: ""}
        self.arr_yellows: list = []
        self.__arr_answers: list = []
    
    @property
    def answers(self):
        return self.__arr_answers
    
    def __checkIfCorrectPosition(self, position: int):
        if not 1 <= position <= 5:
            raise ValueError("Positionは1~5でなければなりません") 

    def __evaluateWord(self, arr_evaled_word: list):
        for dict_yellow in self.arr_yellows:
            yellow_letter_place = list(dict_yellow.keys())[0]
            yellow_letter = dict_yellow[yellow_letter_place] 
            ifPossiblePosition = not (arr_evaled_word[yellow_letter_place - 1] == yellow_letter)
            ifYellowLetterUsed = (yellow_letter in arr_evaled_word)
            if not ifPossiblePosition or not ifYellowLetterUsed:
                return 
        word = ''.join(arr_evaled_word)
        if word in self.__arr_all_words:
            self.__arr_answers.append(word)

    def setGreenLetter(self, letter: str, position: int):
        self.__checkIfCorrectPosition(position)
        self.dict_decided[position] = letter
        
    def setYellowLetter(self, letter: str, position: int):
        self.__checkIfCorrectPosition(position)
        self.arr_yellows.append({position: letter})
    
    def setGrayLetters(self, letter: str):
        self.arr_possible_letters = [i for i in self.arr_possible_letters if i not in list(letter)]
            
    def solveWordle(self):
        arr_undef_positions = [position for position, letter in self.dict_decided.items() if letter == ""]  
        arr_candidate_part_words = list(itertools.product(self.arr_possible_letters, repeat=len(arr_undef_positions)))
        for arr_part_word in arr_candidate_part_words:
            dict_trial_letters = dict(zip(arr_undef_positions, arr_part_word))
            dict_evaled_word = {**self.dict_decided, **dict_trial_letters}
            arr_evaled_word = list(dict_evaled_word.values())
            self.__evaluateWord(arr_evaled_word)