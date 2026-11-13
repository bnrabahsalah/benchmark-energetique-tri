def quick_sort(liste):
    if len(liste) <= 1:
        return liste.copy()
    pivot = liste[len(liste) // 2]
    gauche = [x for x in liste if x < pivot]
    milieu = [x for x in liste if x == pivot]
    droite = [x for x in liste if x > pivot]
    return quick_sort(gauche) + milieu + quick_sort(droite)
