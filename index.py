print("Dobrodošli u Unidu sustav!")
print("Za prijavu upišite broj 1, za registraciju broj 2:")
odabir = int(input("Unesite broj: "))

while odabir != 1 and odabir != 2:
    odabir = int(input("Unesite broj: "))


if odabir == 1:
    print("Dobrodošli u prijavu!")

else:
    print("Dobrodošli u registraciju!")
    
