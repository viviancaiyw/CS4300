from . import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(Base, UserMixin):
  __tablename__ = 'users'

  username        = db.Column(db.String(64), index=True, unique=True)
  email           = db.Column(db.String(128), nullable=False, unique=True)
  password_hash = db.Column(db.String(128))

  # def __init__(self, **kwargs):
  #   self.email           = kwargs.get('email', None)
  #   self.fname           = kwargs.get('fname', None)
  #   self.lname           = kwargs.get('lname', None)
  #   self.password_digest = generate_password_hash(kwargs.get('password'), None)

  def __repr__(self):
    return str(self.__dict__)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

# class UserSchema(ModelSchema):
#   class Meta:
#     model = User

@login.user_loader
def load_user(id):
  return User.query.get(int(id))