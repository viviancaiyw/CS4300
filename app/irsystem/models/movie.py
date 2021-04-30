from app import db


class Movie(db.Model):
    __tablename__ = "movies"

    link_id = db.Column(db.String(127), primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    games_review_match = db.Column(db.Text)
    games_title_match = db.Column(db.Text)
    genre = db.Column(db.Text)
    desc_keywords = db.Column(db.Text)
    vector_pca = db.Column(db.Text)

    def __init__(self, link_id: str, name: str, games_review_match: [], games_title_match: [],
                 genre: [], desc_keywords: [], vector_pca: []):
        db.Model.__init__(self,
                          link_id=link_id,
                          name=name,
                          games_review_match=games_review_match,
                          games_title_match=games_title_match,
                          genre=genre,
                          desc_keywords=desc_keywords,
                          vector_pca=vector_pca)

    def __repr__(self):
        return "<Movie %s: %r>" % (self.link_id, self.name)
