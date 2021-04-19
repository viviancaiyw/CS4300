from app import db

class Game(db.Model):
	__tablename__ = "games"

	app_id = db.Column(db.String(63), primary_key=True, nullable=False)

	name = db.Column(db.String(255))
	developer = db.Column(db.Text)
	publisher = db.Column(db.Text)
	tags = db.Column(db.Text)
	genre = db.Column(db.Text)
	num_players = db.Column(db.Text)
	rating = db.Column(db.String(31))
	mature_content = db.Column(db.Boolean)
	url = db.Column(db.String(255))
	desc_keywords = db.Column(db.Text)


	def __init__(self, app_id:str, name:str, developer:[], publisher:[],
				tags:[], genre:[], num_players:[], rating:int, mature_content:bool,
				url:str, desc_keywords:[]):
		db.Model.__init__(self, app_id=app_id, name=name, developer=developer, 
			publisher=publisher, tags=tags, genre=genre, num_players=num_players, 
			rating=rating, mature_content=mature_content, url=url, desc_keywords=desc_keywords)

	def __repr__(self):
		return "<Game %s: %r>" % (self.app_id, self.name)

