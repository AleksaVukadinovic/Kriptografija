from common.conversions import blocks_to_bytes, bytes_to_blocks, xor

# Problem
# -------------------------
# Ana i Boban zele da komuniciraju poverljivo putem nebezbednog javnog kanala (npr preko WiFi).
# Eva koja kontrolise kanal moze da prisluskuje komunikaciju, ali i da menja sadrzaj svake poruke.
# Na koji nacin Ana i Boban mogu da ostvare poverljivu komunikaciju i da pritom otkriju ukoliko je poruka bila izmenjena?
#
# Blok šifre su osnovne kriptografske primitive nad kojima je izgrađena većina modernih šifarskih sistema.
# Osim što nude rešenje za problem poverljive komunikacije, takođe omogućavaju konstrukciju takozvane autentifikovane enkripcije.
#
# Formalno, blok sifra je sifra (E, D) pri cemu je velicina poruke samim tim i sifrata fiksirana na n bitova.
# Kazemo da je n velicina bloka. Naglasimo da se, zbog tog uslova, blok sifrom ne mogu direktno sifrovati proizvoljne poruke.
# Za fiksiran kljuc k, funkcija E_k(m) = E(k, m) je permutacija skupa svih bitovskih niski duzine n.
# Cilj prilikom dizajniranja blok sifre je da se fja E_k ponasa kao random permuracija za svaki kljuc k.
#
# Uopsteno, blok sifre se konstruisu iterativnom primenom neke jednostavne invertibilne transformacije koja zavisi od kljuca,
# pri cemu se jedna iteracija naziva runda, a transformacija se naziva funkcija runde.
# Kljuc k se prosiruje u niz podkljuceva k1, ..., kr (po jedan za svaku rundu) pomocu PGR.


# Kao neki pseudo kod za ts
def key_expansion(key: bytes, rounds: int):
    pass


def round_function(key: str, block: bytes):
    pass


def encrypt_block(key: bytes, block: bytes) -> bytes:
    keys = key_expansion(key, rounds)
    for k in keys:
        block = round_function(k, block)
    return block


def decrypt_block(key: bytes, block: bytes) -> bytes:
    keys = key_expansion(key, rounds)
    for k in reversed(keys):
        block = round_inverse(k, block)
    return block


# Dve osnovne komponente koje se koriste u konstrukciji blok sifri  su P-tabela (P-box) i S-tabela(S-box).
# P-tabela vrsi permutaciju pozicija bitova (tj. prelsikava m ulaznih u n izlaznih bitova promenom redosleda).
# S-tabela je komponenta koja vrsi supstituciju, odnosno preslikava m ulaznih bitova u n izlaznih bitova najcesce pomocu lookup tabele.
# Dobro odabrana S-box funkcija uvodi nelinearnost u sifru, otezavajuci kriptoanalizu
#
# Kako bismo sifrovali poruke proizvoljne duzine koristeci blok sifre, potrebno je da definisemo operacioni mod siforvanja:
# -----------------------------
# ECB (Electronic Codebook) je najjednostavniji operacioni mod. Poruka se deli na blokove i svaki se zasebno sifruje.
# Sifrovanje: c_i = E_k(m_i)
# Desifrovanje: m_i = D_k(c_i)
# Prednosti: najlaksi za implementaciju, moguca paralelizacija, otpornost na greske
# Mana: isti blokovi se sifruju u iste blokove
# -----------------------------


def ecb_encrypt(key: bytes, message: bytes) -> bytes:
    blocks = bytes_to_blocks(message, len(message))
    ciphertext = bytes()
    for block in blocks:
        ciphertext += encrypt_block(key, block)
    return ciphertext


def ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    blocks = bytes_to_blocks(ciphertext, len(ciphertext))
    message = bytes()
    for block in blocks:
        message += decrypt_block(key, block)
    return message


# -----------------------------
# Jedan od načina da se prevaziđu nedostaci ECB moda je korišćenjem CBC (eng. Cipher Block Chaining) moda.
# Blok poruke se pre šifrovanja kombinuje sa prethodnim blokom šifrata pomoću xor operacije.
# Za prvi blok se koristi nasumični inicijalizacioni vektor (IV). S
# lično kao i kod ECB moda, poruka se dopunjava do veličine deljive veličinom bloka.
# Sifrovanje: c_i = E_k(c_i − 1 XOR m_i) - mora sekvencijalno tako da je sporije
# Desifrovanje m_i =D_k(c_i) XOR c_i − 1 - moze paralelno
# -----------------------------


def cbc_encrypt(key: bytes, message: bytes, iv: bytes) -> bytes:
    blocks = bytes_to_blocks(message, len(message))
    cipher = [iv]
    for block in blocks:
        cipher.append(encrypt_block(key, xor(block, cipher[-1])))
    return blocks_to_bytes(cipher)


def cbc_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    blocks = bytes_to_blocks(ciphertext, len(ciphertext))
    message = bytes()
    for i in range(1, len(blocks)):
        message += xor(decrypt_block(key, blocks[i]), blocks[i - 1])
    return message


# -----------------------------
# Moderniji pristup šifrovanju blok šifrom je CTR (eng. Counter) mod.
# Ovo je način da se od blok šifre konstruiše protočna šifra.
# Počevši od nekog slučajno odabranog brojača, odnosno inicijalizacionog vektora n (eng. nonce),
# generiše se niz blokova E(k,n),E(k,n+1),E(k,n+2),… . Poruka se kombinuje sa ovim blokovima pomoću xor operacije.
# Za razliku od prethodna dva moda, ovde nije potrebna dopuna poruke.
# Još jedna prednost CTR moda je što se blokovi mogu šifrovati paralelno, što nije slučaj kod CBC moda.
# Takođe, dešifrovanje se ne oslanja na algoritam dešifrovanja blok šifre, što može pojednostaviti implementaciju.
# -----------------------------

block_size = 128  # npr.


def crt_encrypt(key: bytes, message: bytes, n: int) -> bytes:
    keystream = bytes()
    for i in range(0, 1 + len(message) // block_size):
        keystream += encrypt_block(key, int.to_bytes(n + i, block_size))
    return xor(message, keystream)


def crt_decrypt(key: bytes, ciphertext: bytes, n: int) -> bytes:
    keystream = bytes()
    for i in range(0, 1 + len(ciphertext) // block_size):
        keystream += encrypt_block(key, int.to_bytes(n + i, block_size))
    return xor(ciphertext, keystream)
