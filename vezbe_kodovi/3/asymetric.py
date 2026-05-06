# Problem
# -------------------
# Ana i Boban se nalaze na udaljenim krajevima planete i žele da uspostave enkriptovanu komunikaciju preko javnog kanala.
# Potrebno im je da uspostave zajednički tajni ključ za simetričnu enkripciju. Kako to mogu da urade?
#
# Asimetrična kriptografija, odnosno kriptografija javnog ključa, je pristup koji omogućava rešavanje prethodno opisanog problema.
# Osnovna ideja je da svaki korisnik ima svoj privatni ključ, koji je tajni podatak, kao i svoj javni ključ, koji je dostupan svima.
#
# Na sledeca dva problema se zasniva sigurnost ovakvih sistema:
#
# * Problem 1 - PROBLEM FAKTORIZACIJE
# ---------------
# Dat je prirodan broj n. Odrediti prost broj p takav da p∣n.
# ---------------
#
# Naivni algoritam ovaj problem resava O(sqrt(n)), ovo se mozda cini dobro na prvi pogled,
# ali kad se uzme u obzir da se ovde radi u brojevima velicine 2^4096, ovo je neupotrbeljivo
# Postoje efikasnije varijante, ali nijedna nije ni blizu da bude upotrebljiva
#
# * Problem 2 - PROBLEM DISKRETNOG LOGARITMA
# ---------------
# Data je konačna grupa (G,⋅) i elementi a,b∈G . Odrediti prirodan broj x takav da je ax=b.
# ---------------
#
# Ista situacija kao i u prethodnom problemu
#
# Difi-Helman protokol je prvi objavljen protokol kriptografije javnog kljuca.
# Zasnovan je na problemu diskretnog logaritma i omogucava razmenu privatnog kljuca preko javnog kanala.
# Za ovaj protokol se unapred bira ciklicna grupa G reda q i generator grupe g.
# Tipican izbor je G = Z*_p za prosto p, g je primitivni koren po modulu p, a red grupe q = p-1
#
# Koraci protokola su sledeci:
# 1. Ana i Boban generisu svoje privatne kljuceve a i b slucajnim odabirom iz skupa 1, 2, ..., q-1
# 2. Ana racuna svoj javni kljuc A = g^a i salje ga Bobanu. Boban radi isto sa svojim javnim kljucem B = g^b
# 3. Ana racuna zajednicki tajni kljuc k = B^a, a Boban racuna k' = A^b
#
# Napadacu su poznate vrednosti p, g, A, B, ali ovo nije dovoljno da se izracuna k (tj. jeste ali mora preko problema diskr)
#
# Jedan problem sa ovim protokolom je što je podložan tzv. man-in-the-middle napadu.
# Recimo da Eva kontroliše kanal kojim Ana i Boban komuniciraju.
# Eva može Ani da se predstavi kao Boban, i Bobanu da se predstavi kao Ana, i sa oboje može da izvrši Difi-Helman razmenu ključa.
# Time dobija tajni ključ k1 za komunikaciju sa Anom i tajni ključ k2 za komunikaciju sa Bobanom.
# Kada Ana pošalje poruku Bobanu, ona je šifruje ključem k1, Eva je prihvata i dešifruje, pročita, i šifruje ključem k2 pre nego što je pošalje Bobanu.
# Na ovaj način, Eva može da prisluškuje i menja poruke između Ane i Bobana bez njihovog znanja. U praksi, ovaj problem se rešava nekim vidom autentifikacije.
#


import secrets

# ovde treba staviti neke normalne vrednost :P
g = 1
p = 3


def generate_keys():
    a = secrets.randbelow(p - 2) + 1
    A = pow(g, a, p)
    return a, A


def shared_key(a, B):
    return pow(B, a, p)


# ElGamal enkripcija
#
# ElGamal enkripcija omogućava slanje šifrovanih poruka korišćenjem javnog ključa.
# Svaki korisnik ima svoj privatni ključ i svoj javni ključ.
# Javni ključ može bilo ko da koristi da šifruje poruke, a tako šifrovane poruke jedino može da dešifruje korisnik koji poseduje privatni ključ.
#
# TODO

# RSA enkripcija
#
# RSA slicno ElGamalovom kriptosistemu, omogucava enkripciju poruka koriscenjem javnog kljuca.
# Za razliku od prethodnih protokola, RSA se oslanja na problem faktorizacije.
#
# Korisnik (Ana) generise svoj par privatnog i javnog kljuca na sledeci nacin.
# Bira dva random prosta p i q i racuna n = pq i fi(n) = (p-1)(q-1).
# Zatim bira broj 1 < e < fi(n) koji je uzajamno prost sa fi(n) i racuna d=e^-1 mod fi(n).
# Javni kljuc je par (n, e), a privatni kljuc je broj d.
# Vrednosti p, q i fi(n) se odbacuju i ne smeju biti javno dostupne


def rsa_generate_keys():
    p = number.getPrime(1024)
    q = number.getPrime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 0
    while math.gcd(e, phi) != 1:
        e = secrets.randbelow(phi - 2) + 2
    d = pow(e, -1, phi)

    return d, (n, e)
