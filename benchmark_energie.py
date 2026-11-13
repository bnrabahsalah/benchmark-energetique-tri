# MODELE SIMPLIFIE : il ne s'agit PAS d'une mesure de consommation reelle.
PUISSANCE_SUPPOSEE_W = 20.0

def estimer_energie_j(temps_moyen_ms, puissance_w=PUISSANCE_SUPPOSEE_W):
    if temps_moyen_ms < 0 or puissance_w < 0:
        raise ValueError("Valeur negative")
    return puissance_w * temps_moyen_ms / 1000.0
