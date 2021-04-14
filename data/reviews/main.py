import download_reviews
from processing import *

import json
import pathlib
import os
import os.path

info_path = 'info/'

app_ids = [730, 570, 578080, 440, 271590, 304930, 4000, 230410, 359550, 218620, 252490, 444090, 433850, 105600, 292030, 252950, 346110, 221100, 550, 381210, 227300, 319630, 698780, 301520, 236390, 413150, 620, 275850, 242760, 227940, 49520, 377160, 291550, 264710, 391540, 107410, 238960, 203160, 374320, 222880, 322330, 10, 431960, 250900, 582010, 304050, 239140, 8870, 48700, 365590, 211820, 255710, 251570, 755790, 22380, 244850, 322170, 220, 219740, 504370, 291480, 363970, 232090, 221380, 220240, 550650, 305620, 220200, 218230, 386360, 12210, 219640, 262060, 379720, 282070, 206420, 435150, 346900, 427520, 265930, 219150, 289070, 225540, 391220, 204360, 367520, 306130, 304390, 238460, 383870, 268910, 236850, 20920, 241930, 273110, 281990, 212680, 113200, 582160, 331470, 524220, 223470, 113400, 294100, 1250, 205100, 552520, 394360, 55230, 206440, 438100, 238320, 221910, 286690, 361420, 460930, 359320, 200210, 233450, 8190, 555570, 20900, 231430, 813820, 302830, 379430, 213670, 287700, 253710, 265630, 466240, 200510, 274190, 588430, 239820, 12120, 646570, 287390, 700330, 447040, 223710, 440900, 204300, 219990, 261570, 311690, 346010, 280790, 109600, 242050, 311210, 438740, 242920, 477160, 588650, 316010, 24960, 268500, 611500, 239030, 364360, 674940, 234140, 552500, 834910, 70, 323190, 594650, 200710, 513710, 214950, 644560, 208650, 812140, 236430, 393380, 433340, 270880, 243470, 203770, 414340, 554620, 335300, 107100, 242860, 201810, 444200, 204100, 493340, 237930, 489520, 274170, 104900, 355840, 313120, 298110, 299740, 386180, 246620, 99900, 814380, 630, 236870, 24240, 35450, 629760, 40800, 274940, 289650, 50300, 50130, 22370, 304430, 226700, 214490, 108710, 203140, 518790, 250320, 10090, 457140, 200260, 553640, 374570, 583950, 356190, 838350, 349040, 248820, 632360, 393420, 285900, 387990, 397900, 33230, 581320, 257510, 307780, 17390, 418460, 7670, 312990, 241540, 372000, 594570, 337000, 319510, 8980, 310560, 307690, 108600, 244210, 17410, 48000, 236110, 221640, 282140, 360430, 10180, 883710, 489830, 434570, 582660, 247730, 339800, 387290, 424280, 403640, 552990, 323370, 383080, 380600, 33930, 269210, 335240, 333600, 355180, 779340, 260230, 362890, 447820, 302510, 209000, 516750, 262410, 284160, 431240, 261640, 648800, 207140, 259080, 3590, 384190, 42910, 577800, 110800, 105450, 334230, 247080, 648350, 884660, 389730, 250400, 637650, 24200, 466560, 47890, 248570, 476600, 263280, 221040, 241560, 47870, 674020, 235460, 241600, 35140, 240720, 418370, 644930, 383120, 544920, 620980, 224600, 303210, 253230, 668630, 480490, 22330, 238010, 233130, 389570, 298630, 325610, 406150, 212070, 270550, 8500, 35720, 32370, 645630, 312530, 236090, 447020, 238090, 214560, 57300, 235540, 312660, 232430, 245550, 264200, 233720, 39000, 375230, 206210, 427730, 601510, 323470, 39140, 39210, 394510, 420, 447530, 22300, 414700, 326460, 367500, 420530, 578310, 501300, 736190, 65980, 409710, 244450, 374040, 351640, 657200, 235600, 242720, 570940, 666140, 332310, 233860, 434650, 322500, 9900, 313340, 371660, 809960, 376210, 288160, 555220, 245170, 681660, 17460, 278360, 254700, 804320, 356670, 636480, 314160, 289130, 475150, 24980, 237110, 601150, 233270, 324800, 11020, 257850, 239160, 256290, 530700, 475550, 204450, 460920, 420290, 287290, 313160, 582500, 219890, 24010, 202170, 373420, 548430, 612880, 495890, 220440, 39120, 750920, 394230, 454650, 418340, 266840, 4500, 228380, 201790, 206500, 202970, 485510, 237990, 310950, 489940, 678950, 102500, 211500, 613100, 292730, 474960, 368500, 286160, 47810, 871720, 738060, 214420, 212500, 460790, 41700, 48240, 12110, 365450, 365300, 12200, 459820, 402710, 203290, 563560, 239350, 209650, 10500, 209160, 9200, 428690, 209080, 211400, 302670, 282900, 630100, 638970, 442080, 339610, 584400, 298240, 250760, 859580, 206190, 291650, 384300, 238430, 436520, 301640, 285190, 473690, 389430, 353370, 208580, 444640, 841370, 21690]

def extract_single_game(app_id):
	print("app_id:", app_id)
	# Download reviews.
	print("Download reviews")
	reviews_dict = download_reviews.get_reviews(app_id)

	# Filter review dict (recommendationid -> review info).
	reviews_dict = filter_reviews_dict(reviews_dict)

	# Look at only 'review' text.
	reviews = [r['review'] for r in reviews_dict.values()]

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

def write_info(info, app_id):
	pathlib.Path(info_path).mkdir(parents=True, exist_ok=True)
	output_path = info_path+'info_'+str(app_id)+'.json'

	with open(output_path, 'w') as f:
		f.write(json.dumps(info)+'\n')

def write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict):
	total = {'keyphrases':keyphrases, 'keywords':keywords}

	output_path = 'keyphrases_and_keywords.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(total, indent=4)+'\n')

	output_path = 'keyphrases_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(keyphrases_dict, indent=4)+'\n')

	output_path = 'keywords_tfidf_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(tfidf_dict, indent=4)+'\n')	

	output_path = 'keywords_count_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(count_dict, indent=4)+'\n')	

def extract_common():
	all_keywords = list()
	all_keyphrases = list()
	count = 0
	for filename in os.listdir(info_path):
		if filename.endswith('.json'):
			with open(info_path+filename, 'r', encoding='utf8') as in_json_file:
				print("Process file", filename)
				info = json.load(in_json_file)
				all_keywords.append(" ".join(info['keywords']))
				all_keyphrases.extend(info['keyphrases'])

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common_keywords_and_phrases(all_keywords, all_keyphrases)
	return keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict


if __name__ == "__main__":
	# for app_id in app_ids:
	# 	app_id = str(app_id)
	# 	output_path = info_path+'info_'+str(app_id)+'.json'
	# 	if os.path.isfile(output_path):
	# 		print(app_id," exists")
	# 		continue

	# 	keyphrases, keywords = extract_single_game(app_id)
	# 	info = {'app_id':app_id, 'keyphrases':keyphrases, 'keywords': keywords}

	# 	write_info(info, app_id)

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common()
	write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict)
