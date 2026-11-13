import statistics
import time

def mesurer_temps(fonction, donnees, attendu, repetitions=10):
    mesures = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        resultat = fonction(donnees)
        duree = (time.perf_counter() - debut) * 1000
        if resultat != attendu:
            raise AssertionError("Tri incorrect")
        mesures.append(duree)
    return {
        "temps_moyen_ms": statistics.mean(mesures),
        "temps_ecart_type_ms": statistics.stdev(mesures) if len(mesures) > 1 else 0.0,
        "temps_min_ms": min(mesures),
        "temps_max_ms": max(mesures),
    }
