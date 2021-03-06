import sqlite3
import hashlib
from datetime import date
import time as time

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

def provjera_email(email):
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    query = cur.execute('SELECT * FROM user WHERE email = ?', (email,))
    tupleUser = query.fetchone()
    
    if tupleUser != None:
        return True
        con.commit()
        con.close()
    else:
        return False
        con.commit()
        con.close()
    


def generiraj_hash(email):
    ts = int(time.time())
    sekunde = ts + 1800
    sekunde_pom = time.localtime(sekunde)
    time_plus_30 = time.strftime("%H:%M:%S", sekunde_pom)
    hash_ts = hashlib.sha256(str(ts).encode('utf-8')).hexdigest()
    
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    query = cur.execute('SELECT id FROM user WHERE email = ?', (email,))
    tupleUser = query.fetchone()

    
    user_id = tupleUser[0]
    today = date.today()
    valid_until = str(today) + ' ' + str(time_plus_30)
    
    cur2 = con.cursor()
    query2 = cur2.execute('INSERT INTO forgot_password (user_id, hash, valid_until) VALUES (?, ?, ?)', (user_id, hash_ts, valid_until))

    print('Link za potvrdu je poslan na Vaš e-mail!')

    con.commit()
    con.close()

def resetiraj_pwd(email):
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    query = cur.execute('SELECT id FROM user WHERE email = ?', (email,))
    tupleUser = query.fetchone()

    if tupleUser != None:
        hash_kod = input('Unesite hash kod za promijenu lozinke: ')
        user_id = tupleUser[0]
        cur2 = con.cursor()
        query2 = cur2.execute('SELECT hash FROM forgot_password WHERE user_id = ?', (user_id,))
        tupleHash = query2.fetchone()
        hash_reset =  tupleHash[0]
        if hash_reset == hash_kod:
            nova_pwd = input('Unesi novu lozinku: ')
            potvrdi_pwd = input('Ponovno unesi novu lozinku: ')
            while nova_pwd != potvrdi_pwd:
                print('Lozinke se ne podudaraju! Probajte ponovo.')
                nova_pwd = input('Unesi novu lozinku: ')
                potvrdi_pwd = input('Ponovno unesi novu lozinku: ')
            cur2 = con.cursor()
            update = cur2.execute('UPDATE user SET password = ? WHERE id = ?', (hash_pwd(nova_pwd), user_id))
            print('Lozinka uspješno promijenjena!')
            cur3 = con.cursor()
            delete = cur3.execute('DELETE FROM forgot_password WHERE user_id = ?', (user_id,))
            con.commit()
            con.close()
        else:
            print('Nije moguće promijeniti lozinku!')
            con.commit()
            con.close()
                
    else:
        print('Korisnik s unesenim e-mailom ne postoji!')
        con.commit()
        con.close()
    
    
    
    

print('Dobrodošli u Unidu sustav!')
print('Za prijavu upišite broj 1, za registraciju broj 2,\n za zaboravljenu lozinku broj 3, za promijenu lozinke broj 4: ')
odabir = int(input('Unesite broj: '))

while odabir != 1 and odabir != 2 and odabir != 3 and odabir != 4:
    odabir = int(input('Unesite broj: '))


if odabir == 1:
    print('Dobrodošli u prijavu!')
    email = input('Unesite e-mail: ')
    pwd = input('Unesite lozinku: ')
    login(email, pwd)

elif odabir == 2:
    print('Dobrodošli u registraciju!')
    name = input('Unesite Vaše ime: ')
    email = input('Unesite e-mail: ')
    pwd = input('Unesite lozinku: ')
    contact = input('Unesite kontakt broj: ')
    register_user(name, email, hash_pwd(pwd), contact)

elif odabir == 3:
    print('Zaboravljena lozinka!')
    email = input('Unesite e-mail: ')
    provjera = provjera_email(email)
    if provjera:
        generiraj_hash(email)
    else:
        print('Korisnik s tim e-mailom ne postoji!')

else:
    print('Resetiraj lozinku!')
    email = input('Unesite e-mail: ')
    resetiraj_pwd(email)
    




    
    
