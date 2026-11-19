"""Rapport météo-houle de la côte basque."""
from pipeline.load import charger
from pipeline.clean import nettoyer
from pipeline.stats import moyenne_par_station


def rapport(lignes):
    temp = moyenne_par_station(lignes, "temp_c")
    houle = moyenne_par_station(lignes, "houle_m")
    print("=== Rapport côte basque ===")
    for station in sorted(temp):
        print(f"{station} : température moyenne {temp[station]} °C, houle moyenne {houle[station]} m")


if __name__ == "__main__":
    rapport(nettoyer(charger("data/mesures.csv")))
