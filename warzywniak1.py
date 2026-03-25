from collections import Counter
from math import inf
from more_itertools import distinct_permutations
from ortools.sat.python import cp_model

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

warzywa =  ("fasolka koper truskawka ogorek ogorek marchew czosnek pietruszka salata burak cukinia cebula pomidor pomidor puste")
warzywa = warzywa.split()
warzywa = [warzywa_mapping[x] for x in warzywa]

stary_uklad = ( "koper      ogorek  ogorek  puste   czosnek "
                "cebula     cukinia burak   fasolka pietruszka "
                "truskawka  pomidor pomidor salata  salata" )
stary_uklad = stary_uklad.split()
stary_uklad = [warzywa_mapping[x] for x in stary_uklad]

wiersze = [zasady_matrix[t] for t in stary_uklad]

uklad = 15*[]
czesciowe_wyniki = []

rozmiar = len(stary_uklad)
rodzaje = len(warzywa)-2

model = cp_model.CpModel()
x= [model.NewIntVar(0, rodzaje-1, f'x[{i}]') for i in range(rozmiar)]

#twarde wymagania
model.Add(x[4] == warzywa_mapping["puste"])
model.Add(x[11] == warzywa_mapping["truskawka"])

for i in range(rozmiar): #punktowanie w porownaniu do zeszlego roku
    wartosc = zasady_matrix[stary_uklad[i]]

    wartosc_pozycji = model.NewIntVar(-1, 1, f'wartosc_pozycji[{i}]')
    model.AddElement(x[i], wartosc, wartosc_pozycji)

    czesciowe_wyniki.append(wartosc_pozycji)

model.Maximize(sum(czesciowe_wyniki))

#ilosc warzyw zgodna z podana na wejsciu
ilosci = Counter(warzywa)

for warzywo, ile_ma_byc in ilosci.items(): #poprawna ilosc wystapien warzyw
    wystapienia = []

    for i in range(rozmiar):
        czy_sprawdzane = model.NewBoolVar(f"czy_{warzywo}_na_pozycji_{i}")

        model.Add(x[i] == warzywo).OnlyEnforceIf(czy_sprawdzane)
        model.Add(x[i] != warzywo).OnlyEnforceIf(czy_sprawdzane.Not())
        wystapienia.append(czy_sprawdzane)
    #sprawdzamy ilosc wystapien konkretnego warzywa
    model.Add(sum(wystapienia) == ile_ma_byc)

for i in range(rozmiar):
    model.Add(sum(uklad[i][veg] for veg in range(13)) == 11)


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