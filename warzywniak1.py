from collections import Counter
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
 [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0], #puste
]

def ewaluuj(stary_uklad, nowy_uklad):
    wartosc=0
    kolumny = 5
    for i in range(len(stary_uklad)):
        wartosc += zasady_matrix[stary_uklad[i]][nowy_uklad[i]]
    for i in range(len(nowy_uklad)):
        if (i % kolumny) != kolumny - 1:
            wartosc += sasiedzi_matrix[nowy_uklad[i]][nowy_uklad[i + 1]]
        if i + kolumny < len(nowy_uklad):
            wartosc += sasiedzi_matrix[nowy_uklad[i]][nowy_uklad[i + kolumny]]
    return wartosc

def ewaluuj_zesz(stary_uklad, nowy_uklad):
    wartosc=0
    for i in range(len(stary_uklad)):
        wartosc += zasady_matrix[stary_uklad[i]][nowy_uklad[i]]
    return wartosc

def ewaluuj_sasiad(nowy_uklad):
    kolumny = 5
    wartosc = 0
    for i in range(len(nowy_uklad)):
        if (i % kolumny) != kolumny - 1:
            wartosc += sasiedzi_matrix[nowy_uklad[i]][nowy_uklad[i + 1]]
        if i + kolumny < len(nowy_uklad):
            wartosc += sasiedzi_matrix[nowy_uklad[i]][nowy_uklad[i + kolumny]]
    return wartosc

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
warzywa = [warzywa_mapping[t] for t in warzywa]

stary_uklad = ( "koper      ogorek  ogorek  puste   czosnek "
                "cebula     cukinia burak   fasolka pietruszka "
                "truskawka  pomidor pomidor salata  salata" )
stary_uklad = stary_uklad.split()
stary_uklad = [warzywa_mapping[t] for t in stary_uklad]


uklad = 15*[]
czesciowe_wyniki = []

rozmiar = len(stary_uklad)
rodzaje = len(warzywa_mapping)

sasiedzi_matrix = [[0 for t in range(rodzaje)] for t in range(rodzaje)]

def sasiedzi(w1, w2, wartosc):
    sasiedzi_matrix[warzywa_mapping[w1]][warzywa_mapping[w2]] = wartosc
    sasiedzi_matrix[warzywa_mapping[w2]][warzywa_mapping[w1]] = wartosc

def stworz_sasiadow():
    sasiedzi("fasolka", "cebula", -1)
    sasiedzi("fasolka", "pomidor", 1)
    sasiedzi("fasolka", "burak", 1)
    sasiedzi("fasolka", "salata", 1)
    sasiedzi("fasolka", "ogorek", 1)
    sasiedzi("fasolka", "truskawka", 1)

    sasiedzi("koper", "cebula", 1)
    sasiedzi("koper", "burak", 1)
    sasiedzi("koper", "salata", 1)
    sasiedzi("koper", "marchew", 1)
    sasiedzi("koper", "ogorek", 1)

    sasiedzi("truskawka", "cebula", 1)
    sasiedzi("truskawka", "burak", 1)
    sasiedzi("truskawka", "pietruszka", 1)
    sasiedzi("truskawka", "czosnek", 1)

    sasiedzi("ogorek", "pomidor", -1)
    sasiedzi("ogorek", "cebula", 1)
    sasiedzi("ogorek", "burak", 1)
    sasiedzi("ogorek", "czosnek", 1)
    sasiedzi("ogorek", "ogorek", 7)

    sasiedzi("marchew", "cebula", 1)
    sasiedzi("marchew", "pomidor", 1)
    sasiedzi("marchew", "czosnek", 1)

    sasiedzi("czosnek", "pomidor", 1)
    sasiedzi("czosnek", "burak", 1)

    sasiedzi("pietruszka", "pomidor", 1)

    sasiedzi("salata", "pomidor", 1)
    sasiedzi("salata", "burak", 1)

    sasiedzi("burak", "cebula", 1)
    sasiedzi("burak", "pomidor", 1)

    sasiedzi("cukinia", "cebula", 1)

stworz_sasiadow()

sasiedzi_flat = [sasiedzi_matrix[i][j] for i in range(rodzaje) for j in range(rodzaje)]
"""
for t in range(len(sasiedzi_matrix)):
    print(sasiedzi_matrix[t])
"""

model = cp_model.CpModel()
x= [model.NewIntVar(0, rodzaje-1, f'x[{i}]') for i in range(rozmiar)]

#twarde wymagania
model.Add(x[3] == warzywa_mapping["puste"])
model.Add(x[10] == warzywa_mapping["truskawka"])

#punktowanie w porownaniu do zeszlego roku
for i in range(rozmiar):
    wartosc = zasady_matrix[stary_uklad[i]]

    wartosc_pozycji = model.NewIntVar(-100, 100, f'wartosc_pozycji[{i}]')
    model.AddElement(x[i], wartosc, wartosc_pozycji)

    czesciowe_wyniki.append(wartosc_pozycji)

#ilosc warzyw zgodna z podana na wejsciu
ilosci = Counter(warzywa)

for warzywo, ile_ma_byc in ilosci.items():
    wystapienia = []

    for i in range(rozmiar):
        czy_sprawdzane = model.NewBoolVar(f"czy_{warzywo}_na_pozycji_{i}")

        model.Add(x[i] == warzywo).OnlyEnforceIf(czy_sprawdzane)
        model.Add(x[i] != warzywo).OnlyEnforceIf(czy_sprawdzane.Not())
        wystapienia.append(czy_sprawdzane)
    #sprawdzamy ilosc wystapien konkretnego warzywa
    model.Add(sum(wystapienia) == ile_ma_byc)

#jakie warzywa moga byc kolo siebie
kolumny = 5
for pole in range(rozmiar):
    #sasiedzi w prawoi
    if (pole % kolumny) != kolumny - 1:
        sasiad = pole + 1
        id_pary = model.NewIntVar(0, rodzaje * rodzaje -1, f'id_pary[{pole}, {sasiad}]')
        model.Add(id_pary == x[pole] * rodzaje + x[sasiad])

        wartosc_sasiadow = model.NewIntVar(-100, 100, f'wartosc_sasiadow[{pole}, {sasiad}]')
        model.AddElement(id_pary, sasiedzi_flat, wartosc_sasiadow)

        czesciowe_wyniki.append(wartosc_sasiadow)
    if pole + kolumny < rozmiar:
        sasiad = pole + kolumny
        id_pary = model.NewIntVar(0, rodzaje * rodzaje - 1, f'id_pary[{pole}, {sasiad}]')
        model.Add(id_pary == x[pole] * rodzaje + x[sasiad])

        wartosc_sasiadow = model.NewIntVar(-100, 100, f'wartosc_sasiadow[{pole}, {sasiad}]')
        model.AddElement(id_pary, sasiedzi_flat, wartosc_sasiadow)

        czesciowe_wyniki.append(wartosc_sasiadow)


model.Maximize(sum(czesciowe_wyniki))
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 18000

result = solver.Solve(model)

if result == cp_model.OPTIMAL: #or result == cp_model.FEASIBLE:
    solution = [solver.Value(x[i]) for i in range(rozmiar)]
    print([warzywa_demapping[v] for v in solution])
    print("Score:", solver.ObjectiveValue())
else:
    print("No solution")

print("Sanity check: ",ewaluuj(stary_uklad, solution))
print("Zeszloroczne wartosc: ", ewaluuj_zesz(stary_uklad, solution))
print("Sasiedzi wartosc: ", ewaluuj_sasiad(solution))