from app import db


class Movie(db.Model):
    __tablename__ = "movies"

    link_id = db.Column(db.String(127), primary_key=True, nullable=False)
    games = db.Column(db.Text)
    genre = db.Column(db.Text)
    desc_keywords = db.Column(db.Text)

    def __init__(self, link_id: str, games: [], genre: [], desc_keywords: []):
        db.Model.__init__(self, link_id=link_id, games=games,
                          genre=genre, desc_keywords=desc_keywords)

    def __repr__(self):
        return "<Movie %s: %r>" % (self.link_id, self.name)
