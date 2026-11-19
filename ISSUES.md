# Tickets — Rapport météo-houle côte basque

Chaque ticket = **une branche** = **un worktree** = **un « agent »**.
Chaque ticket se corrige en **une seule ligne** : le code à écrire est donné. Le défi n'est pas Python, c'est Git.

## Répartition dans le binôme

| Étudiant | Tour 1 (obligatoire) | Tour 2 (si le temps) |
|---|---|---|
| **A** | T01 | T05 |
| **B** | T04 | T06 |

A relit et merge les PR de B, B relit et merge celles de A.

---

## Tour 1

### T01 · Correctif · Les valeurs manquantes faussent les moyennes  (étudiant A)
- **Branche** : `fix/T01-valeurs-manquantes` · **Worktree** : `../meteo-T01`
- **Problème** : Anglet affiche 11.7 °C de moyenne alors qu'aucune mesure n'est sous 13,6 °C.
  Une valeur manquante est comptée comme un 0.
- **Fichier** : `pipeline/clean.py`, fonction `convertir()`

Avant :
```python
        return 0.0
```
Après :
```python
        return None
```
- **Vérifier** : `python main.py` → Anglet affiche `14.625`.
- **Commit** : `T01 : une valeur manquante devient None`

### T04 · Dette technique · Nouvelles valeurs manquantes  (étudiant B)
- **Branche** : `chore/T04-valeurs-manquantes` · **Worktree** : `../meteo-T04`
- **Problème** : les stations envoient aussi `"NA"` et `"-"` pour une mesure absente.
- **Fichier** : `pipeline/clean.py`, fonction `convertir()`

Avant :
```python
    if valeur in ("", "N/A"):
```
Après :
```python
    if valeur in ("", "N/A", "NA", "-"):
```
- **Vérifier** : `python main.py` tourne toujours.
- **Commit** : `T04 : NA et - sont aussi des valeurs manquantes`

---

## Tour 2

### T05 · Évolutif · Stations en majuscules  (étudiant A)
- **Branche** : `feat/T05-majuscules` · **Worktree** : `../meteo-T05`
- **Fichier** : `main.py`, ligne du `print(f"{station} : ...`
- **Changement** : remplacer `{station}` par `{station.upper()}`
- **Vérifier** : `python main.py` → `ANGLET : ...`
- **Commit** : `T05 : noms de station en majuscules`

### T06 · Correctif · Trop de décimales  (étudiant B)
- **Branche** : `fix/T06-arrondi` · **Worktree** : `../meteo-T06`
- **Problème** : Hendaye affiche une houle moyenne de `1.3400000000000003 m`.
- **Fichier** : `main.py`, ligne du `print(f"{station} : ...`
- **Changement** : remplacer `{temp[station]}` par `{temp[station]:.1f}` et `{houle[station]}` par `{houle[station]:.1f}`
- **Vérifier** : `python main.py` → Hendaye affiche `1.3 m`.
- **Commit** : `T06 : arrondi à 1 décimale`

---

## Tickets bonus (tech leads et binômes rapides : pas de solution fournie)

### T02 · Évolutif · Houle maximale par station
Ajouter `max_par_station(lignes, champ)` dans `pipeline/stats.py` et l'afficher dans le rapport.

### T03 · Évolutif · Vent en nœuds
Ajouter une fonction `kmh_vers_noeuds(v)` (1 nœud = 1,852 km/h) et afficher le vent moyen en nœuds.

### T07 · Dette technique · Tests manquants
Ajouter des tests pour `moyenne_par_station()`, y compris avec des valeurs manquantes.

### T08 · Correctif · Accents illisibles sous Windows
Dans certains terminaux Windows, « côte » s'affiche « c�te ». Corriger l'affichage sans casser Linux/Mac.

### T09 · Évolutif · Exporter le rapport en Markdown
En plus de l'affichage console, écrire un fichier `rapport.md` contenant un tableau
`| Station | Température moyenne (°C) | Houle moyenne (m) |`.
