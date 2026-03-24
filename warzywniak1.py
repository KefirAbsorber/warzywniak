from more_itertools import distinct_permutations


zasady_matrix =[ # stare x nowe
#pom ogr rzod
 [0,    10, -10 ], #pomidor
 [-10,  -10,  10  ], #ogorek
 [0,    10, 0   ]  #rzodkiewka
]

warzywa_mapping = {
    "pomidor" : 0,
    "ogorek" : 1,
    "rzodkiewka" : 2,
}

warzywa_demapping = {v: k for k, v in warzywa_mapping.items()}

def ewaluuj(stary_uklad, nowy_uklad):
    wartosc=0
    for i in range(len(stary_uklad)):
        wartosc += zasady_matrix[stary_uklad[i]][nowy_uklad[i]]
    return wartosc
"""
warzywa = input("Podaj warzywa: ")
warzywa=warzywa.split()
"""
warzywa =  ("rzodkiewka rzodkiewka rzodkiewka rzodkiewka ogorek ogorek ogorek ogorek pomidor pomidor pomidor pomidor ")
warzywa = warzywa.split()
warzywa = [warzywa_mapping[x] for x in warzywa]
uklady=distinct_permutations(warzywa)

print("Permutacje done")

stary_uklad = ( 'ogorek   ogorek     pomidor '
                'ogorek   ogorek     pomidor '
                'pomidor  rzodkiewka rzodkiewka '
                'pomidor  rzodkiewka rzodkiewka')
stary_uklad = stary_uklad.split()
stary_uklad = [warzywa_mapping[x] for x in stary_uklad]


maks=0
najlepszy=[]
for uklad in uklady:
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

print("Najwyzsza wartosc: ", maks)
for i in opcje_demap:
    print(i)