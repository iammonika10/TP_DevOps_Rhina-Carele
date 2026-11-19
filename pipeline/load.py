"""Lecture du fichier de mesures brutes."""
import csv


def charger(chemin):
    """Retourne la liste des lignes du CSV sous forme de dictionnaires."""
    with open(chemin, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
