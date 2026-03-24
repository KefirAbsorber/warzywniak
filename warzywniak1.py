from math import inf
from more_itertools import distinct_permutations


zasady_matrix =[ # stare x nowe
# fas kop trus ogo mar czo pie sal bur cuk ceb pom pus
 [-1, 0, -10,  1,  1,  0,  0,  1,  0,  1,  1,  1, -100], #fas
 [0,  0, -10,  0,  0,  0,  0,  0,  0,  0,  0,  0, -100], #kop
 [0,  0,  10,  0,  0,  0,  0,  0,  0,  0,  0,  0, -100], #tru
 [1,  0, -10, -1,  0,  1,  1,  0,  0, -1,  0, -1, -100], #ogo
 [-1, 0, -10,  0, -1,  0, -1,  1, -1,  0,  1,  0, -100], #mar
 [0,  0, -10,  1,  0, -1,  0,  0,  0,  1,  0,  1, -100], #czo
 [0,  0, -10,  0, -1,  0, -1,  0, -1,  0,  1,  0, -100], #pie
 [1,  0, -10,  0,  0, -1,  1, -1,  1,  1,  0,  1, -100], #sal
 [0,  0, -10,  0, -1,  0, -1,  1, -1,  0,  1,  0, -100], #bur
 [0,  0, -10, -1,  0,  1,  1,  0,  0, -1,  0, -1, -100], #cuk
 [1,  0, -10,  1,  0, -1,  0,  1,  0,  1, -1,  1, -100], #ceb
 [0,  0, -10, -1,  0,  0,  0,  0,  0,  0,  0, -1, -100], #pom
 [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10, 100], #puste
]

warzywa_mapping = {
    "fasolka" : 0,
    "koper" : 1,
    "truskawka" : 2,
    "ogorek" : 3,
    "marchew" : 4,
    "czosnek" : 5,
    "pietruszka" : 6,
    "salata" : 7,
    "burak" : 8,
    "cukinia" : 9,
    "cebula" : 10,
    "pomidor" : 11,
    "puste" : 12,
}

warzywa_demapping = {v: k for k, v in warzywa_mapping.items()}

def ewaluuj(stary_uklad, nowy_uklad):
    wartosc=0
    for i in range(len(stary_uklad)):
        wartosc += zasady_matrix[stary_uklad[i]][nowy_uklad[i]]
    return wartosc

warzywa =  ("fasolka koper truskawka ogorek ogorek marchew czosnek pietruszka salata burak cukinia cebula pomidor pomidor puste")
warzywa = warzywa.split()
warzywa = [warzywa_mapping[x] for x in warzywa]
uklady=distinct_permutations(warzywa)

print("Permutacje done")

stary_uklad = ( "koper      ogorek  ogorek  puste   czosnek "
                "cebula     cukinia burak   fasolka pietruszka "
                "truskawka  pomidor pomidor salata  salata" )

stary_uklad = stary_uklad.split()
stary_uklad = [warzywa_mapping[x] for x in stary_uklad]


maks=-inf
najlepszy=[]
for uklad in uklady:
    if uklad[4] != 12:
        continue
    aktualny=ewaluuj(stary_uklad, uklad)
    if aktualny>maks:
        maks=aktualny
        najlepszy=[uklad]
    elif aktualny == maks:
        najlepszy.append(uklad)

opcje_demap=[]
i=0
for uklad in najlepszy:
    opcje_demap.append([])
    for t in uklad:
        opcje_demap[i].append(warzywa_demapping.get(t))
    i=i+1

print("Najwyzsza wartosc:", maks-100)
for i in opcje_demap:
    print("Opcja nr:", i)
    for j in range(4):
        print(i[j:5*(j+1)])