from app import db

class eigenvector(db.Model):
    __tablename__ = "eigenvector"
    rownumber = db.Column(db.String, nullable=False, primary_key=True)
    alleigenvector = db.Column(db.Text)

    def __init__(self, rn, vec):
        db.Model.__init__(self, rownumber=rn, alleigenvector=vec)

