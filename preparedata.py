import re
import pandas as pd
import nltk
import pickle

from tqdm import tqdm

languages = ["deu", "eng", "fra", "spa", "ita"]
corpus = {}

#discarding punctuation marks and other symbols
def text_cleaner (text):	
	sent = re.sub("[^\p{Sc}\p{So}\p{Mn}\p{P}\p{Z}À-ÿ\D+']"," ",text).replace('\n','').replace('\t',' ').replace('|',' ').replace('.',' ').replace('。',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(":",' ').replace(';',' ').replace('(','').replace(')','').replace('"','').replace('!','').replace('-','').replace('*','')	
	return sent

#breaking down tokens into bigrams and trigrams, storing their frequencies, storing top 10000 most common ngrams into the dictionary by rank
def tokenize (tokens):
	for index in range(len(tokens)):
		tokens[index] = "|" + tokens[index].lower() + "|"
	freq_dist = nltk.probability.FreqDist()
	for token in tokens:
		bigrams = nltk.bigrams (list(token))
		trigrams = nltk.trigrams (list(token))
		for bigram in bigrams:
			bigram = "".join(bigram)
			if bigram in freq_dist:
				freq_dist[bigram] += 1
			else:
				freq_dist[bigram] = 1
		for trigram in trigrams:
			trigram = "".join(trigram)
			if trigram in freq_dist:
				freq_dist[trigram] += 1
			else:
				freq_dist[trigram] = 1
	top_10000 = freq_dist.most_common (10000)
	index = 0
	language_table = {}
	for word, frequency in top_10000:
		language_table[word] = index
		index = index + 1
	return language_table

#dictionary prepared for each language and stored in a pickle file
def prepare_dictionary ():
	dictionary = {}	
	print ("Preparing dictionary...")
	for lang in tqdm(corpus.keys()):
		tokens = []
		for sentence in corpus[lang]:
			tokens += nltk.tokenize.word_tokenize (sentence)
		lang_table = tokenize (tokens)
		dictionary[lang] = lang_table
	f = open ("./data/language_dictionary", "wb")
	pickle.dump(dictionary, f)	

def prepare_data ():
	data = pd.read_csv("../data/dataset.csv")
	print ("Preprocessing...")
	for language in tqdm(languages):
		sentencelist = []
		dataframe = data.loc[data['lang'] == language]
		for sentence in dataframe.sentences:
			sentence = text_cleaner (sentence)
			sentencelist.append(sentence)
		corpus [language] = sentencelist
	prepare_dictionary ()
