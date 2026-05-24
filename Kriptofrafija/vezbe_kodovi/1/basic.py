# Problem
# -----------------------
# Ana i Boban zele da komuniciraju poverljivo putem javnog kanala (npr. interneta).
# Eva, koja prisluskuje komunikaciju, ne sme da sazna sadrzaj poruka koje Ana i Boban razmenjuju.
# Na koji nacin Ana i Boban mopgu da ostvare poverljivu komunikaciju?


# Resenje problema
# -----------------------
# Resenje problema svodi se na koriscenje sifri, Ana i Boban mogu unapred da dogovore sifri i kljucu.
# Kljuc je neki tajni podatak poznati samo Ani i Bobanu, a pod sifrom podrazumevamo algoritam koji proizvoljnu poruku pomocu kljuca sifruje.
# Tako sifrovana niska se naziva sifrat.
#
# Formalno sifra je par algoritama (E, D), gde je E algoritam Enkripcije, a D dekripcije.
# Algoritam E proizovdi sifrat c (cipher), a kao argumente uzima poruku m (message) i kljuc k (key) tj. c = E(k, m)
# Algoritam D je inverzna stvar m = D(k, c)


# Klasicne sifre
# -----------------------
#
# Cezarova sifra - najjedsnotavnija moguca, kod nje se ceo alfabet pomera u stranu za fiksan broj mesta k
# Npr. za k = 3, poruka HELLO postaje KHOOR
# Desifrovanje se, jasno, vrsi inverznim mapiranjem karaktera
# Cezarova sifra je jednostavna, ali nebezbedna (postoji samo 25 mogucih kljuceva), pa je laka za brute force
# Npr. za poruku ZRUOG, mozemo redom probati sve k dok ne dobijemo nesto smisleno:
# k=1  YQTNF
# k=2  XPSME
# k=3  WORLD // SMISLENO!

import json
import secrets
from string import ascii_lowercase

from common import bits_to_bytes, bytes_to_bits, xor

with open("english.json", "r") as file:
    freq_eng = json.load(file)


# Ovo se moze napisati na jos nacina, npr. da k bude int i da imamo opciju u kom smeru shiftujemo
def caesar_encrypt_one_letter(message: str, key: str) -> str:
    if not message.islower():
        return message

    ord_m = ascii_lowercase.index(message)
    ord_k = ascii_lowercase.index(key)
    return ascii_lowercase[(ord_m + ord_k) % 26]


def caesar_encrypt(message: str, key: str) -> str:
    return "".join(caesar_encrypt_one_letter(m, key) for m in message)


# Za gore navedenu encrypt funkciju, ovo je decrypt funkcija
def caesar_decrypt_one_letter(cypher, key):
    if not cypher.islower():
        return cypher
    ord_c = ascii_lowercase.index(cypher)
    ord_k = ascii_lowercase.index(key)
    return ascii_lowercase[(ord_c - ord_k + 26) % 26]


def caesar_decrypt(cyphertext: str, key: str) -> str:
    return "".join(caesar_decrypt_one_letter(c, key) for c in cyphertext)


# U slucaju dugackih poruka, razbijanje ove sifre se moze dodatno olaksati statickom analizom frekvencije karaktera.
# Ovako dobijamo informaciju o kom jeziku se radi, sto nam treba da bi mogli da automatizujemo otkrivanje smislenih prevoda.
# Funkcija ispod prikazuje ovo za engleski (tj. detektuje koliko je jezik slican engleksokm na osnovu raspodele karaktera)


def caesar_analyze(message, freq_eng):
    frequencies = {letter: 0.0 for letter in ascii_lowercase}
    for letter in message:
        if letter.islower():
            frequencies[letter] += 1 / len(message)

    score = 0
    for letter in ascii_lowercase:
        score += abs(frequencies[letter] - freq_eng[letter]) / 26
    return score


# Vizenerova sifra
# -------------------
# Vizenerova sifra je unapredjenje nad Cezarovom sifrom koja koristi kljuc u vidu reci umesto fiksnog pomeraja.
# Svako slovo kljuca odredjuje jednu vrednost pomeraja Cezarove sifre (na osnovu svoje pozicije u alfabetu).
# Zatim se svako slovo poruke sifruje Cezarovom sifrom na odgovarajucoj poziciji.
# Npr za rec SECRET:
# S   E   C	  R	  E	  T
# 17  4   2	  16  4	  18
# Onda se poruka HELLO šifruje tako što se H šifruje Cezarovom šifrom sa pomerajem 17, E šifruje Cezarovom šifrom sa pomerajem 4, itd. Rezultat šifrovanja je ZINCS


def vigenere_encrypt_one_letter(message: str, key: str) -> str:
    if not message.islower():
        return message

    ord_m = ascii_lowercase.index(message)
    ord_k = ascii_lowercase.index(key)
    return ascii_lowercase[(ord_m + ord_k) % 26]


def vignere_analyze(message, freq_eng):
    frequencies = {letter: 0.0 for letter in ascii_lowercase}
    for letter in message:
        if letter.islower():
            frequencies[letter] += 1 / len(message)

    score = 0
    for letter in ascii_lowercase:
        score += abs(frequencies[letter] - freq_eng[letter]) / 26

    return score


def vigenere_decrypt_one_letter(cyphertext: str, key: str) -> str:
    if not cyphertext.islower():
        return cyphertext
    ord_c = ascii_lowercase.index(cyphertext)
    ord_k = ascii_lowercase.index(key)
    return ascii_lowercase[(ord_c - ord_k + 26) % 26]


def vigenere_decrypt(message: str, key: str) -> str:
    score = vignere_analyze(message, freq_eng)
    if score < 0.01:
        print()
        print(f"Possible decryption for key {key} with score {score}")
        print(f"{message}")
    return "".join(
        vigenere_encrypt_one_letter(m, key[i % len(key)]) for i, m in enumerate(message)
    )


# Jednokratna sifra (One-time pad)
# ----------------------------------
#
# Jednokratna sifra je sifra koja je teorijski neprobojna ako se koristi na pravilan nacin.
# Kljuc je niz bitova koji je jednako dug kao i poruka. Enkripcija se vrsi tako sto se poruka kombinuje sa kljucem pomocu XOR-a.
# E(k, m) = k XOR m, D(k, c) = k XOR c
#
# Kako bi sifra zaista bila neprobojna, kljuc mora biti slucajno generisan, iste duzine kao i poruka, koriscen samo jednom i cuvan u tajnosti.
# Ako bar jedan od ovih uslova nije ispunjen, sifra postaje podlozna napadima


def generate_key(length: int) -> bytes:
    return bytes(secrets.randbelow(256) for _ in range(length))


def otp_encrypt(message: str, key: str) -> bytes:
    if len(message) != len(key):
        raise ValueError("Message and key must be same length")

    return bytes(ord(m) ^ ord(k) for m, k in zip(message, key))


def otp_decrypt(cipher: bytes, key: str) -> str:
    if len(cipher) != len(key):
        raise ValueError("Cipher and key must be same length")

    return "".join(chr(c ^ ord(k)) for c, k in zip(cipher, key))


# Protocne sifre
# ---------------------------
#
# Protocne sifre se zasnivaju na generisanju random niza bitova na osnovu datog kljuca, koji se na neki nacin kombinuje sa porukom (obicno XOR).
# Formalnije, neka je G presudoslucajni generator (PGR - pseudenoranom generator) koji na osnovu kljuca generise niz bitaova b1 b2 ...
# Tada mozemo definisati protocnu sifru kao par algoritama (E, D) gde je E(k, m) = G(k) XOR m i D(k, c) = G(k) XOR c
#
# LFSR (Linear feedback(povratni) shift register) drzi stanje od n bitova s1, ..., sn. Svaki naredni bit random stanja racuna se po formuli s_i = (c_n AND s_i-n) XOR ... XOR (c_1 AND s_i-1)
# c1, ..., cn su bitovi koji definisu registar i sluze da odaberu bitove trenutnog stanja na onsovu kojih se racuna naredni bit stanja.
# Za LFSR je usko vezan polinom C(x)=cnxn+⋯+c1x+1 sa koeficijentima u 𝔽2
# Na primer, neka je LFSR dužine n=4 definisan polinomom x4+x3+x+1. To znači da se naredni bit stanja računa po formuli si=si−4 XOR si−3 XOR si−1


def lfsr(state: list[int], b: int) -> list[int]:
    stream = state + [0] * b
    for i in range(len(state), len(stream)):
        stream[i] = stream[i - 16] ^ stream[i - 15] ^ stream[i - 13] ^ stream[i - 4]
    return stream[len(state) :]


def lfsr_reverse(state: list[int], b: int) -> list[int]:
    stream = [0] * b + state
    for j in range(b - 1, -1, -1):
        stream[j] = stream[j + 16] ^ stream[j + 12] ^ stream[j + 3] ^ stream[j + 1]
    return stream[:b]


def encrypt(key: bytes, message: bytes) -> bytes:
    keystream = lfsr(bytes_to_bits(key), 8 * len(message))
    return xor(bits_to_bytes(keystream), message)


def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    keystream = lfsr(bytes_to_bits(key), 8 * len(ciphertext))
    return xor(bits_to_bytes(keystream), ciphertext)


def encrypt_iv(key: bytes, iv: bytes, message: bytes) -> bytes:
    keystream = lfsr(bytes_to_bits(key + iv), 8 * len(message))
    return xor(bits_to_bytes(keystream), message)


def decrypt_iv(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    keystream = lfsr(bytes_to_bits(key + iv), 8 * len(ciphertext))
    return xor(bits_to_bytes(keystream), ciphertext)


if __name__ == "__main__":
    # prostor za testiranje
    pass
