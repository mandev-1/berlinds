# Description: This script creates a PostgreSQL table with specified columns and data types.

# Requirements: The column names must exactly match the ones in the CSV file, and their data
# types must be appropriate. You must use **at least six different data types**.
# • A DATETIME column as the **first column** is mandatory.

# Specification:
# Column names: event_time,event_type,product_id,price,user_id,user_session
# Data types:
# event_time: TIMESTAMP
# event_type: VARCHAR(50)
# product_id: INTEGER
# price: NUMERIC(10, 2)
# user_id: INTEGER
# session: UUID

import psycopg2
import pandas as pd
from uuid import uuid4

# Database connection parameters
DB_PARAMS = {
	'dbname': 'piscineds',
	'dbuser': 'mman',
	'dbpassword': 'mysecretpassword',
	'dbhost': 'localhost',
	'dbport': '5432'
}

# Table name
TABLENAME = "TEST_TABLE"
FILE = "data_2022_oct.csv"
