import sys
import os
import pickle
import nltk
import tqdm
from preparedata import text_cleaner, tokenize

languages = {"deu", "eng", "fra", "spa", "ita"}
dictionary = {}

#absolute difference between the ranks of ngrams is added to the distance variable. if ngram does not exist in a given language, a penalty is added
def distance_calculator (language, text, dictionary):
	distance = 0
	penalty = 1e10
	currentdictionary = dictionary[language]
	for key in text.keys():
		if key in currentdictionary:
			x1 = currentdictionary[key]
			x2 = text[key]
			distance += abs(x1 - x2)
		else:		
			distance += penalty
	return distance

#text is tokenized (similar to preprocessing) and distance is calculated between the text and all the languages in the dictionary. the language with the least distance is predicted as the language of the text.
def identify ():
	f = open ("./data/language_dictionary", "rb")
	dictionary = pickle.load(f)
	file_path = input ("Enter the path of the text file for which the language is to be identified: ")
	assert os.path.exists(file_path), "Could not find file at " + str(file_path)
	f = open (file_path, "r+")
	input_text = f.read()
	input_text = text_cleaner(input_text)
	tokens = nltk.tokenize.word_tokenize (input_text)
	input_table = tokenize (tokens)
	distance = {}
	print ("Calculating distances...")
	for language in dictionary.keys():
		distance[language] = distance_calculator(language, input_table, dictionary)
	language = ""
	minimum_distance = 1e18
	for lang in dictionary.keys():
		if distance[lang] < minimum_distance:
			language = lang
			minimum_distance = distance[lang]
	print ("The input language is " + language)
