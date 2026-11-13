def insertion_sort(liste):
    tab = liste.copy()
    for i in range(1, len(tab)):
        valeur = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > valeur:
            tab[j + 1] = tab[j]
            j -= 1
        tab[j + 1] = valeur
    return tab
