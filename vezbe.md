# Kriptografija — Materijal za kolokvijum

---

# Nedelja 1: Uvod u kriptografiju

## Šta je kriptografija?

Kriptografija je nauka koja se bavi obezbeđivanjem tri ključna svojstva komunikacije:

1. **Tajnost (Confidentiality)** — niko neovlašćen ne može da pročita poruku
2. **Integritet (Integrity)** — poruka nije menjana tokom prenosa
3. **Autentičnost (Authenticity)** — znamo ko je autor poruke

## Osnovni pojmovi

| Pojam | Značenje |
|---|---|
| **Otvoreni tekst (plaintext)** | Originalna, nešifrovana poruka |
| **Šifrovani tekst (ciphertext)** | Poruka nakon šifrovanja |
| **Ključ (key)** | Tajna vrednost koja kontroliše šifrovanje/dešifrovanje |
| **Šifrovanje (encryption)** | Transformacija otvorenog teksta u šifrovani tekst pomoću ključa |
| **Dešifrovanje (decryption)** | Inverzna operacija — vraćanje šifrovanog teksta u otvoreni |

Formalno:
- Šifrovanje: `C = E(K, M)` gde je M poruka, K ključ, C šifrat
- Dešifrovanje: `M = D(K, C)` i važi `D(K, E(K, M)) = M`

## Osećaj za velike brojeve

Ovo je bitno za razumevanje zašto su neki napadi nepraktični:

- Broj kombinacija za loto (6 od 45): oko 8 miliona ≈ 2²³
- Rastojanje Beograd–Atina u milimetrima: ~600 km = 6×10⁸ ≈ 2³⁰
- Molekuli vazduha u prostoriji: ~10²⁷ ≈ 2⁹⁰
- AES-128 ključ: 2¹²⁸ ≈ 3.4 × 10³⁸ mogućih ključeva
- Računar koji proba 10⁹ ključeva/sec treba ~10²² godina za brute-force AES-128

Poenta: ako je prostor ključeva dovoljno veliki (≥ 2¹²⁸), brute-force napad je nemoguć sa trenutnom tehnologijom.

## Cezarova šifra

Najjednostavniji šifarski sistem — svako slovo se pomera za fiksnu vrednost (ključ).

**Kako radi:**
- Alfabet: A=0, B=1, C=2, ..., Z=25
- Šifrovanje: `c = (m + k) mod 26`
- Dešifrovanje: `m = (c - k) mod 26`

**Primer** (ključ k=3):
```
Otvoreni:  A B C D E F ... X  Y  Z
Šifrovani: D E F G H I ... A  B  C

"NAPAD" → "QDSDG"
```

**Prostor ključeva:** samo 26 mogućih ključeva → trivijalno se razbija (probaj svih 26).

### Kriptoanaliza Cezarove šifre

1. **Brute force:** Probaj svih 26 ključeva, pogledaj koji daje smisleni tekst.
2. **Frekventna analiza:** U engleskom jeziku slovo 'E' je najčešće (~12.7%). Nađi najčešće slovo u šifratu → pomeranje od 'E' do tog slova je verovatno ključ.

## Vigenerova šifra

Proširenje Cezarove šifre — koristi se ključ-reč umesto jednog broja. Svako slovo poruke se šifruje drugim pomeranjem.

**Kako radi:**
- Ključ: reč koja se ciklično ponavlja
- Šifrovanje: `cᵢ = (mᵢ + kᵢ mod len(key)) mod 26`
- Dešifrovanje: `mᵢ = (cᵢ - kᵢ mod len(key)) mod 26`

**Primer** (ključ = "KEY"):
```
Otvoreni tekst:  N A P A D
Ključ (ciklus):  K E Y K E
Pomeranja:       10 4 24 10 4
Šifrovani tekst: X E N K H
```

**Prednost nad Cezarovom:** isto slovo u otvorenom tekstu se šifruje u različita slova (npr. oba 'A' daju različite rezultate jer se koriste različita pomeranja).

**Slabost:** Ključ se ponavlja ciklično. Ako napadač otkrije dužinu ključa (npr. Kasiski test ili indeks koincidencije), problem se svodi na više nezavisnih Cezarovih šifri.

### Kasiski test (ukratko)
Ponovljeni obrasci u šifratu se javljaju na razmacima koji su višekratnici dužine ključa. Analizom razmaka između ponavljanja — NZD tih razmaka daje verovatnu dužinu ključa.

## Kerckhoffsov princip

> Bezbednost šifarskog sistema mora da zavisi **isključivo od tajnosti ključa**, a ne od tajnosti algoritma.

Ovo znači: pretpostavlja se da napadač zna potpuno kako algoritam radi. Jedina tajna je ključ. Svi moderni kriptografski sistemi poštuju ovaj princip — AES, RSA, itd. su javno poznati algoritmi.

## Pregled oblasti kriptografije

```
Kriptografija
├── Simetrična kriptografija (isti ključ za šifrovanje i dešifrovanje)
│   ├── Protočne šifre (stream ciphers)
│   └── Blokovske šifre (block ciphers)
├── Asimetrična kriptografija (javni + privatni ključ)
│   ├── RSA
│   ├── Diffie-Hellman razmena ključeva
│   ├── ElGamal
│   └── Eliptičke krive (ECC)
├── Heš funkcije
│   ├── MD5, SHA-1, SHA-2, SHA-3
│   ├── HMAC
│   └── KDF
└── Primene
    ├── Digitalni potpisi
    ├── Sertifikati (CA)
    ├── Blockchain
    └── ...
```

---

# Nedelja 2: Simetrična kriptografija

Simetrični kriptografski sistem koristi **isti ključ** i za šifrovanje i za dešifrovanje.

```
Alisa                                    Boban
  M ──→ E(K, M) = C ──── kanal ────→ D(K, C) = M
         ↑                                ↑
         K (isti ključ)                    K
```

**Centralni problem:** Kako Alisa i Boban bezbedno razmene ključ K? (Rešava se asimetričnom kriptografijom ili fizičkim kanalima.)

Dve glavne vrste:
1. **Protočne šifre (stream ciphers)** — šifruju bit po bit / bajt po bajt
2. **Blokovske šifre (block ciphers)** — šifruju blokove fiksne dužine

---

## Protočne šifre (Stream Ciphers)

### Princip rada

Generisanje pseudoslučajnog niza bitova (keystream) koji se XOR-uje sa otvorenim tekstom:

```
Ključ (seed) → PRNG → keystream: k₁ k₂ k₃ k₄ ...
Otvoreni tekst:                   m₁ m₂ m₃ m₄ ...
Šifrovani tekst:                  c₁ c₂ c₃ c₄ ...

Šifrovanje: cᵢ = mᵢ ⊕ kᵢ
Dešifrovanje: mᵢ = cᵢ ⊕ kᵢ   (jer x ⊕ y ⊕ y = x)
```

### Zašto XOR?

XOR ima savršena svojstva za kriptografiju:
- `a ⊕ 0 = a` (identitet)
- `a ⊕ a = 0` (samoinverzija)
- `a ⊕ b ⊕ b = a` (dešifrovanje poništava šifrovanje)
- Komutativna i asocijativna

### One-Time Pad (OTP) — savršena šifra

Ako je keystream **potpuno slučajan**, iste dužine kao poruka, i koristi se **samo jednom**, dobijamo One-Time Pad koji je teorijski neprobojan (dokazao Claude Shannon).

**Mane OTP-a:**
- Ključ mora biti iste dužine kao poruka → nepraktično za dugačke poruke
- Ključ se sme koristiti **samo jednom**
- Ključ se mora bezbedno razmeniti

### Zašto se ključ NE SME ponoviti?

Ako se isti keystream K koristi za dve poruke M₁ i M₂:
```
C₁ = M₁ ⊕ K
C₂ = M₂ ⊕ K

C₁ ⊕ C₂ = M₁ ⊕ K ⊕ M₂ ⊕ K = M₁ ⊕ M₂
```
Napadač dobija XOR dve poruke u otvorenom tekstu! Iz toga može statistički da rekonstruiše obe poruke (poznavanje jedne otkriva drugu).

### Pseudoslučajni generatori (PRNG)

Pošto OTP nije praktičan, koriste se PRNG-ovi koji od kratkog ključa (seed) generišu dugačak keystream koji **izgleda** slučajno.

**Zahtevi za kriptografski PRNG:**

| Svojstvo | Objašnjenje |
|---|---|
| **Veliki period** | Niz se ne ponavlja pre nego što se generiše ogroman broj bitova |
| **Prolazi statističke testove** | NIST SP 800-22 testovi za randomnost (frekvencija, runs, FFT, itd.) |
| **Velika linearna složenost** | Ne može se opisati kratkim LFSR-om |
| **Nepredvidivost sledećeg bita** | Čak i ako napadač zna prvih milijardu bitova, verovatnoća da pogodi sledeći bit je ≤ 50% |

**Primeri protočnih šifri:**
- **RC4** — probijena, ne koristi se više
- **A5/1** — koristi se u GSM mrežama, teorijski probijena ali se još koristi
- **ChaCha20** — moderna, sigurna, koristi se u TLS 1.3, WireGuard, itd.

---

## Blokovske šifre (Block Ciphers)

Šifruju blok otvorenog teksta fiksne dužine u blok šifrovanog teksta iste dužine, koristeći ključ.

```
E: {0,1}ⁿ × {0,1}ᵏ → {0,1}ⁿ

n = dužina bloka
k = dužina ključa
```

### Padding — dopunjavanje poruke

Ako poruka nije deljiva sa dužinom bloka, mora se dopuniti.

**PKCS#7 padding:**
- Ako treba dopuniti sa N bajtova → svaki dopunjeni bajt ima vrednost N
- Ako je poruka **već deljiva** sa veličinom bloka → dodaje se ceo novi blok gde svaki bajt = veličina bloka

```
Blok = 8 bajtova

Poruka: [AA BB CC]           → [AA BB CC 05 05 05 05 05]     (5 bajtova dopune)
Poruka: [AA BB CC DD EE FF]  → [AA BB CC DD EE FF 02 02]     (2 bajta dopune)
Poruka: [AA BB CC DD EE FF GG HH] → [AA BB CC DD EE FF GG HH 08 08 08 08 08 08 08 08]
                                      ↑ ceo novi blok jer je već deljivo sa 8
```

Zašto dodati blok kad je već deljivo? Da bi dešifrovanje bilo jednoznačno — uvek se gleda poslednji bajt i ukloni toliko bajtova.

### DES (Data Encryption Standard)

- **Blok:** 64 bita
- **Ključ:** 56 bita (nominalno 64, ali 8 bitova su paritet)
- **Struktura:** 16 rundi Feistel mreže
- **Status:** **Zastareo** — 2⁵⁶ ≈ 7.2 × 10¹⁶ ključeva, probija se za < 1 dan na specijalizovanom hardveru

**3DES (Triple DES):**
- Primenjuje DES tri puta: `C = E(K₁, D(K₂, E(K₁, M)))` (sa 2 ključa) ili `C = E(K₃, D(K₂, E(K₁, M)))` (sa 3 ključa)
- Varijanta sa 2 ključa: efektivna sigurnost ~2¹¹² (ne 2¹¹² već manje zbog Meet-in-the-Middle napada)
- Varijanta sa 3 ključa: nije mnogo sigurnija od varijante sa 2, a teže je razmeniti 3 ključa

**Meet-in-the-Middle napad (na dvostruki DES):**

Zašto ne koristimo prosto 2DES (duplo šifrovanje)? `C = E(K₂, E(K₁, M))`

```
Napad:
1. Za poznati par (M, C):
2. Izračunaj E(K₁, M) za svaki mogući K₁ → čuvaj u tabeli
3. Izračunaj D(K₂, C) za svaki mogući K₂ → traži poklapanje u tabeli
4. Složenost: 2⁵⁶ + 2⁵⁶ = 2⁵⁷ (umesto očekivanih 2¹¹²)
```

Dvostruki DES sa 2×56=112 bita ključa daje samo 2⁵⁷ sigurnosti — skoro ništa bolje od običnog DES-a!

### AES (Advanced Encryption Standard)

Naslednik DES-a, danas **najkorišćenija** blokovska šifra.

| Parametar | Vrednost |
|---|---|
| **Blok** | 128 bita (16 bajtova) |
| **Ključ** | 128, 192 ili 256 bita |
| **Runde** | 10 (AES-128), 12 (AES-192), 14 (AES-256) |
| **Struktura** | Substitucijsko-permutacijska mreža (SPN), nije Feistel |

**Svaka runda AES-a se sastoji od 4 operacije:**
1. **SubBytes** — nelinearna supstitucija (S-box), svaki bajt se zameni drugim prema fiksnoj tabeli
2. **ShiftRows** — ciklično pomeranje redova matrice stanja (0, 1, 2, 3 pozicije)
3. **MixColumns** — mešanje kolona — linearna transformacija u GF(2⁸) (ne radi se u poslednjoj rundi)
4. **AddRoundKey** — XOR sa rundnim ključem (izvedenim iz glavnog ključa)

```
Otvoreni tekst (128b)
       ↓
  AddRoundKey (ključ runde 0)
       ↓
  ┌─── Runda 1-9 (ili 11, 13) ───┐
  │  SubBytes                      │
  │  ShiftRows                     │
  │  MixColumns                    │
  │  AddRoundKey                   │
  └────────────────────────────────┘
       ↓
  Poslednja runda (bez MixColumns)
  │  SubBytes                      │
  │  ShiftRows                     │
  │  AddRoundKey                   │
       ↓
  Šifrovani tekst (128b)
```

**OpenSSL komande:**
```bash
# Šifrovanje
openssl enc -aes-256-cbc -out proba.txt

# Dešifrovanje
openssl enc -d -aes-256-cbc -in proba.txt
```

---

## Modovi rada blokovskih šifri

Blokovska šifra sama po sebi šifruje samo jedan blok. Da bi šifrovali poruku dužu od jednog bloka, koriste se **modovi rada**.

### ECB — Electronic Codebook

Najjednostavniji mod: svaki blok se šifruje nezavisno.

```
Šifrovanje: Cᵢ = E(K, Mᵢ)
Dešifrovanje: Mᵢ = D(K, Cᵢ)
```

```python
def encrypt(key, message):
    blocks = bytes_to_blocks(message)
    ciphertext = bytes()
    for block in blocks:
        ciphertext += encrypt_block(key, block)
    return ciphertext

def decrypt(key, ciphertext):
    blocks = bytes_to_blocks(ciphertext)
    message = bytes()
    for block in blocks:
        message += decrypt_block(key, block)
    return message
```

| Prednosti | Mane |
|---|---|
| Jednostavan za implementaciju | **Isti blokovi otvorenog teksta → isti blokovi šifrata** |
| Paralelizacija i šifrovanja i dešifrovanja | Otkriva obrasce u podacima |
| Greška u jednom bloku ne utiče na druge | Nesiguran za većinu primena |

**Poznati primer:** ECB Tux pingvin — šifrovanje slike u ECB modu ostavlja obrise vidljivim jer se isti pikseli šifruju u iste blokove.

⚠️ **ECB se nikada ne koristi u praksi za podatke koji imaju bilo kakvu strukturu!**

### CBC — Cipher Block Chaining

Svaki blok se pre šifrovanja XOR-uje sa prethodnim šifrovanim blokom.

```
Šifrovanje: C₀ = IV,  Cᵢ = E(K, Cᵢ₋₁ ⊕ Mᵢ)
Dešifrovanje: Mᵢ = D(K, Cᵢ) ⊕ Cᵢ₋₁
```

```
Šifrovanje:            Dešifrovanje:
Mᵢ ──⊕──→ E(K) → Cᵢ     Cᵢ → D(K) ──⊕──→ Mᵢ
      ↑                              ↑
     Cᵢ₋₁                          Cᵢ₋₁
```

```python
def encrypt(key, message, iv):
    blocks = bytes_to_blocks(message)
    cipher = [iv]
    for block in blocks:
        cipher.append(encrypt_block(key, xor(block, cipher[-1])))
    return blocks_to_bytes(cipher)

def decrypt(key, ciphertext):
    blocks = bytes_to_blocks(ciphertext)
    message = bytes()
    for i in range(1, len(blocks)):
        message += xor(decrypt_block(key, blocks[i]), blocks[i-1])
    return message
```

| Prednosti | Mane |
|---|---|
| Isti blokovi daju različite šifrate | Šifrovanje je **sekvencijalno** (sporo) |
| Dešifrovanje je paralelizabilno | IV se ne sme ponavljati sa istim ključem |
| Široko korišćen i dobro proučen | Osetljiv na padding oracle napade |

### CTR — Counter Mode

Pretvara blokovsku šifru u protočnu šifru. Šifruje brojač (nonce + counter) i XOR-uje sa otvorenim tekstom.

```
Keystream: Kᵢ = E(K, nonce || i)
Šifrovanje: Cᵢ = Mᵢ ⊕ Kᵢ
Dešifrovanje: Mᵢ = Cᵢ ⊕ Kᵢ   (identično šifrovanju!)
```

```
nonce||0 → E(K) → ⊕ M₀ = C₀
nonce||1 → E(K) → ⊕ M₁ = C₁
nonce||2 → E(K) → ⊕ M₂ = C₂
...
```

```python
def encrypt(key, message, n):   # n = nonce
    keystream = bytes()
    for i in range(0, 1 + len(message) // block_size):
        keystream += encrypt_block(key, int.to_bytes(n + i, block_size))
    return xor(message, keystream)

def decrypt(key, ciphertext, n):  # identično encrypt-u!
    keystream = bytes()
    for i in range(0, 1 + len(ciphertext) // block_size):
        keystream += encrypt_block(key, int.to_bytes(n + i, block_size))
    return xor(ciphertext, keystream)
```

| Prednosti | Mane |
|---|---|
| Potpuna paralelizacija (i šifrovanje i dešifrovanje) | Ponovljeni nonce → potpuno kompromitovanje |
| Ne treba padding | Nema zaštite integriteta — napadač može menjati bitove šifrata |
| Koristi se samo E(K), nikad D(K) | |
| Random pristup blokovima | |

**Zašto ponovljeni nonce u CTR ubija?** Isto kao kod protočnih šifri — isti keystream za dve poruke daje napadaču M₁ ⊕ M₂.

### GCM — Galois/Counter Mode

Najkorišćeniji mod u praksi. Kombinuje CTR mod za šifrovanje + **autentikacioni tag** (GMAC) za zaštitu integriteta.

```
GCM = CTR šifrovanje + GHASH autentikacioni kod
```

- Generiše **šifrovani tekst** i **autentikacioni tag** (obično 128 bita)
- Tag potvrđuje da poruku nije niko menjao i da ju je generisao neko ko zna ključ
- Podržava **Additional Authenticated Data (AAD)** — podaci koji se ne šifruju ali se štite od izmene
- Ovo je primer **AEAD** (Authenticated Encryption with Associated Data)

**AEAD koncept:**
Šifrovanje + autentikacija u jednom koraku. Deo podataka može biti nešifrovan ali zaštićen od izmene (kao adresa na koverti — mora biti čitljiva da pismo stigne, ali ne sme biti menjana).

### Uporedna tabela modova

| Mod | Paralelno šifrovanje | Paralelno dešifrovanje | Treba IV/nonce | Integritet | Sigurnost |
|-----|-----|-----|-----|-----|-----|
| ECB | ✅ | ✅ | ❌ | ❌ | ⛔ Nesiguran |
| CBC | ❌ | ✅ | ✅ (IV) | ❌ | ✅ Za šifrovanje |
| CTR | ✅ | ✅ | ✅ (nonce) | ❌ | ✅ Ali menjiv šifrat |
| GCM | ✅ | ✅ | ✅ (nonce) | ✅ (tag) | ✅ Preporučen |

---

## Gde se koristi simetrična kriptografija

- **Komunikacija:** HTTPS (TLS), VPN, SSH, WiFi (WPA2/3), Bluetooth
- **Šifrovanje diska:** BitLocker, FileVault, LUKS
- **Aplikacije:** Password manageri, End-to-End enkripcija (Signal, WhatsApp)
- **PRNG:** Generisanje pseudoslučajnih bitova (CTR_DRBG koristi AES u CTR modu)

---

# Nedelja 3: Asimetrična kriptografija

## Zašto postoji asimetrična kriptografija?

Simetrična kriptografija ima fundamentalan problem: **kako dva korisnika bezbedno razmene ključ?**

- Ako Alisa želi da komunicira sa 100 ljudi, treba joj 100 različitih ključeva
- Za N korisnika treba N×(N-1)/2 ključeva — ne skalira se
- Ključ se mora razmeniti pre komunikacije — ali kanal nije siguran

Asimetrična kriptografija rešava ovo: svako ima **par ključeva**:
- **Javni ključ** — poznat svima, koristi se za šifrovanje
- **Privatni ključ** — poznat samo vlasniku, koristi se za dešifrovanje

```
Alisa                                        Boban
                                        (generiše par ključeva)
                                        Javni ključ: Kpub
                                        Privatni ključ: Kpriv

Alisa dobije Bobov javni ključ Kpub
C = E(Kpub, M) ────── kanal ──────→ M = D(Kpriv, C)
```

Bilo ko može da šifruje poruku Bobovim javnim ključem, ali **samo Boban** može da je dešifruje.

## Matematička osnova

Asimetrična kriptografija se zasniva na **jednosmernim funkcijama** — funkcijama koje je lako izračunati u jednom smeru, ali praktično nemoguće invertovati.

| Problem | Lako | Teško |
|---|---|---|
| **Faktorizacija** | Pomnožiti dva prosta broja p×q | Od proizvoda n naći p i q |
| **Diskretni logaritam** | Izračunati g^a mod p | Od g^a mod p naći a |
| **ECC diskretni logaritam** | Izračunati a×P (tačka na krivoj) | Od a×P naći a |

## Mesi-Omura protokol (idejno)

Analogija sa katancima — ilustruje da je moguća bezbedna komunikacija bez zajedničkog ključa:

```
1. Alisa stavlja poruku u kutiju, zaključava SVOJIM katancem → šalje Bobanu
2. Boban NE MOŽE otvoriti, ali stavlja i SVOJ katanac → šalje nazad Alisi
3. Alisa skida SVOJ katanac → šalje Bobanu
4. Boban skida SVOJ katanac → čita poruku
```

Niko osim Alise i Bobana nije mogao da čita poruku, a nikad nisu razmenili ključ!

## RSA (Rivest–Shamir–Adleman)

Najpoznatiji asimetrični kriptosistem. Zasniva se na **težini faktorizacije velikih brojeva**.

### Generisanje ključeva

```
1. Izaberi dva velika prosta broja: p, q
2. Izračunaj: n = p × q
3. Izračunaj: φ(n) = (p-1)(q-1)       ← Ojlerova funkcija
4. Izaberi e tako da: 1 < e < φ(n) i NZD(e, φ(n)) = 1
   (najčešće e = 65537 = 2¹⁶ + 1)
5. Izračunaj d tako da: e × d ≡ 1 (mod φ(n))
   (d je modularni inverz od e)

Javni ključ:   (n, e)
Privatni ključ: (n, d)    [p, q se brišu ili čuvaju za optimizaciju]
```

### Šifrovanje i dešifrovanje

```
Šifrovanje:   C = M^e mod n    (koristi javni ključ)
Dešifrovanje: M = C^d mod n    (koristi privatni ključ)
```

**Zašto radi?** Iz Ojlerove teoreme: M^(e×d) ≡ M^(1 + k×φ(n)) ≡ M × (M^φ(n))^k ≡ M × 1^k ≡ M (mod n)

### Konkretan primer (p=11, q=5)

```
1. p = 11, q = 5
2. n = 11 × 5 = 55
3. φ(n) = (11-1)(5-1) = 10 × 4 = 40
4. Biramo e = 3  (NZD(3, 40) = 1 ✓)
5. Tražimo d: 3 × d ≡ 1 (mod 40)
   3 × 27 = 81 = 2×40 + 1 → d = 27

Javni ključ:   (55, 3)
Privatni ključ: (55, 27)

Šifrovanje poruke M = 7:
  C = 7³ mod 55 = 343 mod 55 = 13

Dešifrovanje:
  M = 13²⁷ mod 55 = 7 ✓
```

### Sigurnost RSA

- Zasniva se na tome da je **faktorizacija n na p i q** teška
- Ako napadač faktorizuje n, može izračunati φ(n), pa d, i dešifrovati sve
- Preporučene dužine ključa: **2048 bita** (minimum), **4096 bita** (dugoročno)
- RSA-768 (232 cifre) je faktorizovan 2009. godine
- RSA-2048 (617 cifara) se smatra sigurnim do ~2030+

### .pem fajlovi

RSA ključevi se čuvaju u PEM formatu (Base64 kodirani). Sadrže: p, q, n, e, d.

```bash
# Generisanje RSA ključa
openssl genrsa -out kljuc.pem 2048

# Prikaz detalja (p, q, n, e, d)
openssl rsa -in kljuc.pem -text -noout
```

## Diffie-Hellman razmena ključeva (DH)

Nije sistem za šifrovanje, već protokol kojim dve strane **dogovaraju zajednički tajni ključ** preko nesigurnog kanala.

Zasniva se na **problemu diskretnog logaritma**: lako je izračunati g^a mod p, ali je iz rezultata praktično nemoguće naći a.

### Protokol korak po korak

```
═══ JAVNI PARAMETRI (poznati svima) ═══
  p = veliki prost broj
  g = generator grupe mod p

═══ ALISA ═══                    ═══ BOBAN ═══
a = random()  ← privatno         b = random()  ← privatno
A = g^a mod p ← javno            B = g^b mod p ← javno

         Alisa ──── A ────→ Boban
         Alisa ←─── B ────  Boban

═══ RAČUNANJE ZAJEDNIČKE TAJNE ═══
Alisa: S = B^a mod p             Boban: S = A^b mod p
     = (g^b)^a mod p                  = (g^a)^b mod p
     = g^(ab) mod p                   = g^(ab) mod p
                    ↑ ISTO! ↑

Zajednička tajna: S = g^(ab) mod p
```

**Šta napadač vidi?** g, p, A = g^a mod p, B = g^b mod p. Da bi izračunao S = g^(ab) mod p, morao bi da nađe a ili b — a to je problem diskretnog logaritma!

**Napomena:** DH sam po sebi ne štiti od **Man-in-the-Middle** napada (Iva se ubaci između i uradi DH sa obe strane). Zato se kombinuje sa sertifikatima.

## ElGamal šifrovanje

Asimetrični kriptosistem zasnovan na **problemu diskretnog logaritma** (kao i DH). Može se koristiti i za šifrovanje i za digitalne potpise.

### Generisanje ključeva

```
1. Javni parametri: veliki prost p, generator g
2. Privatni ključ: x = random iz {1, ..., p-2}
3. Javni ključ: y = g^x mod p
```

### Šifrovanje i dešifrovanje

```
Šifrovanje poruke M (pošiljalac bira random k):
  c₁ = g^k mod p
  c₂ = M × y^k mod p
  Šifrat: (c₁, c₂)

Dešifrovanje (primalac koristi privatni ključ x):
  S = c₁^x mod p          ← zajednička tajna
  M = c₂ × S^(-1) mod p   ← S^(-1) je modularni inverz od S
```

**Zašto radi?**
- S = c₁^x = (g^k)^x = g^(kx) mod p
- c₂ = M × y^k = M × (g^x)^k = M × g^(kx) mod p
- M = c₂ × (g^(kx))^(-1) = M × g^(kx) × g^(-kx) = M mod p ✓

**Bitna razlika od RSA:** šifrat je **dva puta duži** od otvorenog teksta (šalje se par (c₁, c₂)).

**Upozorenje:** random k se **mora menjati** za svako šifrovanje. Ponavljanje k potpuno kompromituje sistem.

---

## Eliptičke krive (ECC — Elliptic Curve Cryptography)

### Jednačina

Eliptička kriva nad konačnim poljem F_p:

```
y² ≡ x³ + ax + b  (mod p)

gde je 4a³ + 27b² ≠ 0 (da kriva nema singularitete)
```

Tačke na krivoj + specijalna "tačka u beskonačnosti" O (neutralni element) čine **grupu**.

### Operacije na krivoj

**Sabiranje tačaka (P + Q, gde P ≠ Q):**
```
Geometrijski: povuci pravu kroz P i Q, ona seče krivu u trećoj tački R'.
Reflektuj R' preko x-ose → to je P + Q = R.

Algebarski (mod p):
  λ = (y₂ - y₁) × (x₂ - x₁)^(-1) mod p
  x₃ = λ² - x₁ - x₂ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p
```

**Dupliranje tačke (P + P = 2P):**
```
Geometrijski: tangenta na krivu u tački P seče krivu u R', reflektuj → 2P.

Algebarski:
  λ = (3x₁² + a) × (2y₁)^(-1) mod p
  x₃ = λ² - 2x₁ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p
```

**Skalarno množenje:** n × P = P + P + ... + P (n puta)
- Efikasno se računa algoritmom "double-and-add" (analogno brzom stepenovanom) u O(log n) koraka

### Diskretni logaritam na eliptičkim krivama (ECDLP)

```
Dato: tačka P i tačka Q = n × P na krivoj
Naći: n
```

Ovo je **teže** nego klasičan diskretni logaritam u Z_p — nema poznatih sub-eksponencijalnih algoritama za opšte krive.

### Glavna prednost ECC

**Ista sigurnost sa mnogo kraćim ključevima:**

| ECC ključ | RSA ključ | Sigurnost (bitovi) |
|---|---|---|
| 160 bita | 1024 bita | ~80 bita |
| 256 bita | 3072 bita | ~128 bita |
| 384 bita | 7680 bita | ~192 bita |
| 521 bit | 15360 bita | ~256 bita |

Kraći ključevi → brže operacije, manje memorije, manji sertifikati. Zato se ECC koristi na mobilnim uređajima, IoT, TLS 1.3, Bitcoin (secp256k1), itd.

---

## Digitalni potpisi

Digitalni potpis je kriptografski mehanizam koji obezbeđuje:
1. **Autentičnost** — znamo ko je autor
2. **Integritet** — poruka nije menjana
3. **Neporecivost** — autor ne može da porekne da je potpisao

### Kako radi

```
Potpisivanje (pošiljalac — koristi PRIVATNI ključ):
  1. Izračunaj heš poruke: h = H(M)
  2. Šifruj heš privatnim ključem: sig = Sign(Kpriv, h)
  3. Pošalji: (M, sig)

Verifikacija (primalac — koristi JAVNI ključ):
  1. Izračunaj heš primljene poruke: h' = H(M)
  2. Dekriptuj potpis javnim ključem: h = Verify(Kpub, sig)
  3. Proveri: h == h' → potpis je validan ✓
```

```
               Potpisivanje                    Verifikacija

Poruka ──→ H() ──→ heš ──→ Sign(Kpriv) → sig    sig ──→ Verify(Kpub) → heš
                                                  Poruka ──→ H() ──→ heš'
                                                  heš == heš' ? ✓ : ✗
```

**Razlika od HMAC-a:**
- HMAC: simetrični — ko god ima ključ može i da generiše i da verifikuje → ne daje neporecivost
- Digitalni potpis: asimetrični — samo vlasnik privatnog ključa može da potpiše, ali **svako** sa javnim ključem može da verifikuje

### Sign-then-Encrypt vs Encrypt-then-Sign

| Pristup | Postupak | Napomena |
|---|---|---|
| **Sign-then-Encrypt** | Potpis + poruka → šifruj sve | Smatra se **boljim** — potpis štiti originalni tekst |
| **Encrypt-then-Sign** | Šifruj poruku → potpiši šifrat | Potpis nad šifratom, ne nad originalnom porukom |

---

## Sertifikati i CA (Certificate Authority)

### Man-in-the-Middle napad (MITM)

Problem sa DH i svim asimetričnim sistemima bez autentikacije:

```
Alisa ←──── Iva ────→ Boban
        (napadač)

1. Alisa misli da komunicira sa Bobanom, ali zapravo komunicira sa Ivom
2. Iva radi DH sa Alisom (dobija ključ K₁)
3. Iva radi DH sa Bobanom (dobija ključ K₂)
4. Iva dešifruje poruke od Alise sa K₁, čita ih, ponovo šifruje sa K₂ i šalje Bobanu
```

Alisa i Boban ne znaju da Iva čita sve! Rešenje: **sertifikati** — potvrda identiteta.

### Šta je sertifikat?

Digitalni dokument koji vezuje **javni ključ za identitet**. Sadrži:

| Polje | Opis |
|---|---|
| Javni ključ | Ključ vlasnika sertifikata |
| Identitet | Domen (npr. google.com), opciono vlasnik |
| Izdavač | CA koji je potpisao sertifikat |
| Period važenja | Od–do datuma |
| Namena | Za šta se sme koristiti |
| **Potpis CA** | Digitalni potpis izdavača — ovo garantuje autentičnost |

### Kako funkcioniše sistem sertifikata

```
1. Server generiše par ključeva (privatni/javni)
2. Server šalje zahtev (CSR) za sertifikat ka CA
3. CA proverava podatke iz zahteva (da li podnosilac zaista kontroliše domen itd.)
4. CA generiše sertifikat (potpisuje ga SVOJIM privatnim ključem)
5. Server stavlja sertifikat na server
6. Klijent pri konekciji dobija sertifikat
7. Klijent verifikuje potpis CA koristeći javni ključ tog CA
```

### Lanac poverenja (Chain of Trust)

Postoji mali broj **Root CA** (Verisign, DigiCert, Let's Encrypt, ...) čiji su javni ključevi ugrađeni u browser/OS.

```
Root CA (self-signed, ugrađen u browser)
  └── Intermediate CA (potpisan od Root CA)
        └── Server sertifikat (potpisan od Intermediate CA)
```

Klijent se penje lancem sertifikata dok ne dođe do Root CA kome veruje.

### Opozivanje sertifikata

Šta kad sertifikat više ne važi (kompromitovan privatni ključ, promena vlasništva)?

| Metod | Opis | Mane |
|---|---|---|
| **CRL** (Certificate Revocation List) | Lista opozvanih sertifikata koju objavljuje CA | Može biti ogromna, browseri često ignorišu |
| **OCSP** (Online Certificate Status Protocol) | Klijent pita CA za konkretni sertifikat u realnom vremenu | Privatnost (CA zna koje sajtove posećuješ), latencija |
| **OCSP Stapling** | Server sam pita CA, kešira odgovor, i šalje ga klijentu uz sertifikat | Bolje od OCSP, danas najčešće korišćen |

---

## Vremenski pečati (TSA — Time Stamping Authority)

Dokaz da je dokument postojao u određenom trenutku.

```
1. Izračunaj heš dokumenta: h = H(dokument)
2. Pošalji h ka TSA
3. TSA nadoveže tačno vreme na heš i potpiše: potpis = Sign(Ktsa_priv, h || vreme)
4. Dobiješ vremenski pečat: (h, vreme, potpis)
```

Alternativa centralizovanom TSA: **blockchain** (decentralizovano) — heš se upiše u blockchain transakciju čiji je timestamp neopoziv.

---

## Onion šifrovanje

Tehnika za **anonimnu komunikaciju** (Tor mreža).

```
Alisa želi da pošalje poruku serveru S preko 3 čvora (N₁, N₂, N₃):

1. Alisa šifruje poruku u 3 sloja:
   C = E(K₁, E(K₂, E(K₃, M)))

2. Prolazak kroz mrežu:
   N₁: skida spoljni sloj → dobija E(K₂, E(K₃, M)) → šalje N₂
   N₂: skida drugi sloj  → dobija E(K₃, M)          → šalje N₃
   N₃: skida poslednji   → dobija M                   → šalje S

3. Nijedan čvor ne zna i pošiljaoca i primaoca:
   N₁ zna: Alisa → N₂       (ne zna krajnje odredište)
   N₂ zna: N₁ → N₃          (ne zna ni pošiljaoca ni primaoca)
   N₃ zna: N₂ → S           (ne zna ko je originalni pošiljalac)
```

## Garlic šifrovanje

Slično onion-u, ali sa grupnim slanjem (I2P mreža):

- Više poruka se kombinuje u **jedan paket** (kao čenovi belog luka)
- Svaki čvor dešifruje samo deo koji mu je namenjen
- Jedan garlic paket sadrži poruke za **različite primaoce** → teže je analizirati saobraćaj
- Komunikacija je uglavnom **unutar same mreže** (retko za pristup javnom internetu)

---

## Gde se koristi asimetrična kriptografija

- **Razmena ključeva:** DH u TLS, SSH, VPN
- **Autentifikacija servera:** HTTPS sertifikati
- **Digitalni potpisi:** PDF, online ugovori, git commitovi, blockchain transakcije
- **Login bez lozinke:** SSH ključevi
- **Vremenski pečati:** TSA, blockchain
- **Šifrovanje mejlova:** PGP (Web of Trust — decentralizovan model poverenja bez CA)

---

# Nedelja 4: Heš funkcije

Heš funkcija je funkcija koja ulaz **proizvoljne dužine** transformiše u izlaz **fiksne dužine**.

```
H: {0,1}* → {0,1}ⁿ

Bilo koji podatak (1 bajt, 1 GB, 1 TB) → uvek isti broj bitova (npr. 256)
```

## Svojstva heš funkcija

| Svojstvo | Definicija | Zašto je bitno |
|---|---|---|
| **Determinističnost** | H(x) uvek daje isti rezultat y | Mora biti ponovljivo |
| **Fiksna dužina izlaza** | Izlaz je uvek isti broj bitova (128–512b) | Nezavisno od veličine ulaza |
| **Brzo računanje** | H(x) se efikasno izračunava | Praktična upotrebljivost |
| **Jednosmernost (preimage resistance)** | Dato y, praktično nemoguće naći x tako da H(x) = y | Iz heša ne možeš rekonstruisati original |
| **Slaba otpornost na kolizije (2nd preimage)** | Dato x, nemoguće naći x' ≠ x tako da H(x) = H(x') | Ne možeš naći drugi dokument sa istim hešom |
| **Jaka otpornost na kolizije** | Nemoguće naći **bilo koje** x ≠ x' tako da H(x) = H(x') | Ne mogu se konstruisati dva dokumenta sa istim hešom |

**Hijerarhija:** Jaka otpornost ⇒ Slaba otpornost ⇒ Jednosmernost (ali ne važi obrnuto).

## Rođendanski paradoks

Objašnjava zašto nam treba heš od **bar 160 bita**.

**Paradoks:** U grupi od 23 osobe verovatnoća da dve imaju isti rođendan je > 50%.

**Uticaj na kriptografiju:**
- Heš od n bita ima 2ⁿ mogućih izlaza
- Brute-force za jednosmernost: ~2ⁿ pokušaja
- Brute-force za koliziju (rođendanski napad): ~2^(n/2) pokušaja!

```
Heš dužina    Kolizija (brute-force)
  128 bita  →  2⁶⁴ pokušaja   ← premalo, praktično izvodljivo!
  160 bita  →  2⁸⁰ pokušaja   ← granično
  256 bita  →  2¹²⁸ pokušaja  ← sigurno
  512 bita  →  2²⁵⁶ pokušaja  ← više nego dovoljno
```

Zato MD5 (128b) i SHA-1 (160b) **nisu sigurni** za primene gde je bitna otpornost na kolizije.

## Primeri heš funkcija

| Algoritam | Izlaz | Status |
|---|---|---|
| **MD5** | 128 bita | ⛔ Probijen — kolizije se nalaze za sekunde |
| **SHA-0** | 160 bita | ⛔ Probijen |
| **SHA-1** | 160 bita | ⛔ Probijen (Google, 2017 — SHAttered napad) |
| **SHA-2** (SHA-224/256/384/512) | 224–512 bita | ✅ Siguran, najkorišćeniji danas |
| **SHA-3** (SHA3-224/256/384/512) | 224–512 bita | ✅ Siguran, drugačija konstrukcija (Keccak/sponge) |
| **RIPEMD-160** | 160 bita | ⚠️ Koristi se u Bitcoin-u |
| **Whirlpool** | 512 bita | ✅ Siguran |

**Razlika SHA-2 vs SHA-3:** SHA-2 koristi Merkle-Damgård konstrukciju, SHA-3 koristi **sponge** konstrukciju — potpuno drugačiji dizajn, otporan na napade specifične za Merkle-Damgård.

---

## Primene heš funkcija

### 1. Digitalni potpisi

(Detaljno objašnjeno u Nedelji 3)

```
Potpisivanje: sig = Sign(Kpriv, H(M))
Verifikacija: H(M) == Verify(Kpub, sig) ?
```

Zašto se heširá pre potpisivanja? RSA potpis je **spor** za velike podatke. Heš svodi poruku na fiksnu dužinu (npr. 256b) pa se potpisuje samo heš.

### 2. Commitment šema

Kriptografski mehanizam koji omogućava da se osoba **obaveže na izbor** bez da ga otkrije, a da posle ne može da ga promeni.

**Problem:** Bacanje novčića preko telefona.
- Alisa i Boban žele da bacaju novčić, ali nisu u istoj prostoriji
- Ko god baca može da laže o ishodu

**Rešenje:**
```
1. Alisa baca novčić, dobija ishod I (glava/pismo)
2. Alisa bira random salt S
3. Alisa šalje Bobanu: commitment = H(I || S)
   → Boban ne može iz heša da sazna I (jednosmernost)
   → Alisa ne može da promeni I jer bi se promenio heš (otpornost na kolizije)

4. Boban kaže šta se dešava u kom slučaju
   (npr. "glava = ti pereš sudove, pismo = ja perem")

5. Alisa otkriva: I i S
6. Boban proverava: H(I || S) == commitment ?
   Ako da → fer rezultat, niko nije varao
```

**Zašto salt?** Bez salta, Boban bi mogao da proba H("glava") i H("pismo") i sazna ishod pre otkrivanja.

### 3. HMAC (Hash-based Message Authentication Code)

Obezbeđuje **integritet** poruke i **autentičnost** pošiljaoca (ali ne i neporecivost — za razliku od digitalnog potpisa).

```
Svi koji imaju ključ K mogu:
  - da generišu HMAC za poruku
  - da verifikuju HMAC poruke
```

**Naivni pristup (pogrešan):** `MAC = H(K || M)`

**Problem:** Heš funkcije zasnovane na **Merkle-Damgård** konstrukciji (MD5, SHA-1, SHA-2) su ranjive na **length extension napad**:
- Napadač zna H(K || M) i dužinu K || M (ne zna K)
- Može da izračuna H(K || M || padding || M') za proizvoljni M'
- Dakle može da generiše validan MAC za novu (produženu) poruku **bez poznavanja ključa**!

**Ispravan HMAC:**
```
HMAC(K, M) = H((K ⊕ opad) || H((K ⊕ ipad) || M))

gde:
  ipad = 0x36 ponovljen dovoljno puta (do veličine bloka heš funkcije)
  opad = 0x5c ponovljen dovoljno puta
```

**Zašto ovo radi?**
- Unutrašnji heš: `H((K ⊕ ipad) || M)` — hešira poruku sa modifikovanim ključem
- Spoljašnji heš: `H((K ⊕ opad) || unutrašnji_heš)` — hešira rezultat sa drugačije modifikovanim ključem
- Dvostruko heširanje sa različitim padding-ima sprečava length extension napad

**HMAC vs digitalni potpis:**

| | HMAC | Digitalni potpis |
|---|---|---|
| Tip | Simetrični (deljeni ključ) | Asimetrični (javni/privatni) |
| Ko može generisati? | Svako ko ima ključ | Samo vlasnik privatnog ključa |
| Ko može verifikovati? | Svako ko ima ključ | Svako ko ima javni ključ |
| Neporecivost | ❌ | ✅ |
| Brzina | Brz | Sporiji |

### 4. AEAD (Authenticated Encryption with Associated Data)

Modernija zamena za HMAC + šifrovanje odvojeno. Šifrovanje i autentikacija u **jednom koraku**.

```
AEAD(K, nonce, plaintext, AAD) → (ciphertext, tag)

- plaintext: podatak koji se šifruje I autentifikuje
- AAD (Associated Data): podatak koji se NE šifruje ali SE autentifikuje
- tag: autentikacioni kod
```

**Analogija:** pismo u koverti
- Sadržaj koverte = plaintext (šifrovano, ne može se čitati)
- Adresa na koverti = AAD (mora biti čitljiva da pismo stigne, ali ne sme se menjati)

**Primer:** AES-GCM je najčešće korišćeni AEAD algoritam (TLS 1.3, SSH, IPsec).

### 5. Merkle stablo (Merkle Tree)

Hijerarhijska struktura zasnovana na heš funkcijama za **efikasnu verifikaciju integriteta** velikih skupova podataka.

```
                    ┌─────────────────────┐
                    │     Merkle Root      │
                    │   H(H12 || H34)      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
       ┌──────┴──────┐                   ┌──────┴──────┐
       │     H12     │                   │     H34     │
       │ H(H1 || H2) │                   │ H(H3 || H4) │
       └──────┬──────┘                   └──────┬──────┘
              │                                 │
        ┌─────┴─────┐                     ┌─────┴─────┐
        │           │                     │           │
    ┌───┴───┐ ┌─────┴───┐           ┌─────┴───┐ ┌────┴────┐
    │  H1   │ │   H2    │           │   H3    │ │   H4    │
    │H(Tx1) │ │ H(Tx2)  │           │ H(Tx3)  │ │ H(Tx4)  │
    └───────┘ └─────────┘           └─────────┘ └─────────┘
```

**Princip:**
- **Listovi:** heševi pojedinačnih podataka
- **Unutrašnji čvorovi:** heš konkatenacije svoje dece
- **Koren (Merkle Root):** heš koji predstavlja **sve** podatke u stablu

**Ključno svojstvo:** Promena **bilo kog** podatka u listu menja koren stabla.

**Efikasna verifikacija (Merkle proof):**
Da dokažeš da je Tx3 u skupu, treba ti samo: H4, H12 i Root.
```
Provera: H(H(H(Tx3) || H4) ...) == Root?

Složenost: O(log n) heševa umesto O(n)
```

**Primene:**
- **Git:** commit je heš korena stabla svih fajlova. Folder je čvor (sadrži heševe fajlova i podfoldera), fajl je list (heš sadržaja).
- **Blockchain:** svaki blok sadrži Merkle Root svih transakcija
- **Upoređivanje skupova:** efikasno naći šta se promenilo u velikom skupu fajlova

### 6. Verifikacija fajlova (Checksum)

```
1. Vlasnik objavi fajl + checksum:  sha256sum = a1b2c3d4...
2. Korisnik skine fajl
3. Korisnik izračuna: sha256sum skinutog_fajla
4. Uporedi sa objavljenim → ako se poklapaju, fajl je intaktan
```

```bash
# Računanje SHA-256 checksum-a
sha256sum fajl.iso

# Verifikacija
sha256sum -c checksums.txt
```

### 7. Decentralizovane heš mape (DHT) — informativno

Distribuirana struktura podataka bez centralnog servera.

```
1. Ključ podatka se hešira → id
2. id određuje čvor/grupu čvorova zaduženuh za taj podatak
3. Tom čvoru se šalju upiti ili izmene
```

**Primena — BitTorrent (uprošćeno):**
```
1. Pitam DHT mrežu: "Ko ima info o peer-ovima za fajl X?"
2. DHT vrati čvor koji zna
3. Taj čvor mi da IP adrese peer-ova
4. Počinjem skidanje fajla od peer-ova
```

---

## KDF (Key Derivation Function)

Funkcija koja od **slabe lozinke** (ili zajedničke DH tajne) pravi **jak kriptografski ključ**.

### Zašto je potrebna?

- Korisničke lozinke su kratke i predvidive → loš materijal za ključ
- DH zajednička tajna g^(ab) mod p nije uniformno raspodeljena → neki bitovi su verovatniji
- Kriptografski ključ mora biti: nepredvidiv, dovoljno dug, uniformno raspodeljen

### Kako radi (uprošćeno)

```
Ulaz: lozinka, salt (random), parametri (broj iteracija, memorija)
Izlaz: jak ključ fiksne dužine

Najprostiji pristup:
  ključ = H(H(H(...H(lozinka || salt)...)))   ← n puta heširanje

U bazi se čuva: salt, n, algoritam, (rezultat)
```

### Šta se dobija korišćenjem KDF

| Svojstvo | Objašnjenje |
|---|---|
| **Sporost** | Probanje jedne lozinke traje duže → brute-force je skuplji |
| **Jedinstvenost** | Salt obezbeđuje da ista lozinka + različit salt → potpuno različit izlaz |
| **Memorijska zahtevnost** | Neke KDF zahtevaju puno memorije → teška paralelizacija na GPU/ASIC |
| **Login je brz** | Jedna provera traje npr. 100ms — prihvatljivo za korisnika |
| **Masovni napad je skup** | Milion pokušaja × 100ms = ~28 sati za jednog korisnika |

### Poznate KDF funkcije

| KDF | Karakteristike |
|---|---|
| **PBKDF2** | Iterativno heširanje. Parametar: broj iteracija. Jednostavan, ali paralelizabilan na GPU. |
| **bcrypt** | Zasnovan na Blowfish šifri. Otporniji na GPU napade. |
| **scrypt** | Memorijski zahtevan → otežava ASIC/GPU napade. |
| **Argon2** | Pobednik Password Hashing Competition (2015). Konfigurabilan CPU + memorija + paralelizam. Preporučen danas. |

### KDF u kontekstu lozinki (čuvanje u bazi)

```
Registracija:
  salt = random()
  hash = KDF(lozinka, salt, parametri)
  čuvaj u bazi: (korisnik, salt, parametri, hash)

Login:
  hash' = KDF(uneta_lozinka, salt_iz_baze, parametri)
  hash' == hash_iz_baze ? → pristup odobren
```

**Zašto salt?** Bez salta, iste lozinke daju isti heš → napadač može koristiti rainbow tabele (unapred izračunate heševe za česte lozinke).

---

*Kraj materijala za kolokvijum. Srećno! 🎯*
