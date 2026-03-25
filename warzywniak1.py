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
 [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0], #puste
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


uklad = 15*[]
czesciowe_wyniki = []

rozmiar = len(stary_uklad)
rodzaje = len(warzywa_mapping)

model = cp_model.CpModel()
x= [model.NewIntVar(0, rodzaje-1, f'x[{i}]') for i in range(rozmiar)]

#twarde wymagania
model.Add(x[3] == warzywa_mapping["puste"])
model.Add(x[11] == warzywa_mapping["truskawka"])

for i in range(rozmiar): #punktowanie w porownaniu do zeszlego roku
    wartosc = zasady_matrix[stary_uklad[i]]

    wartosc_pozycji = model.NewIntVar(-100, 100, f'wartosc_pozycji[{i}]')
    model.AddElement(x[i], wartosc, wartosc_pozycji)

    czesciowe_wyniki.append(wartosc_pozycji)

model.Maximize(sum(czesciowe_wyniki))

#ilosc warzyw zgodna z podana na wejsciu
ilosci = Counter(warzywa)


#poprawna ilosc wystapien warzyw
for warzywo, ile_ma_byc in ilosci.items():
    wystapienia = []

    for i in range(rozmiar):
        czy_sprawdzane = model.NewBoolVar(f"czy_{warzywo}_na_pozycji_{i}")

        model.Add(x[i] == warzywo).OnlyEnforceIf(czy_sprawdzane)
        model.Add(x[i] != warzywo).OnlyEnforceIf(czy_sprawdzane.Not())
        wystapienia.append(czy_sprawdzane)
    #sprawdzamy ilosc wystapien konkretnego warzywa
    model.Add(sum(wystapienia) == ile_ma_byc)


solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 18000

result = solver.Solve(model)

if result == cp_model.OPTIMAL: #or result == cp_model.FEASIBLE:
    solution = [solver.Value(x[i]) for i in range(rozmiar)]
    print([warzywa_demapping[v] for v in solution])
    print("Score:", solver.ObjectiveValue())
else:
    print("No solution")