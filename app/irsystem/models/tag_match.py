import json
import re
import itertools
from collections import Counter
import numpy as np

from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
tag_stop_words = ['game', 'play', 'video', 'steam']



# Cleaning

'''
Clean a string by lowercasing and removing punctuations.
'''
def clean_str(string):
	string = string.lower()
    string = re.sub('[^A-Za-z]+', ' ', syn).strip()
    return string


'''
Clean a synonym.
'''
def clean_syn(syn):
	cleaned = clean_str(syn)

	# Filter synonym with punctuations
	if cleaned != syn:
		return []

	# Filter synonym with more than 1 word
	split = cleaned.split()
	split = list(filter(lambda x: len(x)>2, split))
	return split

'''
Clean a list of synonyms.
'''
def clean_syns(syns):
	syns = list(map(clean_syn, syns))
	syns = list(itertools.chain(*syns))
	return syns


'''
Clean a tag.
'''
def clean_tag(tag):
	tag = clean_str(tag)

	# Lemmatize tag with a single word
	if len(tag.split())==1:
		(tag,pos) = nltk.pos_tag([tag])[0]
		if pos != 'n' and pos != 'a':
			pos = 'n'
		tag = lemmatizer.lemmatize(tag, pos)

	return tag


'''
Clean a lis tof tags.
'''
def clean_tags(tags):
	tags = list(map(clean_tag, tags))

	# Filter tags that are stopwords.
	tags = list(filter(lambda x: x not in tag_stop_words, tags))
	return tags





# Keyword match

'''
Get a list of synonyms for the given word.
'''
def get_syns(word):
	syns = set()

	# Get all the synonyms for the word when the word is a noun / adj.
	synsets = wn.synsets(word, pos=wn.NOUN)
	synsets.extend(wn.synsets(word, pos=wn.ADJ))

	for sense in synsets:
		if sense.pos()=='s':
			sense = sense.similar_tos()[0]
		syns.update(clean_syns(sense.lemma_names()))

	if word in syns:
		syns.remove(word)
	return list(syns)

'''
Get a list of derived adjs for the given word if the word is a noun.
'''
def get_derived(word, pos):
	derived = set()

	synsets = wn.synsets(word, pos=pos)

	# Only get derived words for a noun.
	if pos=='n':
		for sense in synsets:
			curr_derived = [n.name() for l in sense.lemmas() \
								for n in l.derivationally_related_forms()]
			curr_derived = clean_syns(curr_derived)

			# Only keep derived words that are adj.
			curr_derived = list(filter(
				lambda x: nltk.pos_tag([x])[0][1][:2]=='JJ', curr_derived))
			derived.update(curr_derived)
	return list(derived)



'''
Get a word_vector representation for the tags to use 
for keyword matching with games.

return: (word_vector, norm)
'''
def match_game_keywords(tags):
	tags = list(map(lambda x: x.split(), tags))
	tags = list(itertools.chain(*tags))

	# Get syns for each tag
	tag_to_syns = dict()
	for tag in tags:
		syns = tag_to_syns.get(tag, list())
		syns.extend(get_syns(tag))
		tag_to_syns[tag] = syns

	# Get all the words to put in the final vector.
	# This includes words appear in the tags and their synonyms.
	allwords = list(tags)
	for syns in tag_to_syns.values():
		allwords.extend(syns)

	# Calculate weights for each word.

	# Start by counting word frequency.
	weight = Counter(allwords)
	weight = dict(weight)

	# Adjust weight based on word pos 
	# and whether it's the original word given by the user
	for word in set(tags):
		(word,pos) = nltk.pos_tag([word])[0]

		if pos[:2]=='NN':
			if word in tags:
				weight[word] = weight[word]*2
			else:
				weight[word] = weight[word]*1.75
			pos = 'n'
		elif pos[:2]=='JJ':
			if word in tags:
				weight[word] = weight[word]*1.75
			else:
				weight[word] = weight[word]*1.5
			pos = 'a'
		else:
			continue

	# Adjust weight for derived words.
	derived = get_derived(word, pos)

	for dv in derived:
		if dv not in weight.keys():
			weight[dv] = weight[word]*0.9

	vector = np.array(list(weight.values()))
	squared = vector ** 2
	norm = np.sum(squared)
	norm = np.sqrt(norm)

	return weight, norm














