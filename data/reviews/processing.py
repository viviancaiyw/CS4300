import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from gensim.parsing.preprocessing import STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from rake_nltk import Rake
import yake
from collections import Counter

# Game stopwords
# stop_words = stopwords.words('english')
# stop_words.extend(STOPWORDS)
# stop_words.extend(['player', 'play', 'people', 'game', 'steam','review',
# 				  'day', 'year', 'hour', 'minute','time','moment','like',
# 				  'world', 'yes', 'lol', 'lmao', 'cool', 'love', 'get',
# 				  'good', 'great', 'nice', 'best', 'fun', 'awesome',
# 				   'ever', 'kinda', 'shit', 'yeah', 'new', 'old',
# 				  'big','small','high','low','many','much','lot','alot',
# 				  'others','thank','http','thing','everyone','anyone','anything',
# 				  'everything','cant','dont','guy','hello','plenty','entire',
# 				  'youtube','something','someone','pro','con','guys',
# 				  'haha', 'hehe','end','nothing','no','one',
# 				  'fine','first','last','epic','english','bit',
# 				  'terrible','overall','original','life','bad',
# 				  'today','fps','gameplay','favorite','com','favourite'
# 				  'man','word','version','pure','experience','www',
# 				  'please','thanks','little','least','way','different',
# 				  'style','man','men','super','problem','item','work','computer',
# 				  'stuff','wait','early','access','sure','able','developer','wow','genre',
# 				  'ive','rich','feel','fact','fuck','absolute','matter','standard',
# 				  'deep',
# 				  'potential','perfect','popular','reason','person'])
# stop_words.extend(['server','update','performance','system','program','software'])
# stop_words.extend(['worth','full','point','real','part','amount','reason',
# 				  'option','open','previous','huge','enjoyable','kind','ton',
# 				  'person','launch','opinion','month','ability','current','use',
# 				  'stupid','mess','slash','wololo','wrong'])
# stop_words = list(set(stop_words))

# Movie stopwords
stop_words = stopwords.words('english')
stop_words.extend(STOPWORDS)
stop_words.extend(['im','youre','hes','shes','theyre','ive','its'])

stop_words.extend(['sort','single','play','start','end','big','small','good','bad',
	'kind','movie','title','time','year','hour','minute','thing','anything','everything',
	'anyone','everyone','film','work','story','great','terrible','strong','cast','fun',
	'worthy','moment','dialogue','people','person','perfect','rate','tone','eye','review',
	'picture','man','guy','mind','line','piece','video','worth','cinema','script',
	'watch','experience','viewer','feel','true','lot',
	'wow','matter','high','low','genre','fact','awesome','popcorn','screen','bang','director',
	'camera','key','studio','actor','season','potential',
	'super','fan','easy','wonderful','perfect','reason',
	'writer','feat','large','heart','tale','ride','spanish','filmmaker','idea','level','hitchcock',
	'offer','plot','character','late','masterpiece','element',
	'deep','performance','narrative','place','impeccable','day',
	'final','bit','hard','let','world','mess','entire'
])

'''
Filter by written_during_early_access=False and play_time_forever>60minutes

Return: dict(recommendationid -> review info)
'''
def filter_reviews_dict(reviews_dict):
	results = list(
		filter(
			lambda x: x['written_during_early_access']==False and 
			x['author']['playtime_forever']>60 and 
			x['language']=='english', 
			reviews_dict['reviews'].values()))
	results = {x['recommendationid']: x for x in results}
	return results

'''
Remove punctuations and numbers, lowercase, filter review with words <= 10.

Return: a processed review split
'''
def clean_review(review):
	review = re.sub('[^A-Za-z]+', ' ', review).strip()
	split = review.split()
	if len(split)<=10:
		return ''
	# review = ' '.join([w.lower() for w in split if len(w)>2])
	review_split = [w.lower() for w in split if len(w)>2]
	return " ".join(review_split)

'''
Keep nouns and adjs in the review, remove all others.

Return: a list of words in the review
'''
def keep_noun_and_adj(review_split):
	is_noun_or_adj = lambda pos: pos[:2]=='NN' or pos[:2]=='JJ'
	lemmatizer = WordNetLemmatizer()

	def noun_adj_processor(word, pos):
		if pos[:2] == 'NN':
			return lemmatizer.lemmatize(word)
		else:
			return lemmatizer.lemmatize(word, pos='a')
	return [noun_adj_processor(word, pos) for (word,pos) in nltk.pos_tag(review_split) if is_noun_or_adj(pos)]


'''
Transform the review by keeping only nouns and adjs, and remove stop words.

Return: a review
'''
def transform_and_remove_words(review):
	review_split = review.split()
	review_split = keep_noun_and_adj(review_split)
	review_split = list(filter(lambda x: x not in stop_words, review_split))
	review_split = keep_noun_and_adj(review_split)
	review_split = list(filter(lambda x: x not in stop_words, review_split))
	if len(review_split)==0:
		return ''
	return " ".join(review_split)


def filter_keyphrase(two_gram_keyphrase):
	split = two_gram_keyphrase.split()

	word_tags = nltk.pos_tag(split)
	(word1, pos1) = word_tags[0]
	(word2, pos2) = word_tags[1]

	if word1==word2:
		return False

	stemmer = SnowballStemmer("english")
	if stemmer.stem(word1)=='game' or stemmer.stem(word2)=='game':
		return False

	if pos2[:2] == 'NN' and (pos1[:2]=='JJ' or pos1[:2]=='NN'):
		return True

	if word2 == 'recommend':
		return True

	return False



''' 
Extract 2 word keyphrases from a game's all reviews.

Return: keyphrases
'''
def extract_keyphrases(reviews):
	if len(reviews)==0:
		return []
	keyphrases_stop_words = stopwords.words('english')
	keyphrases_stop_words.extend(STOPWORDS)
	keyphrases_stop_words.extend(['game'])

	count_vec = CountVectorizer(ngram_range=(2,2),stop_words=keyphrases_stop_words,binary=True)
	count = count_vec.fit_transform(reviews)
	count = np.squeeze(np.array(np.sum(count.T, axis=1)))

	count_df = pd.DataFrame({
		'word': count_vec.get_feature_names(),
		'count': count
		})
	count_df = count_df[count_df['count']>1]
	count_df = count_df.sort_values(by=['count'], ascending=False)

	keyphrases = list(count_df['word'])
	keyphrases = list(filter(filter_keyphrase, keyphrases))[:50]


	return keyphrases


'''
Process keywords for each review using yake keyword_extractor.

Return: keywords for a review
'''
def process_keywords(review):
	language = "en"
	max_ngram_size = 1
	deduplication_threshold = 0.9
	numOfKeywords = 20
	custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

	keywords = custom_kw_extractor.extract_keywords(review)
	keywords = sorted(keywords, key=lambda item:(item[1]))[:10]
	keywords = [x[0] for x in keywords]
	keywords = " ".join(keywords)
	return keywords


'''
Extract keywords for multiple reviews.

Return: keywords for the review list.
'''
def extract_keywords(reviews):
	if len(reviews)==0:
		return []
	# Use yake to extract keywords for each review
	review_keywords = list(map(process_keywords, reviews))
	review_keywords = list(filter(lambda x: len(x)>0, review_keywords))

	if len(review_keywords)==0:
		return []

	# Use count vectorizer to get keywords.
	count_vec = CountVectorizer(binary=True)
	count = count_vec.fit_transform(review_keywords)
	count = np.squeeze(np.array(np.sum(count.T, axis=1)))

	count_df = pd.DataFrame({
		'word': count_vec.get_feature_names(),
		'count': count
		})
	count_df = count_df[count_df['count']>1]
	count_df = count_df.sort_values(by=['count'], ascending=False)
	keywords = set(count_df[:100]['word'])

	# Use tf-idf vectorizer to get keywords.
	tfidf_vec = TfidfVectorizer(smooth_idf=True,max_df=1.0,use_idf=True, sublinear_tf=True)
	tfidf = tfidf_vec.fit_transform(reviews)
	tfidf = tfidf[0]

	tfidf_df = pd.DataFrame({
		'word': tfidf_vec.get_feature_names(),
		'tfidf': np.squeeze(np.array(tfidf.T.todense()))
	})
	tfidf_df = tfidf_df[tfidf_df['tfidf']!=0]
	tfidf_df = tfidf_df.sort_values(by=['tfidf'], ascending=False)
	keywords.update(set(tfidf_df[:100]['word']))

	keywords = list(keywords)

	return keywords

def extract_common_keywords_and_phrases(all_keywords, all_keyphrases):
	keyphrase_count_threshold = 5
	keyword_count_threshold = 3

	# keyphrases
	print("Extract common keyphrases")
	keyphrases_count = Counter(all_keyphrases)
	keyphrases_count = keyphrases_count.most_common()
	keyphrases_dict = {x: count for x,count in keyphrases_count if count>=keyphrase_count_threshold}
	keyphrases = keyphrases_dict.keys()

	# keywords
	print("Extract common keywords with tfidf")
	keywords = set()
	tfidf_vec = TfidfVectorizer(smooth_idf=True,max_df=0.9,use_idf=True, sublinear_tf=True)
	tfidf = tfidf_vec.fit_transform(all_keywords)
	tfidf = tfidf[0]

	tfidf_df = pd.DataFrame({
		'word': tfidf_vec.get_feature_names(),
		'tfidf': np.squeeze(np.array(tfidf.T.todense()))
	})
	tfidf_df = tfidf_df[tfidf_df['tfidf']!=0]
	tfidf_df = tfidf_df.sort_values(by=['tfidf'], ascending=False)

	tfidf_dict = dict(zip(tfidf_df.word, tfidf_df.tfidf))

	keywords.update(list(tfidf_df['word']))


	print("Extract common keywords with count")
	count_vec = CountVectorizer(binary=True)
	count = count_vec.fit_transform(all_keywords)
	count = np.squeeze(np.array(np.sum(count.T, axis=1)))

	def is_noun(word):
		word_pos = nltk.pos_tag([word])
		if word_pos[0][1][:2] == 'NN':
			return True
		else:
			return False

	def filter_fn(row):
		if is_noun(row['word']) and row['count'] > keyword_count_threshold:
			return True
		elif row['count'] > keyword_count_threshold*2:
			return True
		else:
			return False
	
	count_df = pd.DataFrame({
		'word': count_vec.get_feature_names(),
		'count': count
	})

	m = count_df.apply(filter_fn, axis=1)
	count_df = count_df[m]
	count_df = count_df.sort_values(by=['count'], ascending=False)

	count_dict = dict(zip(count_df['word'], count_df['count']))

	keywords.update(list(count_df['word']))

	return list(keyphrases), list(keywords), keyphrases_dict, tfidf_dict, count_dict


















