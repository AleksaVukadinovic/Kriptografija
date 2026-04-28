# 1. Uvod

**Kriptografija** je nauka koja nam omogucava da osiguramo tajnost, integritet i autenticnost. Sprecava neovlasceno citanje i promene i omogucava nam da znamo identitet autora.

Neki osnovni pojmovi koji ce nam trebati da bi dalje mogli da pratimo kurs (ostali ce biti uvedeni usputno):
- **OT (Otvoreni tekst)** je poruka koji treba poslati npr. “ZDRAVO”
- **ST (Šifrat)** je sifrovana poruka npr. “XQABER”
- **Sifrovanje** je transformacija otvorenog teksta u sifrat
- **Desifrovanje** je transformacija sifrata u otvoreni tekst
- **Kodiranje** transformise otvoreni tekst u niz cifara ili bita. Npr. velika slova abecede mogu da se kodiraju sa A -> 0, B -> 1, …, Z -> 25 (ZDRAVO -> 25 3 17 0 21 14) ili npr. ASCII kod (A -> 01000001, B -> 01000010, …)
- **Dekodiranje** je obrnuta transformacija kodiranju, transformise niz cifara ili bita u polazni tekst.

## Cezarova i Viženerova sifra<!-- {"fold":true} -->

Ljudi su jos davno uvideli potrebu za sifrovanjem (motivisani cuvanjem i prenosenjem tajni u ratu). Jedan od najpoznatijih primera sifrovanja je **Cezarova sifra**. Ona je sifra zamene, koja svako slovo zamenjuje trecim slovom udesno (duz abecede) od njega. Ako se radi o engleskoj abecedi onda A -> D, B -> E, …, Z -> C.

Ovo se moze uopstiti. Ako je moguce pomeranje u abecedi za proizvoljan broj pozicija tada se radi o **monoalfabetskoj cifri translacije** i tada je Cezarova sifra samo specijalni slucaj ovog sistema. Najpoznatiji primer ovog sistema je **Viznerova sifra (Vigener)** koji kaze ovako neka je kljuc neka rec npr. TIN, slovo T je 19-to u abecedi, I je sedmo, a N 13-to. Tada se sifrovanje obavlja translacijom prvog slova za 19, drugog za 7, treceg za 13, cetvrtog za 19 itd. Ovakva sifra je primer troalfabetne sifre translacije. Pre nego sto su postojali racunari, ljudi su koristili Vizinerov kvadrat (slika ispod). Da bi se sifrovala rec CRYPTO kljucem TIN, najpre se sifruje slovo C slovom T. U kvadratu se procita slovo na preseku vrste C i kolone T (ili obrnuto). Rezultat sifrovanja je VZLIBB. Primerimo da se slobo B dva puta pojavljuje u sifratu. Ako primalac ima isti kljuc, onda on moze da napravi istu tabelu i desifrovanje postaje jako lako.
![](image.png)

## Simetrična kriptografija

**Simetrična kriptografija** (poznata i kao kriptografija sa privatnim ključem) predstavlja najstariji i najbrži oblik enkripcije. Njena glavna karakteristika je da se **isti ključ** koristi i za zaključavanje (enkripciju) i za otključavanje (dekripciju) podataka.

Intuitivno mozemo zamisliti to kao da hocemo da ostavimo nekome poverljiv dokument u sef da ga on pokupi. Kad ga ostavimo, zakljucavao ga, da bi osoba kojoj je dokument namenjen mogla da mu pristupi potreno je da ima isti kljuc, kako bi mogla da otkljuca sef.

Formalnije receno, ako je P originalni text (plaintext), K tajni kljuc, E funkcija enkripcije tada se sifrovan tekst C dobija kao: $C = E(K, P)$, Dekripcija se vrsi primenom inverzne funkcije D uz pomoc istog kljuca: $P = D(K, C)$.

Simetrični sistemi se dele na dve glavne kategorije u zavisnosti od toga kako obrađuju podatke:
- **Blok šifre (Block Ciphers)** - Podaci se dele na blokove fiksne veličine (npr. 64 ili 128 bita). Svaki blok se šifruje zasebno.
  - **AES (Advanced Encryption Standard):** Trenutni standard. Koristi blokove od 128 bita i ključeve od 128, 192 ili 256 bita. Izuzetno je siguran i hardverski optimizovan.
  * **DES i 3DES:** Stariji standardi. DES je danas nesiguran zbog kratkog ključa (56 bita), dok se 3DES polako povlači iz upotrebe.
- **Protočne šifre (Stream Ciphers)** - Podaci se šifruju bit po bit ili bajt po bajt u neprekidnom nizu. Obično su brže od blok šifri i koriste se tamo gde je bitna nisko kasnjenje.
  * **ChaCha20:** Moderan i veoma brz algoritam, često se koristi u mobilnim uređajima i TLS protokolu.
  * **RC4:** Nekada popularan, ali danas se smatra nesigurnim.

| **Prednosti** | **Mane** |
|---|---|
| **Brzina:** Ekstremno brzi algoritmi, pogodni za velike količine podataka. | **Distribucija ključa:** Najveći problem – kako bezbedno poslati ključ drugoj strani a da ga niko ne presretne? |
| **Mala procesorska snaga:** Idealni za IoT uređaje i mobilne telefone. | **Skalabilnost:** Ako 100 ljudi treba da komunicira međusobno, svakom paru je potreban unikatan ključ, što vodi do ogromnog broja ključeva ($n(n-1)/2$). |
| **Efikasnost:** Šifrovani podaci obično ne zauzimaju više prostora od originalnih. | **Nema neporecivosti:** Pošto obe strane imaju isti ključ, ne može se dokazati ko je tačno kreirao poruku. |

## Protočna šifra

**Protočne šifre** šifruju podatke **bit po bit** ili bajt po bajt. One kombinuju izvorni tekst sa neprekidnim nizom bitova koji se naziva **keystream**. **Princip rada:** Koristi se logička operacija **XOR** ($\oplus$). Ako je P bit teksta, a K bit ključa, šifrat je $C = P \oplus K$. Prednost ovog pristupa je velika brzina i malo kasnjenje (za razliku od blok sifre ovde nema cekanja da se sledeci blok obradi). Problem je cinjenica da se kljucni niz nikada ne sme ponoviti sa istim kljucem (u suportnom postoji opasnost od Two-Time Pad napada).

Pošto je nemoguće razmeniti beskonačno dugačak nasumični ključ, koristimo **PRNG** (**Pseudo Random Number Generator**). On uzima kratak, tajni kljuc koji se naziva seme (**seed**) i pomocu matematickog algoritma generise ogroman, naizgled nasumican niz bitova (**keystream**). U savremenim sistemima se često koriste **linearni pomerački registri (LFSR)** čije su orbite i karakteristični polinomi ključni za stabilnost šifre.

## Blokovske sifre

Ovi sistemi obrađuju fiksne grupe bita (blokove) koristeći složene matematičke transformacije unutar konačnih polja. Imamo dve vrste standarda blokovskog sifrovanja:
- **DES (Data Encryption Standard)** - Klasicna blokovska sifra sa blokom od 64 bita i kljucem od 56 bita. Koristi Feistelovu mrezu, ali se danas smatra prevazidjenom zbog male duzine kljuca.
- **AES (Advanced Encryption Standard)** - Savremeni standard, postoje cetiri uobicajena nacina rada AES-a. Posto AES sifruje blokove podataka od 128 bita, ovi modovi definisu kako cemo sifrovati dugacku poruku koja se sastoji od mnogo takvih blokova:
  - Najjednostavniji i najnesigurniji nacin rada je **ECB** (**electronic code book**). Svaki blok otvorenog teksta se sifruje potpuno nezavisno od ostalih, koristeci isti kljuc. Problem sa ovim pristupom je ako u poruci imamo dva identicna bloka podataka, dobijamo dva identicna bloka sifrata - ovo otkriva obrasce u podacima.
  - Drugi i najecesci nacin rada je **CBC** (**cipher block chaining**). Za razliku od EBC-a ovde se uzodi zavisnost izmedju blokova kako bi se sakrili podaci. Pre nego sto se blok otvorenog teksta sifruje, on se XOR-uje sa sifratom prethodnog bloka. Za prvi blok se koristi poseban, unapred odabran, ne-tahni broj koji se naziva **IV (inicijalni vektor)**. Stavise IV se salje pre svake poruke.
