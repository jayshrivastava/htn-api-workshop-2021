# Part 2
from flask import Flask, jsonify, request
# Part 4
import json
# Part 6
import os
# Part 7
import random
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

"""
Part 7 - Working with A Database
"""
# # Source: https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-pony.html
# db = Database()

# db_password = os.environ['db_password']
# # print(len(db_password))

# class Book(db.Entity):
#   _table_ = 'books'
#   id = PrimaryKey(int)
#   title = Required(str)
#   author = Required(str)
#   rating = float
#   pages = int

# db_params = dict(provider='cockroach', user='jayant', host='free-tier.gcp-us-central1.cockroachlabs.cloud', port=26257, database='upbeat-bear-3029.defaultdb', password=db_password)

# sql_debug(True)  # Print all generated SQL queries to stdout
# db.bind(**db_params)  # Bind Database object to the real database
# db.generate_mapping(create_tables=True)  # Create tables

# @db_session  # db_session decorator manages the transactions
# def db_create_book(id, title, author, rating, pages):
#   return Book(id, title, author, rating, pages).to_dict()

# @db_session
# def db_get_all_books():
#   return [book.to_dict() for book in Book.select()]

# @db_session 
# def db_get_book(id, title, author, rating, pages):
#   return Book(id, title, author, rating, pages).to_dict() 

# @app.route('/', methods=['GET'])
# @db_session
# def index():
#     return jsonify(db_get_all_books())

"""
End of Part 7 Code
"""


"""
Parts 2-5 - Building an API without a Database
"""

# Part 2 - Set up an API
app = Flask(__name__)

# Books stored in memory in a Python dictionary
books = {
  0: {'id': 0,
    'title': 'Harry Potter and the Chamber of Secrets (Harry Potter #2)',
    'author': 'J.K. Rowling',
    'rating': 4.42,
    'pages': 352},
  1: {'id': 1,
    'title': 'The Fellowship of the Ring (The Lord of the Rings #1)',
    'author': 'J.R.R. Tolkien',
    'rating': 4.36,
    'pages': 398},
  2: {'id': 2,
    'title': 'Treasure Island',
    'author': 'Robert Louis Stevenson',
    'rating': 3.83,
    'pages': 311}
}

# Part 3 - Get Requests
@app.route('/', methods=['GET'])
def index():
    return jsonify([books[book_id] for book_id in books])

# Request Params Example
@app.route("/<id>", methods=['GET'])
def get_book(id):
    if int(id) not in books:
      return jsonify({"error": "invalid id"})
    return jsonify(books[int(id)])

# Route Params Example
@app.route("/search", methods=['GET'])
def search_books():
  result = []

  for book_id, book in books.items():
    if request.args.get('max_pages'):
      if book['pages'] > int(request.args.get('max_pages')):
        continue

    if request.args.get('min_rating'):
      if book['rating'] < int(request.args.get('min_rating')):
        continue

    result.append(book)
  return jsonify(result)

# Part 4 - Post Requests
@app.route("/", methods=['POST'])
def create_book():
  new_book = request.json
  if new_book['id'] in books:
    return jsonify({"error": "book with that id already exists"})

  books[new_book['id']] = new_book
  return jsonify(new_book)

# Part 5 - Put and Delete Requests
@app.route("/<id>", methods=['PUT'])
def update_author(id):
  if int(id) not in books:
    return jsonify({"error": "invalid id"})
  books[int(id)]['author'] = request.json['author']

  return jsonify(books[int(id)])

@app.route("/<id>", methods=['DELETE'])
def delete_book(id):
  if int(id) not in books:
    return jsonify({"error": "invalid id"})
  deleted_book = books[int(id)]
  del books[int(id)]
  return jsonify(deleted_book)

# Runs the API and exposes it on https://<repl name>.<replit username>.repl.co
# ex. Mine deploys to https://htn-api.jayantsh.repl.co.
app.run(
  host = "0.0.0.0",
  debug = True
)




