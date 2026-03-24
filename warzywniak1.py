from more_itertools import distinct_permutations

zasady={('pomidor','ogorek'):10,('pomidor','zodkiewka'):-10,('zodkiewka','ogorek'):10}

def ewaluuj(stary_uklad, nowy_uklad):
    wartosc=0
    for i in range(len(stary_uklad)):
        wartosc += zasady.get((stary_uklad[i], nowy_uklad[i]), 0)
    return wartosc


"""
warzywa = input("Podaj warzywa: ")
warzywa=warzywa.split()
"""
warzywa =  "ogorek zodkiewka pomidor pomidor pomidor pomidor pomidor ogorek"
uklady=distinct_permutations(warzywa)

print("Permutacje done")

stary_uklad='pomidor pomidor pomidor pomidor pomidor ogorek ogorek zodkiewka'
stary_uklad=stary_uklad.split()


maks=0
najlepszy=[]
for uklad in uklady:
    uklad = list(uklad)
    aktualny=ewaluuj(stary_uklad, uklad)
    if aktualny>maks:
        maks=aktualny
        najlepszy=uklad
    elif aktualny == maks:
        najlepszy.append(uklad)

print(f"{najlepszy}:{maks}")


