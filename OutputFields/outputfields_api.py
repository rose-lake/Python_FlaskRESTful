import tomllib
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

with open("../config.toml", "rb") as f:
  data = tomllib.load(f)
db_password = data['db']['password']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://root:{db_password}@localhost/bookshop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

app.app_context().push()
db = SQLAlchemy(app)

class Book(db.Model):
  
    book_id = db.Column(db.String(24), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)

    def __init__(self, book_id, title, author, price, quantity):

        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

class AvailableItem(fields.Raw):
    def format(self, value):
        return "Available" if value > 0 else "Unavailable"

class SpecialOfferItem(fields.Raw):
    def format(self, value):
        return "Special offer!" if value < 1 else "No offer yet"

class LowerCaseItem(fields.Raw):
    def format(self, value):
        return value.lower()

class UpperCaseItem(fields.Raw):
    def format(self, value):
        return value.upper()

resource_fields = {
    # previously, we upper-cased / lower-cased using a lambda
    # 'book_id': fields.String(attribute=lambda book: book.title.lower()),
    # 'book_title': fields.String(attribute=lambda book: book.title.upper()),
    # now, we upper-case / lower-case using our defined classes which extend fields.Raw and override the format method
    'book_id': LowerCaseItem(attribute='book_id'),
    'book_title': UpperCaseItem(attribute='title'),
    'book_author': fields.String(attribute='author'),
    'book_price_quantity': {
        'book_price': fields.Float(attribute='price', default=1.99),
        'book_quantity': fields.Integer(attribute='quantity', default=1)
    },
    'uri': fields.Url('book'),
    'https_uri': fields.Url('book', absolute=True, scheme='https'),
    'status': AvailableItem(attribute='quantity'),
    'offer': SpecialOfferItem(attribute='price')
}

add_book_parser = reqparse.RequestParser()
add_book_parser.add_argument("author", type=str, required=True)
add_book_parser.add_argument("title", type=str, required=True)
add_book_parser.add_argument("price", type=float, required=True)
add_book_parser.add_argument("quantity", type=int, required=True)

update_book_parser = add_book_parser.copy()
update_book_parser.remove_argument("author")
update_book_parser.remove_argument("title")
update_book_parser.replace_argument("price", type=float)
update_book_parser.replace_argument("quantity", type=int)

class Books(Resource):

    @marshal_with(resource_fields) 
    def get(self):
        
        return Book.query.all()

class HarryPotterSeries(Resource):
    
    @marshal_with(resource_fields, envelope='hp_books')
    def get(self):
        
        books = Book.query.filter_by(author = "J.K. Rowling").all()
        return books

class GameOfThronesSeries(Resource):
    
    @marshal_with(resource_fields, envelope='got_books')
    def get(self):
        
        books = Book.query.filter_by(author = "George R. R. Martin").all()
        return books

api.add_resource(Books, '/books/all', endpoint='book')

api.add_resource(HarryPotterSeries, '/books/hp_series')
api.add_resource(GameOfThronesSeries, '/books/got_series')

if __name__ == "__main__":
  app.run(debug=True)