from app import db

class Movie(db.Model):
	__tablename__ = "movies"

	link_id = db.Column(db.String(127), primary_key=True, nullable=False)

	name = db.Column(db.String(255))
	genre = db.Column(db.Text)
	content_rating = db.Column(db.String(31))
	audience_count = db.Column(db.String(31))
	desc_keywords = db.Column(db.Text)
	review_keywords = db.Column(db.Text)
	review_keyphrases = db.Column(db.Text)

	def __init__(self, link_id:str, name:str, genre:[], content_rating:str, audience_count:int,
					desc_keywords:[], review_keywords:[], review_keyphrases:[]):
		db.Model.__init__(self, link_id=link_id, name=name, genre=genre, content_rating=content_rating,
			audience_count=audience_count, desc_keywords=desc_keywords, 
			review_keywords=review_keywords, review_keyphrases=review_keyphrases)

	def __repr__(self):
		return "<Movie %s: %r>" % (self.link_id, self.name)