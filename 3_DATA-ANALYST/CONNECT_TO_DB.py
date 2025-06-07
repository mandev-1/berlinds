import psycopg2

TABLENAMECONST = "customers"

# Database connection parameters
DB_PARAMS = {
	'dbname': 'piscineds',
	'dbuser': 'mman',
	'dbpassword': 'mysecretpassword',
	'dbhost': 'localhost',
	'dbport': '5432'
}

def setup_connection():
    connection_string = (
        f"dbname='{DB_PARAMS['dbname']}' user='{DB_PARAMS['dbuser']}' "
        f"password='{DB_PARAMS['dbpassword']}' host='{DB_PARAMS['dbhost']}' port='{DB_PARAMS['dbport']}'"
    )
    return psycopg2.connect(connection_string)