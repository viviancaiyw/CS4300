# Data

## Game Keywords and Keyphrases

### Game Popular Keyowrds
#### Extraction
For each game, for each review, extract keywords from the review using yake keyword extractor, which gives a set of keywords for each review.
For each game, treat each set of keywords for one review as a document. Use count vectorizer and tfidf vectorizer to get a set of keywords for the game.
Treat each set of keywords for one game as a document, use counter vectorizer and tfidf vectorizer to get a set of commonly used keywords for games in general.

#### Script
- processing.py

#### Files
##### keywords_count_dict.json
Set of commonly used keywords for games in general extracted with count vectorizer.
```
{
	keyword:count,
	...
}
```

##### keywords_tfidf_dict.json
Set of commonly used keywords for games in general extracted with tfidf vectorizer.
```
{
	keyword:tfidf_score,
	...
}
```
Note: Doesn't seem very useful in terms of keyword quality.

##### inverse_keyword_phrases.json
Dict from keyword to game app_id with that keyword.
```
{
	keyword: [app_id1, app_id2, ...],
	...
}
```

##### keyphrases_and_keywords.json
List of keyphrases and list of keywords for games.
```
{
	keyphrases: [keyphrase1, keyphrase2, ...],
	keywords: [keyword1, keyword2, ...]
}
```



### Game Popular Keyphrases
#### Extraction
Same logic as game keyword extraction, except using counter vectorizer with 2-gram word. All keyphrases are composed of two words only.

#### Script
- processing.py

#### Files
##### keyphrases_dict.json
Set of commonly used keyphrase for games in general extracted with count vectorizer.
```
{
	keyphrase:count,
	...
}
```

##### inverse_keyword_phrases.json
Explaiend in **Game Popular Keywords**





## Movie Keywords and Keyphrases

### Movie Popular Keywords
#### Extraction
Same logic as game keyword extraction.

#### Script
- processing.py

#### Files
##### movie_keywords_count_dict.json
Set of commonly used keywords for movies in general extracted with count vectorizer.
```
{
	keyword:count,
	...
}
```

##### movie_keywords_tfidf_dict.json
Set of commonly used keywords for movies in general extracted with tfidf vectorizer.
```
{
	keyword:tfidf_score,
	...
}
```
Note: Doesn't seem very useful in terms of keyword quality.

##### movies_inverse_keyword_phrases.json
Dict from keyword to movie link with that keyword. (If the movie is 'm/xxx', then the link is 'xxx').
```
{
	keyword: [link1, link2, ...],
	...
}
```

##### movie_keyphrases_and_keywords.json
List of keyphrases and list of keywords for movies.
```
{
	keyphrases: [keyphrase1, keyphrase2, ...],
	keywords: [keyword1, keyword2, ...]
}
```



### Movie Popular Keyphrases
#### Extraction
Same logic as game keyphrase extraction.

#### Script
- processing.py

#### Files
##### movie_keyphrases_dict.json
Set of commonly used keyphrase for movies in general extracted with count vectorizer.
```
{
	keyphrae:count,
	...
}
```
##### movies_inverse_keyword_phrases.json
Explaiend in **Movie Popular Keywords**




## Synonym for Keywords and Keyphrases

### Synonym for Keywords

#### Extraction
Get a union set of the commonly used keywords for games and movies.
For each keyword, find all the synonyms for that keyword and the synonym must exist in the set too.
is_synonym(word1, word) logic:
* len(word1/word2) >= 3 and word2/word1 starts/end with word1/word2.
  * 'friend' and 'friendship'
* word1 and word2 has a similar semantic definition.
  * Used nltk wordnet synsets.
  * Used path_similarity. If score>0.65, then return true.

#### Script
- keyword_synonyms.ipynb

#### Files
##### word_to_synonyms.json
Dict from a keyword to all its synonym keywords.
```
{
	word: [synonym1, synonym2, ...],
	...
}
```



### Synonym for Keyphrases

#### Extraction
Get a union set o fthe commonly used keyphrases for games and movies.
For each keyphrase, split the keyphrase into words. Create a dict from word used in the keyphrases to a list of keyphrases that used this word.
For each word in the dict keys, find a list of synonyms that are also in the dict keys. (is_synonym logic explained in **Synonym for Keywords Extraction**)
For each word, get a list of keyphrases that either use this word or its synonym.

#### Script
- keyphrase_synonyms.ipynb

#### Files
##### phrase_word_to_syns.json
Dict from a word used in keyphrases to all its synonym words that are also used in keyphrases.
```
{
	word: [synonym1, synonym2, ...],
	...
}
```

##### phrase_word_to_synphrase.json
Dict from a word used in keyphrases to all its synonym keyphrases.
```
{
	word: [synphrase1, synphrase2, ...],
	...
}
```

