import ast 
from pprint import pprint
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')



# tid = 2220054
# url = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid=" + str(tid)

# FORBIDDEN AGAIN! :(
# import urllib
# link = url
# f = urllib.request.urlopen(link)
# myfile = f.read()
# print(myfile)

sid = SentimentIntensityAnalyzer()

def produce_sentiment(json_file_name):
	teacher_name = json_file_name[:-4]
	text = ""
	with open(json_file_name) as f:
		data = json.load(f)
	for review in data:
		new_text = review["rComments"]
		text = text + " " + new_text

	ss = sid.polarity_scores(text)
	for k in ss:
		if k != 'compound': #or k == 'positive' or k == 'negative':
			print(k, ss[k])
	print(ss)
	return(teacher_name, ss)

produce_sentiment("ada.json")
produce_sentiment("mackey.json")
produce_sentiment("iliano.json")

# THIS IS HIGHLY BIASED DATA
# SAMPLE SIZE ~20 

# Anil Ada:
# pos 0.288
# neu 0.671
# neg 0.041

# John Mackey:
# pos 0.33
# neu 0.614
# neg 0.056

# Iliano Cervesato:
# pos 0.142
# neu 0.749
# neg 0.109