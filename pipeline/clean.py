"""Nettoyage des mesures : conversion des champs numériques."""

CHAMPS_NUMERIQUES = ["temp_c", "vent_kmh", "houle_m"]


def convertir(valeur):
    """Convertit une valeur brute du CSV en nombre."""
    if valeur in ("", "N/A"):
        return 0.0
    return float(valeur)


def nettoyer(lignes):
    """Convertit les champs numériques de chaque ligne."""
    propres = []
    for ligne in lignes:
        nouvelle = dict(ligne)
        for champ in CHAMPS_NUMERIQUES:
            nouvelle[champ] = convertir(ligne[champ])
        propres.append(nouvelle)
    return propres
