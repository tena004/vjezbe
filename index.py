import sqlite3
import hashlib
from datetime import date

def register_user(name, email, password, contact):
    today = date.today()
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    querySelect = cur.execute('SELECT ? FROM user WHERE email = ?', ("*", email))
    if len(querySelect.fetchall())>0:
        print('Korisnik s tim e-mailom već postoji!')
        exit()
    else:
        query = cur.execute('INSERT INTO user (name, email, password, contact, created_at) VALUES (?, ?, ?, ?, ?)', (name, email, password, contact, today))
        print('Uspješna registracija!')
    con.commit()
    con.close()

def login(email, password):
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    query = cur.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, hash_pwd(password)))
    tupleUser = query.fetchone()
    
    if tupleUser != None:
        print('Prijavljeni ste!')
        login_counter = tupleUser[6]
        login_counter += 1
        user_id = tupleUser[0]
        cur2 = con.cursor()
        update = cur2.execute('UPDATE user SET count_login = ? WHERE id = ?', (login_counter, user_id))
        
    else:
        print('Pogrešan e-mail i/ili lozinka. Pokušajte ponovo!')
        
    con.commit()
    con.close()



def hash_pwd(pwd):
    password_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    return password_hash

print('Dobrodošli u Unidu sustav!')
print('Za prijavu upišite broj 1, za registraciju broj 2:')
odabir = int(input('Unesite broj: '))

while odabir != 1 and odabir != 2:
    odabir = int(input('Unesite broj: '))


if odabir == 1:
    print('Dobrodošli u prijavu!')
    email = input('Unesite e-mail: ')
    pwd = input('Unesite lozinku: ')
    login(email, pwd)

else:
    print('Dobrodošli u registraciju!')
    name = input('Unesite Vaše ime: ')
    email = input('Unesite e-mail: ')
    pwd = input('Unesite lozinku: ')
    contact = input('Unesite kontakt broj: ')
    register_user(name, email, hash_pwd(pwd), contact)
    




    
    
