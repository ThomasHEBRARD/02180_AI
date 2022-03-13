import psycopg2

def connector():
    connection = psycopg2.connect(
        host="localhost",
        port="5434",
        user="postgres",
        password="1234",
    )
    return connection
