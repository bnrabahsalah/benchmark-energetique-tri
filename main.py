from comparaison import executer_comparaison, creer_graphiques

if __name__ == "__main__":
    print("=== MOOC : BENCHMARK D'ALGORITHMES ===")
    print("Temps reel, allocations Python mesurees, energie ESTIMEE (20 W supposes).")
    lignes, sortie = executer_comparaison()
    creer_graphiques(lignes, sortie)
    print("\nTERMINE : consulter le dossier resultats/")
