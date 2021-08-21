import random
import os
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

db_password = '<PUT DB PASSWORD HERE>' # Replit does not read os.environ['db_password'] correctly outside of main.py :(

db = Database()

class Book(db.Entity):
  _table_ = 'books'
  id = PrimaryKey(int)
  title = Required(str)
  author = Required(str)
  rating = Required(float)
  pages = Required(int)

db_params = dict(provider='cockroach', user='jayant', host='free-tier.gcp-us-central1.cockroachlabs.cloud', port=26257, database='upbeat-bear-3029.defaultdb', password=db_password)

sql_debug(True)  # Print all generated SQL queries to stdout
db.bind(**db_params)  # Bind Database object to the real database
db.generate_mapping(create_tables=True)  # Create tables

@db_session
def create_book(id,title, author, rating, pages):
  Book(id=id, title=title, author=author, rating=rating, pages=pages)

# Read CSV Data and Create Books
f = open("books.csv", "r")
for i,line in enumerate(f):
  parts = line.strip().split(',')
  create_book(i,parts[0], parts[1], parts[2], parts[3])