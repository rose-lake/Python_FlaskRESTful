import tomllib
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from flask_restful import HTTPException

class BookAlreadyExistsError(HTTPException):
    pass

class BookDoesNotExistError(HTTPException):
    pass

my_custom_errors = {
    'BookAlreadyExistsError': {
        'message': "A book with this book_id already exists",
        'status': 412
    },
    'BookDoesNotExistError': {
        'message': "A book with this book_id does not exist",
        'status': 404
    }
}
    
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

with open("../config.toml", "rb") as f:
  data = tomllib.load(f)
db_password = data['db']['password']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://root:{db_password}@localhost/bookshop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app, errors=my_custom_errors)

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

resource_fields = {
    'book_id': fields.String,
    'title': fields.String,
    'author': fields.String,
    'price': fields.Float,
    'quantity': fields.Integer
}

def non_negative_quantity(value, name):
    
    if (value < 0):
        raise ValueError(f"The parameter {name} is negative: {value}")
    
    return value

add_book_parser = reqparse.RequestParser()
add_book_parser.add_argument("author", type=str, required=True)
add_book_parser.add_argument("title", type=str, required=True)
add_book_parser.add_argument("price", type=float, required=True)
add_book_parser.add_argument("quantity", type=non_negative_quantity, required=True)

update_book_parser = add_book_parser.copy()
update_book_parser.remove_argument("author")
update_book_parser.remove_argument("title")
update_book_parser.replace_argument("price", type=float)
update_book_parser.replace_argument("quantity", type=int)

class Books(Resource):

    @marshal_with(resource_fields) 
    def get(self):
        
        return Book.query.all()

class SingleBook(Resource):

    @marshal_with(resource_fields)
    def get(self, book_id):
        
        book = Book.query.get(book_id)
        
        if not book:
            raise BookDoesNotExistError()
        
        return book, 200

    @marshal_with(resource_fields)
    def post(self, book_id):
    
        args = add_book_parser.parse_args()
        
        book = Book.query.filter_by(book_id = book_id).first()
        
        if book:
            raise BookAlreadyExistsError()
        
        book = Book(book_id=book_id,
                    title=args['title'],
                    author=args['author'],
                    price=args['price'],
                    quantity=args['quantity'])
        
        db.session.add(book)
        db.session.commit()
        
        return book, 201
    
    @marshal_with(resource_fields)
    def put(self, book_id):
        
        args = update_book_parser.parse_args()
        
        book = Book.query.filter_by(book_id = book_id).first()
        
        if not book:
            raise BookDoesNotExistError()
        
        for key, value in args.items():
            if key == "price" and value:
                book.price = value
            if key == "quantity" and value:
                book.quantity = value
        
        db.session.add(book)
        db.session.commit()
        
        return book, 200
    
    def delete(self, book_id):
        
        book = Book.query.filter_by(book_id = book_id).first()
        
        if not book:
            raise BookDoesNotExistError()
            
        db.session.delete(book)
        db.session.commit()
        
        return "", 204

api.add_resource(Books, '/books/all')
api.add_resource(SingleBook, '/books/<string:book_id>')

if __name__ == "__main__":
  app.run(debug=True)