import pandas as pd
import numpy as np

def word_counter(text):
	'''This function retund the counts of each word sorted in their repetition order
		Args:
			text: any text/paragraph/string
		'''
	text = text.replace('.','')
	text = text.replace('\n',' ')
	list_of_words = text.split(' ')
	counts = {}
	for i in pd.unique(list_of_words):
		if i in counts.keys():
			counts[i]=counts[i]+1
		else:
			counts[i]=0
			counts[i]=counts[i]+1

	return counts

string = '''My name is deepesh,
i work as a data analyst in practo.
this is the string.'''

print type(string)

print word_counter(string)