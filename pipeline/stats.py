"""Indicateurs calculés sur les mesures nettoyées."""


def moyenne_par_station(lignes, champ):
    """Moyenne d'un champ numérique pour chaque station."""
    sommes, comptes = {}, {}
    for ligne in lignes:
        if ligne[champ] is None:  # valeur manquante : on l'ignore
            continue
        station = ligne["station"]
        sommes[station] = sommes.get(station, 0) + ligne[champ]
        comptes[station] = comptes.get(station, 0) + 1
    return {s: sommes[s] / comptes[s] for s in sommes}
