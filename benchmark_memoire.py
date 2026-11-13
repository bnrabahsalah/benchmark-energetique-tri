import gc
import statistics
import tracemalloc

def mesurer_memoire(fonction, donnees, attendu, repetitions=5):
    pics = []
    for _ in range(repetitions):
        gc.collect()
        tracemalloc.start()
        try:
            resultat = fonction(donnees)
            _, pic = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        if resultat != attendu:
            raise AssertionError("Tri incorrect")
        pics.append(pic / 1024)
    return {"pic_memoire_moyen_ko": statistics.mean(pics)}
