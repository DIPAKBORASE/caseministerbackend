import psycopg2
from flask import current_app, g

# Your database connection parameters
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "Dipu@1234"
DB_NAME = "caseminister"

def init_db(app):
    # Your initialization logic here, if needed
    app.config['DB_HOST'] = DB_HOST
    app.config['DB_USER'] = DB_USER
    app.config['DB_PASS'] = DB_PASS
    app.config['DB_NAME'] = DB_NAME

def get_db():
    if 'db' not in g:
        # Create a new database connection and store it in the Flask app context
        g.db = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASS'],
            database=current_app.config['DB_NAME']
        )
    return g.db

# Use this function to close the database connection when done
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
