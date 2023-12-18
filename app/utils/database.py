import mysql.connector
from flask import current_app, g
import psycopg2
# Your database connection parameters
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "caseminister"

# Create a MySQL connector instance
conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

def init_db(app, conn):
    # Your initialization logic here, if needed
    app.config['DB_CONN'] = conn  

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

def get_mysql_conn():
    return mysql_conn 
