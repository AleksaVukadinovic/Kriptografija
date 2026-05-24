# Problem
# ---------------------
# Ana ima neki podatak m koji zeli da posalje Bobanu, ali mozda ne zeli odmah da ga otkrije
# Boban zeli da dobije garanciju od Ane da, kada mu Ana konacno posalje neki podatak (mzd cak i preko posrednika, Eve)
# on moze nezavisno da se uveri da je zaista dobio pravi podataka m
# ---------------------
#
# Kriptografska hes funkcija je kriptografska primitva koji nam omogucava da prozivoljnom podatku pridruzmo kratak "otisak prsta".
# Formalnije, kriptografska hes funkcija preslikava proizvoljnu poruku m u niz bitova h(m) fiksne duzine n (npr. 256),
# pri cemu mora da postuje sledeca pravila:
# 1. Otpornost na inverznu sliku: Za dato d nije moguce pronaci poruku m tako da je h(m) = d
# 2. Otpornost na drugu inverznu sliku: Za dato m nije moguce pronaci m' t.d. h(m) = h(m')
# 3. Otpornost na kolizije: Nije moguce pronaci par razlicitih poruka m i m' t.d h(m) = h(m')
#
# Kad se kaze nije moguce, misli da nije moguce u razumnom vremenu.
#
# Takodje je bitno da funkcije imaju sledeca svojstva:
# - Deterministcnost, za isto x, funkcija h uvek daje isto y tj. H(x)=y.
# - Bez obzira na velicinu ulazne poruke, hes je uvek iste duzine
# - Brzo se racuna
# - Jednosmerna funkcija, tj. skoro nemoguce izracunati inverz
# - Kolizije treba sto redje da nastaju
#
# Primeri hes funkcija:
# MD5 -> 128b hes
# - SHA-0 i 1 -> 160b hes
# - SHA-2 razne varijante (224-512b)
# - SHA-3 razne varijante (224-512b)
# - RIPEMD
# - Whirlpool
#
# Primetimo da sve ove funkcije imaju velicinu hesa barem 160b. To upravo ima veze sa rodjenaskim paradoksom.
# Rodjendanski paradoks: U grupi od samo 23 osobe, sansa da barem dvoje ljudi ima isti rodjendan je veca od 50%
#
#
