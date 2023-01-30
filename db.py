import os
import psycopg2
from psycopg2 import DatabaseError
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(user=os.environ.get('DB_USER', "postgres"),
                              password=os.environ.get('DB_PASSWORD', 'default_password'),
                              host=os.environ.get('DB_HOST', "127.0.0.1"),
                              port=os.environ.get('DB_PORT', "5432"),
                              database=os.environ.get('DB_NAME', 'store'))

cursor = connection.cursor()
try:
    cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    cursor.execute("CREATE TABLE Category (id uuid DEFAULT uuid_generate_v4 (), imageUrl VARCHAR(255), name VARCHAR("
                   "255), PRIMARY KEY (id) )")

    cursor.execute("CREATE TABLE Product (id uuid DEFAULT uuid_generate_v4 (), imageUrl VARCHAR(255), name VARCHAR(255), "
                   "description TEXT, price DECIMAL (11, 3), categoryId uuid, "
                   "FOREIGN KEY (categoryId) REFERENCES Category (id), PRIMARY KEY (id)"
                   ")")
except DatabaseError:
    pass

connection.commit()