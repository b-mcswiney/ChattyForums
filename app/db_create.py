from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

#Used for creation of the database
db.create_all()