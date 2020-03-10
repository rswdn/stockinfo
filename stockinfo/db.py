import psycopg2

con = psycopg2.connect(
        database='stockinfo',
        user='Ryan',
        password='',
        host='127.0.0.1', 
        port='5432'
        )

cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        );''')
print('Table created successfully')

con.commit()
con.close()


