import sqlite3
con = sqlite3.connect('baza.db')

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS user
               (id integer PRIMARY KEY,
               name text NOT NULL,
               email text NOT NULL,
               password text NOT NULL,
               contact text NOT NULL,
               created_at text)''')

cur.execute('''ALTER TABLE user ADD COLUMN count_login integer default 0''')

con.commit()
con.close()

