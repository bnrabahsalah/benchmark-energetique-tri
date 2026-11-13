
import random
import time
import tracemalloc
import statistics
import csv
import gc
import os

import matplotlib.pyplot as plt

from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from quick_sort import quick_sort

# PARAMETRES
PUISSANCE_WATTS = 20  # Hypothese, pas une mesure
TAILLES = [100, 1000, 5000]
REPETITIONS = 5

ALGORITHMES = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort
}

# Dossier de sortie
os.makedirs("resultats", exist_ok=True)

resultats = []
random.seed(42)

print("===== BENCHMARK COMPLET MOOC =====")

# BENCHMARK
for taille in TAILLES:
    print(f"\nTest avec {taille} elements")

    donnees = [
        random.randint(1, 100000)
        for _ in range(taille)
    ]

    attendu = sorted(donnees)

    for nom, fonction in ALGORITHMES.items():
        temps = []
        memoires = []

        for _ in range(REPETITIONS):

            # Mesure du temps sans tracemalloc
            debut = time.perf_counter()
            resultat = fonction(donnees)
            fin = time.perf_counter()

            assert resultat == attendu
            temps.append((fin - debut) * 1000)

            # Mesure de la memoire separee
            gc.collect()
            tracemalloc.start()

            resultat = fonction(donnees)
            _, pic = tracemalloc.get_traced_memory()

            tracemalloc.stop()

            assert resultat == attendu
            memoires.append(pic / 1024)

        temps_moyen = statistics.mean(temps)
        memoire_moyenne = statistics.mean(memoires)

        # Conversion ms -> s puis estimation E = P * t
        energie = PUISSANCE_WATTS * temps_moyen / 1000

        resultats.append({
            "algorithme": nom,
            "taille": taille,
            "temps_ms": temps_moyen,
            "memoire_ko": memoire_moyenne,
            "energie_j": energie
        })

        print(
            f"{nom:16} | "
            f"{temps_moyen:.3f} ms | "
            f"{memoire_moyenne:.2f} Ko | "
            f"{energie:.6f} J"
        )

# EXPORT CSV
chemin_csv = "resultats/benchmark.csv"

with open(chemin_csv, "w", newline="", encoding="utf-8") as f:
    colonnes = [
        "algorithme",
        "taille",
        "temps_ms",
        "memoire_ko",
        "energie_j"
    ]

    writer = csv.DictWriter(f, fieldnames=colonnes)
    writer.writeheader()
    writer.writerows(resultats)

print(f"\nCSV enregistre : {chemin_csv}")

# CREATION DES GRAPHIQUES
graphiques = [
    ("temps_ms", "Temps d'execution", "Temps (ms)", "temps.png"),
    ("memoire_ko", "Memoire allouee", "Pic memoire (Ko)", "memoire.png"),
    ("energie_j", "Energie estimee", "Energie (J)", "energie.png")
]

for colonne, titre, unite, fichier in graphiques:

    plt.figure(figsize=(9, 5))

    for nom in ALGORITHMES:
        lignes = [
            r for r in resultats
            if r["algorithme"] == nom
        ]

        x = [r["taille"] for r in lignes]
        y = [r[colonne] for r in lignes]

        plt.plot(x, y, marker="o", label=nom)

    plt.title(titre)
    plt.xlabel("Nombre d'elements")
    plt.ylabel(unite)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    chemin = os.path.join("resultats", fichier)
    plt.savefig(chemin, dpi=300)
    plt.close()

    print(f"Graphique enregistre : {chemin}")

print("\nBENCHMARK TERMINE AVEC SUCCES !")
