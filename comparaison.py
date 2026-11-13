import csv
from pathlib import Path

from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from quick_sort import quick_sort
from donnees import TYPES, generer_donnees
from benchmark import mesurer_temps
from benchmark_memoire import mesurer_memoire
from benchmark_energie import estimer_energie_j, PUISSANCE_SUPPOSEE_W

ALGORITHMES = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort,
}
TAILLES = (100, 1000, 5000)
REPETITIONS_TEMPS = 10
REPETITIONS_MEMOIRE = 5


def executer_comparaison():
    sortie = Path(__file__).resolve().parent / "resultats"
    sortie.mkdir(exist_ok=True)
    lignes = []
    for type_liste in TYPES:
        for taille in TAILLES:
            donnees = generer_donnees(taille, type_liste, seed=42 + taille)
            attendu = sorted(donnees)
            print(f"\n{type_liste} / {taille} elements", flush=True)
            for nom, fonction in ALGORITHMES.items():
                t = mesurer_temps(fonction, donnees, attendu, REPETITIONS_TEMPS)
                m = mesurer_memoire(fonction, donnees, attendu, REPETITIONS_MEMOIRE)
                energie = estimer_energie_j(t["temps_moyen_ms"])
                ligne = {
                    "type_liste": type_liste,
                    "taille": taille,
                    "algorithme": nom,
                    **t,
                    **m,
                    "energie_estimee_j": energie,
                    "puissance_supposee_w": PUISSANCE_SUPPOSEE_W,
                }
                lignes.append(ligne)
                print(f"  {nom:16} {t['temps_moyen_ms']:10.3f} ms | "
                      f"{m['pic_memoire_moyen_ko']:10.2f} Ko | "
                      f"{energie:10.6f} J (estime)", flush=True)
    csv_path = sortie / "benchmark_complet.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)
    print(f"\nCSV : {csv_path}")
    return lignes, sortie


def creer_graphiques(lignes, sortie):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib absent : graphiques ignores. Installer avec : python -m pip install -r requirements.txt")
        return

    indicateurs = (
        ("temps_moyen_ms", "Temps moyen (ms)", "temps"),
        ("pic_memoire_moyen_ko", "Pic allocations Python (Ko)", "memoire"),
        ("energie_estimee_j", "Energie estimee (J)", "energie_estimee"),
    )
    for type_liste in TYPES:
        for champ, etiquette, nom_fichier in indicateurs:
            fig, ax = plt.subplots(figsize=(9, 5))
            for nom in ALGORITHMES:
                selection = sorted(
                    (l for l in lignes if l["type_liste"] == type_liste and l["algorithme"] == nom),
                    key=lambda l: l["taille"],
                )
                ax.plot([l["taille"] for l in selection],
                        [l[champ] for l in selection], marker="o", label=nom)
            ax.set_title(f"{etiquette} - {type_liste}")
            ax.set_xlabel("Nombre d'elements")
            ax.set_ylabel(etiquette)
            ax.grid(alpha=0.3)
            ax.legend()
            fig.tight_layout()
            chemin = sortie / f"{nom_fichier}_{type_liste}.png"
            fig.savefig(chemin, dpi=200)
            plt.close(fig)
    print("12 graphiques PNG enregistres dans resultats/")
