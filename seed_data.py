import random
import os
from pony.orm import Database, PrimaryKey, Required, sql_debug, db_session

db_password = 'slJ9J1ABhGg1eic3'

db = Database()

class Book(db.Entity):
  _table_ = 'books'
  id = PrimaryKey(int,auto=True)
  title = Required(str,unique=True)
  author = Required(str)
  rating = Required(float)
  pages = Required(int)

# SQLite
# Store data in a file!
db_params = dict(provider='sqlite', filename='booksdb.sqlite', create_db=True) # The create_db option will create the file if it does not exist.

# CockroachDB 
# https://www.cockroachlabs.com/free-tier/
# db_params = dict(provider='cockroach', user='jayant', host='free-tier.gcp-us-central1.cockroachlabs.cloud', port=26257, database='ample-lemur-3072.defaultdb', password=<INSERT_PASSWORD>)
# Note: You may want to use a Replit environment variables to store the password and database name (see https://docs.replit.com/tutorials/08-storing-secrets-and-history). Note that os.getenv/os.envrion may not work outside of main.py.

sql_debug(True)  # Print all generated SQL queries to stdout
db.bind(**db_params)  # Bind Database object to the real database
db.generate_mapping(create_tables=True)  # Create tables

@db_session
def create_book(id,title, author, rating, pages):
  # the db will assign ids for us
  Book(title=title, author=author, rating=rating, pages=pages)

# Read CSV Data and Create Books
f = open("books.csv", "r")
for line in f:
  parts = line.strip().split(',')
  create_book(parts[0], parts[1], parts[2], float(parts[3]), parts[4])
