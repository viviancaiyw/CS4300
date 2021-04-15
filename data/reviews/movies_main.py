import download_reviews
from processing import *

import json
import pathlib
import os
import os.path

movie_info_path = 'movie_info/'


def extract_single_movie(link, reviews):
	print("link:", link)

	# Clean reviews.
	print("Clean reviews")
	reviews = list(map(clean_review, reviews))
	reviews = list(filter(lambda x: x!='', reviews))

	# Tranform reviews.
	print("Transform reviews")
	transformed_reviews = list(map(transform_and_remove_words, reviews))
	transformed_reviews = list(filter(lambda x: x!='', transformed_reviews))

	# Extract keyphrases from original reviews.
	print("Keyphrases")
	keyphrases = extract_keyphrases(reviews)

	# Extract keywords from cleaned reviews.
	print("Keywords")
	keywords = extract_keywords(transformed_reviews)

	print(keywords[:10])
	print(keyphrases[:5])

	return keyphrases, keywords

def write_info(info, link):
	pathlib.Path(movie_info_path).mkdir(parents=True, exist_ok=True)
	output_path = movie_info_path+'info_'+link+'.json'

	with open(output_path, 'w') as f:
		f.write(json.dumps(info)+'\n')

def write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict):
	total = {'keyphrases':keyphrases, 'keywords':keywords}

	output_path = 'movie_keyphrases_and_keywords.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(total, indent=4)+'\n')

	output_path = 'movie_keyphrases_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(keyphrases_dict, indent=4)+'\n')

	output_path = 'movie_keywords_tfidf_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(tfidf_dict, indent=4)+'\n')	

	output_path = 'movie_keywords_count_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(count_dict, indent=4)+'\n')	

def extract_common():
	all_keywords = list()
	all_keyphrases = list()
	count = 0
	for filename in os.listdir(movie_info_path):
		if filename.endswith('.json'):
			with open(movie_info_path+filename, 'r', encoding='utf8') as in_json_file:
				print("Process file", filename)
				info = json.load(in_json_file)
				all_keywords.append(" ".join(info['keywords']))
				all_keyphrases.extend(info['keyphrases'])

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common_keywords_and_phrases(all_keywords, all_keyphrases)
	return keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict


if __name__ == "__main__":
	print("Read in reviews")
	# reviews_data = pd.read_csv('rotten_tomatoes_critic_reviews.csv')

	# link_to_reviews = dict()
	# for index, row in reviews_data.iterrows():
	# 	reviews = link_to_reviews.get(row['rotten_tomatoes_link'][2:], set())
	# 	reviews.add(str(row['review_content']))
	# 	link_to_reviews[row['rotten_tomatoes_link'][2:]] = reviews

	# link_to_reviews = {link: list(reviews) for (link, reviews) in link_to_reviews.items()}

	# output_path = 'movie_link_to_reviews.json'
	# with open(output_path, 'w') as f:
	# 	f.write(json.dumps(link_to_reviews, indent=4)+'\n')

	with open('movie_link_to_reviews.json', 'r', encoding='utf8') as in_json_file:
			link_to_reviews = json.load(in_json_file)

	links = link_to_reviews.keys()
	for link in links:
		output_path = movie_info_path+'info_'+link+'.json'
		if os.path.isfile(output_path):
			print(link, 'exists')
			continue

		keyphrases, keywords = extract_single_movie(link, link_to_reviews[link])
		info = {'link':link, 'keyphrases':keyphrases, 'keywords':keywords}

		write_info(info, link)

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common()
	write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict)
