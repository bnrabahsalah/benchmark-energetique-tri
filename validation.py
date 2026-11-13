from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from quick_sort import quick_sort
from donnees import TYPES, generer_donnees
from benchmark_energie import estimer_energie_j

algorithmes = (bubble_sort, insertion_sort, quick_sort)
for liste in ([], [1], [3, 1, 2, 2, -1], list(range(50)), list(range(50, 0, -1))):
    for algo in algorithmes:
        assert algo(liste) == sorted(liste)
for type_liste in TYPES:
    liste = generer_donnees(100, type_liste)
    for algo in algorithmes:
        assert algo(liste) == sorted(liste)
assert estimer_energie_j(1000, 20) == 20
print("Tous les tests de validation ont reussi !")
