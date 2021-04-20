from app import db # Grab the db from the top-level app
from marshmallow_sqlalchemy import ModelSchema # Needed for serialization in each model
from werkzeug import check_password_hash, generate_password_hash # Hashing
import hashlib # For session_token generation (session-based auth. flow)
import datetime # For handling dates 

import os

DATA_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "data"))

class Base(db.Model):
  """Base PostgreSQL model"""
  __abstract__ = True
  id         = db.Column(db.Integer, primary_key =True)
  created_at = db.Column(db.DateTime, default    =db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default    =db.func.current_timestamp())
