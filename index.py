import sqlite3
from datetime import date

def register_user(name, email, password, contact):
    today = date.today()
    con = sqlite3.connect('baza.db')
    cur = con.cursor()
    query = cur.execute("INSERT INTO user (name, email, password, contact, created_at) VALUES (?, ?, ?, ?, ?)", (name, email, password, contact, today))
    con.commit()
    con.close()



print("Dobrodošli u Unidu sustav!")
print("Za prijavu upišite broj 1, za registraciju broj 2:")
odabir = int(input("Unesite broj: "))

while odabir != 1 and odabir != 2:
    odabir = int(input("Unesite broj: "))


if odabir == 1:
    print("Dobrodošli u prijavu!")

else:
    print("Dobrodošli u registraciju!")
    name = input("Unesite Vaše ime: ")
    email = input("Unesite e-mail: ")
    pwd = input("Unesite lozinku: ")
    contact = input("Unesite kontakt broj: ")
    register_user(name, email, pwd, contact)
    




    
    
