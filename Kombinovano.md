# Nedelja 1: Uvod u kriptografiju<!-- {"fold":true} -->

## Uvod

**Kriptografija** je nauka koja nam omogucava da osiguramo tajnost, integritet i autenticnost pri komunikaciji. Sprecava neovlasceno citanje i promene podataka i omgucava nam da znamo identitet autora.
1\. **Tajnost (Confidentiality)** — niko neovlašćen ne može da pročita poruku
2\. **Integritet (Integrity)** — poruka nije menjana tokom prenosa
3\. **Autentičnost (Authenticity)** — znamo ko je autor poruke

Neki osnovni pojmovi koji ce nam trebati da bi dalje mogli da pratimo kurs (ostali ce biti uvedeni usputno):
- **OT (Otvoreni tekst)** je poruka koji treba poslati npr. “ZDRAVO”
- **ST (Šifrat)** je sifrovana poruka npr. “XQABER”
- **Sifrovanje** je transformacija otvorenog teksta u sifrat - `C = E(K, M)`, gde je M poruka, K kljuc, a C sifrat
- **Desifrovanje** je inverzna operacija sifrovanju, transformise sifrat u otvoreni tekst, vazi `M = D(K, C)` i `D(K, E(K, M)) = M`
- **Kodiranje** transformise otvoreni tekst u niz cifara ili bita. Npr. velika slova abecede mogu da se kodiraju sa A -> 0, B -> 1, …, Z -> 25 (ZDRAVO -> 25 3 17 0 21 14) ili npr. ASCII kod (A -> 01000001, B -> 01000010, …)
- **Dekodiranje** je obrnuta transformacija kodiranju, transformise niz cifara ili bita u polazni tekst.

Vecina bezbednosti u kriptografiji se oslanja na svojstva velikih brojeva. Cak i ako postoje (relativno) efikasni algoritmi za razbijanje vecine bezbednosih sistema oni u praksi nisu izvoljivi zbog same velicine brojeva u pitanju. Pogledajmo par primera da steknemo osecaj zašto su neki napadi nepraktični:
* Broj kombinacija za loto (6 od 45): oko 8 miliona ≈ 2²³
* Rastojanje Beograd–Atina u milimetrima: ~600 km = 6×10⁸ ≈ 2³⁰
* Molekuli vazduha u prostoriji: ~10²⁷ ≈ 2⁹⁰
* AES-128 ključ: 2¹²⁸ ≈ 3.4 × 10³⁸ mogućih ključeva
* Računar koji proba 10⁹ ključeva/sec treba ~10²² godina za brute-force AES-128

Poenta: ako je prostor ključeva dovoljno veliki (≥ 2¹²⁸), brute-force napad je nemoguć sa trenutnom tehnologijom.

## Cezarova i Viženerova sifra

Ljudi su jos davno uvideli potrebu za sifrovanjem (motivisani cuvanjem i prenosenjem tajni u ratu). Jedan od najpoznatijih primera sifrovanja je **Cezarova sifra**. Ona je sifra zamene, koja svako slovo zamenjuje trecim slovom udesno (duz abecede) od njega. Ako se radi o engleskoj abecedi onda A -> D, B -> E, …, Z -> C.

### Cezarova šifra<!-- {"fold":true} -->

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

Kriptoanaliza Cezarove šifre:
1\. **Brute force:** Probaj svih 26 ključeva, pogledaj koji daje smisleni tekst.
2\. **Frekventna analiza:** U engleskom jeziku slovo 'E' je najčešće (~12.7%). Nađi najčešće slovo u šifratu → pomeranje od 'E' do tog slova je verovatno ključ.

### Vizenerova sifra

Ovo se moze uopstiti. Ako je moguce pomeranje u abecedi za proizvoljan broj pozicija tada se radi o **monoalfabetskoj cifri translacije** i tada je Cezarova sifra samo specijalni slucaj ovog sistema. Najpoznatiji primer ovog sistema je **Viznerova sifra (Vigener)**.

Vigener je Proširenje Cezarove šifre — koristi se ključ-reč umesto jednog broja. Svako slovo poruke se šifruje drugim pomeranjem.

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

### One-Time Pad

**Jednokratna sifra (One-time pad)** je sifra koja je teorijski neprobojna ako se koristi na pravilan nacin. Kljuc je niz bitova koji je jednako dug kao i poruka. Enkripcija se vrsi tako sto se poruka kombinuje sa kljucem pomocu XOR-a.
E(k, m) = k XOR m, D(k, c) = k XOR c.

Kako bi sifra zaista bila neprobojna, kljuc mora biti slucajno generisan, iste duzine kao i poruka, koriscen samo jednom i cuvan u tajnosti. Ako bar jedan od ovih uslova nije ispunjen, sifra postaje podlozna napadima

## Kerckhoffsov princip<!-- {"fold":true} -->

> Bezbednost šifarskog sistema mora da zavisi **isključivo od tajnosti ključa**, a ne od tajnosti algoritma.

Ovo znači: pretpostavlja se da napadač zna potpuno kako algoritam radi. Jedina tajna je ključ. Svi moderni kriptografski sistemi poštuju ovaj princip — AES, RSA, itd. su javno poznati algoritmi.

## Simetricni i Asimetricni kriptografski sistemi
### Simetricna kriptografija, blokovske i protocne sifre
**Simetrična kriptografija** (poznata i kao kriptografija sa privatnim ključem) predstavlja najstariji i najbrži oblik enkripcije. Njena glavna karakteristika je da se isti ključ koristi i za zaključavanje (enkripciju) i za otključavanje (dekripciju) podataka.

Formalnije receno, ako je P originalni text (plaintext), K tajni kljuc, E funkcija enkripcije tada se sifrovan tekst C dobija kao: $C = E(K, P)$, Dekripcija se vrsi primenom inverzne funkcije D uz pomoc istog kljuca: $P = D(K, C)$.

Simetrični sistemi se dele na dve glavne kategorije u zavisnosti od toga kako obrađuju podatke:
- **Blok šifre (Block Ciphers)** - Podaci se dele na blokove fiksne veličine (npr. 64 ili 128 bita). Svaki blok se šifruje zasebno.
    - **AES (Advanced Encryption Standard):** Trenutni standard. Koristi blokove od 128 bita i ključeve od 128, 192 ili 256 bita. Izuzetno je siguran i hardverski optimizovan.
    * **DES i 3DES:** Stariji standardi. DES je danas nesiguran zbog kratkog ključa (56 bita), dok se 3DES polako povlači iz upotrebe.
- **Protočne šifre (Stream Ciphers)** - Podaci se šifruju bit po bit ili bajt po bajt u neprekidnom nizu. Obično su brže od blok šifri i koriste se tamo gde je bitno nisko kasnjenje.
    * **ChaCha20:** Moderan i veoma brz algoritam, često se koristi u mobilnim uređajima i TLS protokolu.
    * **RC4:** Nekada popularan, ali danas se smatra nesigurnim.

| **Prednosti**                                                | **Mane**                                                     |
|--------------------------------------------------------------|--------------------------------------------------------------|
| **Brzina:** Ekstremno brzi algoritmi, pogodni za velike količine podataka. | **Distribucija ključa:** Najveći problem – kako bezbedno poslati ključ drugoj strani a da ga niko ne presretne? |
| **Mala procesorska snaga:** Idealni za IoT uređaje i mobilne telefone. | **Skalabilnost:** Ako 100 ljudi treba da komunicira međusobno, svakom paru je potreban unikatan ključ, što vodi do ogromnog broja ključeva - n(n-1)/2. |
| **Efikasnost:** Šifrovani podaci obično ne zauzimaju više prostora od originalnih. | **Nema neporecivosti:** Pošto obe strane imaju isti ključ, ne može se dokazati ko je tačno kreirao poruku. |

#### Protocne i blokovske sifre

**Protočne šifre** šifruju podatke **bit po bit** ili bajt po bajt. One kombinuju izvorni tekst sa neprekidnim nizom bitova koji se naziva **keystream**. **Princip rada:** Koristi se logička operacija **XOR** ($\oplus$). Ako je P bit teksta, a K bit ključa, šifrat je $C = P \oplus K$. Prednost ovog pristupa je velika brzina i malo kasnjenje (za razliku od blok sifre ovde nema cekanja da se sledeci blok obradi). Problem je cinjenica da se kljucni niz nikada ne sme ponoviti sa istim kljucem (u suportnom postoji opasnost od Two-Time Pad napada).

Pošto je nemoguće razmeniti beskonačno dugačak nasumični ključ, koristimo **PRNG** (**Pseudo Random Number Generator**). On uzima kratak, tajni kljuc koji se naziva seme (**seed**) i pomocu matematickog algoritma generise ogroman, naizgled nasumican niz bitova (**keystream**).

**Blokovski** sistemi obrađuju fiksne grupe bita (blokove) koristeći složene matematičke transformacije unutar konačnih polja. Imamo dve vrste standarda blokovskog sifrovanja:
- **DES (Data Encryption Standard)** - Klasicna blokovska sifra sa blokom od 64 bita i kljucem od 56 bita. Koristi Feistelovu mrezu, ali se danas smatra prevazidjenom zbog male duzine kljuca.
- **AES (Advanced Encryption Standard)** - Savremeni standard, postoje cetiri uobicajena nacina rada AES-a. Posto AES sifruje blokove podataka od 128 bita, ovi modovi definisu kako cemo sifrovati dugacku poruku koja se sastoji od mnogo takvih blokova:
    - Najjednostavniji i najnesigurniji nacin rada je **ECB** (**electronic code book**). Svaki blok otvorenog teksta se sifruje potpuno nezavisno od ostalih, koristeci isti kljuc. Problem sa ovim pristupom je ako u poruci imamo dva identicna bloka podataka, dobijamo dva identicna bloka sifrata - ovo otkriva obrasce u podacima.
    - Drugi i najecesci nacin rada je **CBC** (**cipher block chaining**). Za razliku od EBC-a ovde se uzodi zavisnost izmedju blokova kako bi se sakrili podaci. Pre nego sto se blok otvorenog teksta sifruje, on se XOR-uje sa sifratom prethodnog bloka. Za prvi blok se koristi poseban, unapred odabran, ne-tahni broj koji se naziva **IV (inicijalni vektor)**. Stavise IV se salje pre svake poruke.

### Asimetricna kriptografija<!-- {"fold":true} -->

U simetričnim sistemima (poput AES-a), pošiljalac i primalac moraju imati isti tajni ključ. Ako taj ključ neko presretne tokom razmene, cela komunikacija je kompromitovana. **Asimetrična kriptografija** ovo rešava korišćenjem para ključeva.
Svaki korisnik u sistemu generise par matematicki povezanih kljuceva:
* **Javni kljuc (Public Key)**: Moze se slobodno deliti sa bilo kim. Sluzi za siforvanje podataka ili proveru digitalnog potpisa.
* **Privatni kljuc (Private Key)**: Cuva se u strogoj tajnosti. Sluzi za desifrovanje podataka ili kreiranje digitalnog potpisa.

Kljucevi funkcionisu po principu - ono sto jedan kljuc zakljuca, samo onaj drugi iz istog para moze da otkljuca. Nemoguce je u razumnom vremenu izracunati privatan kljuc na osnovu poznavanja javnog kljuca.
Ako osoba A (pošiljalac) želi da pošalje tajnu poruku osobi B (primalac):
1. Osoba A uzima javni ključ osobe B.
2. Osoba A šifruje poruku tim javnim ključem.
3. Sada tu poruku može da dešifruje isključivo osoba B, jer samo ona poseduje odgovarajući privatni ključ.

Najpoznatiji primeri su RSA, ECC i Diffie-Hellmann. Najveca prednost asimetricnog sifrovanja je to sto nema potrebe za razmenom poverljivih kljuceva. Ovo dolazi po cenu brzinu jer su ovi algoritmi mnogo sporiji i cesto se desava da je sam sifrat veci od poruke. U praksi se cesto koriste hibridni pristupi, gde se asimetricna kriptografija koristi samo na pocetku za uspostavljanje tajnog kljuca.

## Heširanje

**Heširanje** je proces transformacije ulaznih podataka bilo koje velicine u izlaz fiskne duzine, koji se naziva **heš vrednost** koriscenjem neke funkcije za heširanje. Za razliku od enrkipcije, heširanje je **jednosmerna funkcija** tj. dizajniraju se tako da bude nemoguce vratiti heš u originalne podatke. Sluze nam da obezbedimo da poruku koju smo primili neko usput nije izmenio, osobina poruke da nije dozivela izmene je **integritet**. Svaka heš funkcija treba da ima sledeća svojstva:
- Potrebno je da se njene vrednosti lako i brzo izracunavaju
- Heš funkcija treba da bude jednosmerna funkcija ( za zadato y potrebno je da bude jako tesko ili nemoguce oredjivanje x takvog da $H(x) = y$)
- Za zadato x potrebno je da bude jako tesko odredjivanje drugog x’ t.d. $H(x’) = H(x)$. Ova osobina se naziva **osnovna otpornost na koliziju**

Ako je pored toga ispunjen zahtev da je tesko pronaci bilo koji par x, x’ takav da je $H(x) = H(x')$, onda se za H kaze da ima **jaku otpornost za koliziju**.

Da se napravi algoritam za heširanje obicno se polazi of funkcije $f$ koja blokove od $m+t$ bita preslikava u blokove od t bita, gde su m i t veliki, a $f$ ima sve tri navedene osobine. Ulaz ovog algoritma je poruka, a izlaz njena heš vrednost.

Funkcija $f$ moze se iskoristiti za dobijanje heš funkcije. Pretpostavimo da je poruka razbijena u m-bitne blokove $M_1, M_2, …, M_k$. Ako duzina poruke nije deljiva sa m, onda se poslednji blok dopunjuje do duzine m. Zadat je unapred dogovoren blok od t bita (inicijalizovani vektor IV).

# Nedelja 2: Difi-Helman, Stepenovanje kvadriranjem, problem diskretnog logaritma, blokovske sifre<!-- {"fold":true} -->

## Difi-Helmanova razmena (usaglasavanje) kljuca<!-- {"fold":true} -->

Ovde koristimo konacno polje $F_q$ i jedan element $g \in F_q$. Najbolje je da g bude generator multiplikativne grupe $F^*_q$  ( = $F_q$ \\ {0}), a prihvatljivo je i da bude element velikog reda. **Difi-Helmanova razmena kljuca** se zasvina na sledecem:
- Ako znamo $g \in F^*_q$ i $n \in N$ lako je odrediti $g^n$
- Ako znamo g i $g^n$ tesko je odrediti n

Algoritam:
1. Primalac i Posiljalac biraju stepen prostog broja $q = p^d$ (priblizno 200-cifren) i generator $g \in F^*_q$ i objavljuju q i g
2. Posiljalac bira svoj tajni kljuc $a_A \in N$, racuna i objavljuje samo $g^a_A$ (tj. javni kljuc)
3. Slicno, primalac bira tajni kljuc $a_B \in N$, racuna i objavljuje samo $g^a_B$ (javni kljuc)
4. Posiljac i primalac oba mogu da izracunaju $K = (g^a_A)^a_B = (g^a_B)^a_A$ i to predstavlja njihov usaglasen javni kljuc
5. Prisluskivac zna samo $q, g, g^a_A$ i $g^a_B$ i pomocu toga ne moze u razumnom vremenu odrediti K

Da bi mogli brzo da izracunamo $g^n \in F^*_q$ koristimo algoritam **stepenovanja ponovljenim kvadriranjem**.

## Stepenovanje kvadriranjem i slozenost<!-- {"fold":true} -->

Algoritam **stepenovanja ponovljenim kvadriranjem** je sledeci:
1. Redukovati stepen na n < q-1 zbog cinjenice da je g^q-1 = 1 na osnovu *male Fermaove teoreme*
2. Zapisati n binarno (kao sumu stepena 2^i, gde je i in {0, 1, 2, …, r})
3. Izracunati 1, g, g^2, (g^2)^2, (g^2^2)^2, …, g^2r (svaki je kvadrat prethodnog)
4. g^n je proizvod onih g^2^i za koje je n_i = 1

U slucaju q = p prost slozenost ovog algoritma je O(r(logp)^2) = O((logp)^3), dok g^n = g\*g\*g…*g bi trebalo O(n(logp)^2) operacija. Takodje na osnovu Male Fermaove Teoreme moze se izracunati da je slozenost O((logq)^4)

## Problem diskretnog logaritma u konacnom polju<!-- {"fold":true} -->

Def. Neka je G grupa (npr $F^*_q$) i neka su $a, g \in G.$ Najmanji prirodan broj n (ako postoji) takav da je $a = g^n$ zovemo **diskretni logaritam** od a u osnovi g i oznacavamo sa $\log_g(a)$.

Problem: Nemamo formulu da izracunavanje $n = \log_g(a) \in F^*_q$, sto znaci da ne postoji dovoljno brz algoritam koji resava problem diskretnog logaritma u $F^*_q$ tj. algoritam cija je brzina uporediva sa stepenovanjem, obicna pretraga je slozenosti O(q), ali postoje optimizacije koje mogu spusititi ovu slozenost na O(sqrt(q)(logp)^2), sto u svakom slucaju nije dovoljno brzo.

## Blokovske sifre i AES

**Problem**: Ana i Boban zele da komuniciraju poverljivo putem nebezbednog javnog kanala (npr preko WiFi). Eva koja kontrolise kanal moze da prisluskuje komunikaciju, ali i da menja sadrzaj svake poruke. Na koji nacin Ana i Boban mogu da ostvare poverljivu komunikaciju i da pritom otkriju ukoliko je poruka bila izmenjena?

Blok šifre su osnovne kriptografske primitive nad kojima je izgrađena većina modernih šifarskih sistema. Osim što nude rešenje za problem poverljive komunikacije, takođe omogućavaju konstrukciju takozvane autentifikovane enkripcije.

Formalno, blok sifra je sifra (E, D) pri cemu je velicina poruke samim tim i sifrata fiksirana na n bitova. Kazemo da je n velicina bloka. Naglasimo da se, zbog tog uslova, blok sifrom ne mogu direktno sifrovati proizvoljne poruke. Za fiksiran kljuc k, funkcija E_k(m) = E(k, m) je permutacija skupa svih bitovskih niski duzine n. Cilj prilikom dizajniranja blok sifre je da se fja E_k ponasa kao random permuracija za svaki kljuc k.

Uopsteno, blok sifre se konstruisu iterativnom primenom neke jednostavne invertibilne transformacije koja zavisi od kljuca, pri cemu se jedna iteracija naziva runda, a transformacija se naziva funkcija runde. Kljuc k se prosiruje u niz podkljuceva k1, ..., kr (po jedan za svaku rundu) pomocu PGR.

Blokovska šifra je tip simetričnog sistema koji podatke obrađuje u **blokovima** fiksne dužine. Dok protočne šifre rade bit-po-bit, blokovske šifre grupišu simbole (npr. 128 bita kod AES-a) i transformišu ih odjednom. **AES (Advanced Encryption Standard)** je postao standard 2001. godine kao naslednik starijeg DES-a, nudeći veću sigurnost kroz duže ključeve (128, 192 ili 256 bita).

### Uprošćeni AES (SAES)
**SAES** je edukativni model koji koristi 16-bitne blokove i 16-bitni ključ kako bi se lakše razumela struktura pravog AES-a. Koristi **tabelu S** (tzv. **S-box**), cija struktura se opisuje koriscenjem konacnog polja F_16 = F_2[x]/(x^4 + x + 1) od 16 elemenata. Rec. **nibl** oznacava cetvorku bita npr. 1011. Niblu b_0b_1b_2b_3 moze se pridruziti elemenat b_0x^3 + b1x^2 + b2x + b3 polja F_16.

**Tabela S** je bijektivno preslikavanje S: {0, 1}^4 -> {0, 1}^4 niblova u niblove. Ova funkcija je kompozicija dva preslikavanja.
1. Prvo preslikavanje je inverzija nibla u F_16, npr. inverz polinoma x + 1 je polinom x^3 + x^2 + x, pa komponenta preslikavanja S preslikava 0011 u 1110. Nibl 0000 je izuzetak, on se slika sam u sebe. Tako dobijenom niblu N se pridruzuje elemenat N(y) = b_0y^3 + b1y^2 + b2y + b3.
2. Druga komponenta preslikavanja S je transformacija nibla N(y) u nibl a(y)N(y) + b(y). Tako se npr. nibl 1110 preslikava u nibl 1011. Prema tome S(0011) = 1011.

Algoritam SAES ima 16-bitni kljuc k_0k_1…k_15. Od njega se formira niz od 48 bita (tri 16-bitna **potkljuca**; od tih 48 bita prvih 16 jednaki su originalnom kljucu). Ovo prosirivanje sa 16 na 48 bita naziva se **prosirivanje kljuca**. Proces koristi funkcije **RotByte** (rotacija bajtova), **SubByte** (zamena preko S-tabele) i dodavanje konstanti **RCON** koje služe da se razbiju pravilnosti i sličnosti između podključeva.

Algoritam se sastoji od početnog koraka i dve runde transformacija,. Operacije unutar rundi su:
* **AddRoundKey (AK):** Sabiranje stanja (podataka) sa potključem runde pomoću bitovne XOR operacije.
* **Nibble Substitution (NS):** Nelinearna zamena svakog nibla vrednošću iz **S-tabele** kako bi se postigla konfuzija,.
* **ShiftRow (SR):** Cikličko pomeranje (zamena mesta) niblova u drugoj vrsti matrice stanja.
* **MixColumn (MC):** Množenje kolona matrice stanja fiksnim polinomom radi postizanja **difuzije** (širenja uticaja jednog bita na ostatak bloka),

**Dešifrovanje** se vrši primenom **inverznih operacija** u obrnutom redosledu. Pošto su operacije poput AddRoundKey i ShiftRow (u SAES verziji) same sebi inverzne ili se lako invertuju, proces je veoma sličan šifrovanju. Zahvaljujući izostavljanju MixColumn-a u poslednjoj rundi šifrovanja, moguće je organizovati dešifrovanje tako da ima identičnu strukturu koraka, što olakšava hardversku implementaciju.

# Nedelja 3: Hesiranje
## RC4

**RC4** je svojevremeno bila jedna od najpopularnijih **protočnih šifara**. Autor ovog algoritma je Ronald Rivest (poznat i kao slovo R u RSA sistemu), a konstruisan je 1987. godine.

Najpre se bira prirodni broj n (obicno se koristi n=8). Osnovna komponenta generatora je promenljiva tabela S duzine 2^n, ciji je sadrzaj u svakom trenutku neka permutacija brojeva i=0, 1, …, 2^n-1. U fazi pripreme generatora se na osnovu lkjuca izracunava pocetni sadrzaj niza S tj. neka permutacija skupa {0, 1, … 2^n-1}. Izracunavanje pocinje tako sto se stavi S_i za i \in {0, 1, …, 2^n-1}. Zatim se od kljuca formira drugi niz K_0, K_1, …, K_2^n-1 od 2^n n-torki bita.

```python
# priprema generatora
j = 0
for j in range(0, 2^n):
	j = (j + S_i + K_i) % 2^n
	swap(S_i, S_j)

# generisanje blokova niza kljuca
i = 0, j = 0
for r in range(0, l)
	i = (i + 1) % 2^n
	j = (j + S_i) % 2^n
	swap(S_i, S_j)
	t = S_i + S_j
	KS_r = S_t # naredna n-torka bita izlaznog niza kljuca
```

## Heširanje

**Heširanje** je proces transformacije ulaznih podataka bilo koje velicine u izlaz fiskne duzine, koji se naziva **heš vrednost** koriscenjem neke funkcije za heširanje. Za razliku od enrkipcije, heširanje je **jednosmerna funkcija** tj. dizajniraju se tako da bude nemoguce vratiti heš u originalne podatke. Sluze nam da obezbedimo da poruku koju smo primili neko usput nije izmenio, osobina poruke da nije dozivela izmene je **integritet**. Svaka heš funkcija treba da ima sledeća svojstva:
- Potrebno je da se njene vrednosti lako i brzo izracunavaju
- Heš funkcija treba da bude jednosmerna funkcija ( za zadato y potrebno je da bude jako tesko ili nemoguce oredjivanje x takvog da $H(x) = y$)
- Za zadato x potrebno je da bude jako tesko odredjivanje drugog x’ t.d. $H(x’) = H(x)$. Ova osobina se naziva **osnovna otpornost na koliziju**

Ako je pored toga ispunjen zahtev da je tesko pronaci bilo koji par x, x’ takav da je $H(x) = H(x')$, onda se za H kaze da ima **jaku otpornost za koliziju**.

Da se napravi algoritam za heširanje obicno se polazi of funkcije $f$ koja blokove od $m+t$ bita preslikava u blokove od t bita, gde su m i t veliki, a $f$ ima sve tri navedene osobine. Ulaz ovog algoritma je poruka, a izlaz njena heš vrednost.

Funkcija $f$ moze se iskoristiti za dobijanje heš funkcije. Pretpostavimo da je poruka razbijena u m-bitne blokove $M_1, M_2, …, M_k$. Ako duzina poruke nije deljiva sa m, onda se poslednji blok dopunjuje do duzine m. Zadat je unapred dogovoren blok od t bita (inicijalizovani vektor IV).

### MD5

Jedan od najpopularnijih hes algoritama je MD5. On je efikasniji od malo pre opisanog algoritma koji koristi AES. On se zasniva na funkciji f koja preslikava blok od 512 bita u blok od 128 bita. Neka je M blok od 512 bita. U ovom kontekstu zvacemo blok od 32 bita rec, dakle M se sastoji od 16 reci - X[0], X[1], …, X[15].

Tokom izvrsavanja stalno se azuriraju stanja cetiri 32-bitna registara. Na pocetku je A = A_0, B = B_0, C = C_0, D = D_0. Definisemo cetiri funkcije:
- F(X, Y, Z) = XY ∨ !XZ
- G(X, Y, Z) = XZ ∨ Y!Z
- H(X, Y, Z) = X ⊕ Y ⊕ Z
- I(X, Y, Z) = Y ⊕ (X ∨ !Z)

Postoje i 64 konstante T[1], …, T[64]. Neka je i broj radijana, tada je |sin(i)| realni broj izmedju 0 i 1 i T[i] je prvih 32 bita posle decimalne tacke.

Sam algoritam radi tako sto se u unutar petlje, jedan od 4 registara (tj. vrednost unutar njega, uzmimo da je to ovde A) azurira na sledeci nacin:
1. **Nelinearna transformacija**: Primenjuje se neka od funkcija F, G, H na preostale vrednost (B, C, D)
2. **Modularno sabiranje**: Rezultat funkcije se sabira sa promenljivom koja se azurira (A), jednim podblokom poruke i nekom konstantom iz tabele
3. **Ciklicno pomeranje (<<)**: Dobijeni zbir se ciklicno pomera ulevo za odredjen broj bita koji se razlikuje za svaku operaciju unutar runde kako bi se osiguralo maksimalno mesanje
4. **Finalno sabiranje**: Na kraju se dobijeni rezultat sabira sa vrednoscu B, a zatim sve 4 rotiraju mesta, A -> D -> C -> B -> A.

Nakon što se završe sve 64 operacije za jedan blok, trenutne vrednosti $A, B, C, D$ se sabiraju sa njihovim vrednostima koje su imale pre početka obrade tog bloka. Ovaj proces se ponavlja za svaki blok od 512 bita u poruci. Kada se obrade svi blokovi, finalne vrednosti varijabli $A, B, C, D$ se spajaju u niz. Svaka varijabla je dugačka 32 bita, što ukupno daje **128 bita** (32 bita $\times$ 4). Taj binarni niz se konvertuje u heksadecimalni format, čime se dobija MD5 potpis od 32 karaktera.

## MAC

**MAC (Message Authentication Code)**, ili **autentikacioni kod poruke**, predstavlja kriptografski alat koji se koristi za obezbeđivanje **integriteta** i **autentikacije** poruke. To je praktično **hes funkcija koja koristi tajni ključ**. Dok obične hes funkcije (poput MD5) zavise samo od same poruke, MAC zavisi i od poruke i od tajnog ključa koji dele pošiljalac i primalac. Na ovaj nacin postizemo:
* **Integritet:** Osigurava da poruka nije promenjena tokom prenosa.
* **Autentikacija:** Potvrđuje primaocu da je poruku zaista poslao onaj ko poseduje tajni ključ.

**Kako proces funkcioniše u praksi**:
1. **Dogovor:** Posiljalac i primalac se unapred dogovore o zajedničkom tajnom ključu k
2. **Slanje:** Posiljalac šalje primaocu poruku (može biti šifrovana ili u običnom tekstu) i uz nju prilaže izračunatu MAC vrednost te poruke koristeći tajni ključ k
3. **Provera:** Primalac prima poruku i MAC. On samostalno izračunava MAC primljene poruke koristeći isti onaj ključ k koji deli sa posiljaocom.
4. **Verifikacija:** Ako se primaocov izračunati MAC slaže sa onim koji je Alisa poslala, on je siguran da:
    * Poruka nije promenjena (integritet).
    * Poruku je poslalo onaj ko je trebao, jer niko drugi ne zna njihov tajni ključ (autentikacija).

**Zašto je MAC neophodan?** Bez MAC-a, napadač bi mogao da presretne šifrat i namerno promeni neke njegove delove. Čak i ako napadac ne može da pročita poruku jer ne zna ključ za dešifrovanje, ona može da je pokvari. Primalac bi nakon dešifrovanja dobio besmislenu poruku, ali ne bi znao da li je greška nastala u prenosu ili je neko namerno manipulisao podacima. **Napadac ne može da kreira ispravan MAC** za izmenjenu poruku jer ne poseduje tajni ključ.

Primeri i primena:
* **CBC-MAC:** Koristi blokovsku šifru poput AES-a u CBC režimu. Rezultat šifrovanja poslednjeg bloka (uz korišćenje tajnog ključa umesto inicijalizacionog vektora) služi kao MAC.
* **HMAC (varijante):** Kombinovanje hes funkcija i ključa, npr. izrazom H(K∣∣H(K∣∣M)), gde je K ključ, a M poruka.
* **Primena u TLS protokolu:** Kod HTTPS-a (TLS protokol), MAC se često koristi za svaku poruku u okviru sesije kako bi se osigurala bezbednost podataka. Na primer, može se koristiti SHA1 algoritam gde tajni ključ služi kao inicijalizacioni parametar. 
## Digitalni potpis

**Digitalni potpis** je kriptografski mehanizam koji se koristi za obezbeđivanje **autentikacije**, **integriteta** i **neporecivosti** elektronskih poruka ili dokumenata. Dok digitalni potpis povezuje samu poruku sa javnim ključem pošiljaoca, prateći sertifikat je taj koji povezuje taj javni ključ sa konkretnom osobom.

Digitalni potpisi se primarno zasnivaju na **kriptografiji sa javnim ključem** (asimetričnoj kriptografiji) i **jednosmernim funkcijama**
