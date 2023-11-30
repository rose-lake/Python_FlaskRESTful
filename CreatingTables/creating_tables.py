from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import tomllib

with open("../config.toml", "rb") as f:
  data = tomllib.load(f)
db_password = data['db']['password']

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
  f"mysql+mysqlconnector://root:{db_password}@localhost/bookshop"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)

class Book(db.Model):
  book_id = db.Column(db.String(24), primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  author = db.Column(db.String(255), nullable=False)
  price = db.Column(db.Float())
  quantity = db.Column(db.Integer())
  
  def __init__(self, book_id, title, author, price, quantity):
    
    self.book_id = book_id
    self.title = title
    self.author = author
    self.price = price
    self.quantity = quantity
    
db.create_all()

if __name__ == "__main__":
  app.run(debug=True)