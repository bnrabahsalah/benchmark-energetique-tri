def bubble_sort(liste):
    tab = liste.copy()
    n = len(tab)
    for i in range(n):
        for j in range(n - i - 1):
            if tab[j] > tab[j + 1]:
                tab[j], tab[j + 1] = tab[j + 1], tab[j]
    return tab
