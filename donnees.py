import random

TYPES = ("aleatoire", "triee", "inversee", "doublons")

def generer_donnees(taille, type_liste, seed=42):
    if taille < 0:
        raise ValueError("Taille negative")
    rng = random.Random(seed)
    if type_liste == "aleatoire":
        return [rng.randint(1, 100000) for _ in range(taille)]
    if type_liste == "triee":
        return list(range(taille))
    if type_liste == "inversee":
        return list(range(taille, 0, -1))
    if type_liste == "doublons":
        return [rng.randint(1, 10) for _ in range(taille)]
    raise ValueError(f"Type inconnu : {type_liste}")

if __name__ == "__main__":
    for type_liste in TYPES:
        print(type_liste, generer_donnees(10, type_liste))
