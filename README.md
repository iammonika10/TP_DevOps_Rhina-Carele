# TP2 — Orchestrateur d'agents

ESTIA BIHAR · M23 · Git à l'ère des agents IA

Un agent IA (Claude Code, Copilot, Cursor…) travaille **dans son propre worktree, sur sa propre branche**,
et son travail n'entre dans `main` qu'après une **pull request relue par un humain**.
Aujourd'hui, **c'est vous les agents** : chaque ticket = un worktree = un « agent ».

Le projet : un mini-pipeline Python qui lit des mesures météo / houle de la côte basque et affiche un rapport.
**Chaque ticket se corrige en une ligne, le code est donné dans [ISSUES.md](ISSUES.md).** Le défi, c'est Git.

> **Réflexe n°1** : avant chaque commande, regardez dans quel dossier vous êtes (le chemin affiché par le terminal)
> et sur quelle branche (`git status`).

## Étape 1 · Setup (10 min)
1. **Étudiant A** : sur la page GitHub du dépôt modèle, *Use this template* → *Create a new repository* (public).
2. A invite B : *Settings → Collaborators → Add people*. B accepte l'invitation (mail ou notification GitHub).
3. **Chacun**, sur son ordinateur :
   ```bash
   git clone https://github.com/<compte-de-A>/<nom-du-depot>.git meteo
   cd meteo
   python main.py
   ```
   Le rapport s'affiche : Anglet à 11.7 °C, Hendaye à 1.3400000000000003 m. Ce sont les bugs à corriger.

## Étape 2 · Tour 1 : lancer son agent (10 min)
**A** (ticket T01) :
```bash
git worktree add ../meteo-T01 -b fix/T01-valeurs-manquantes
cd ../meteo-T01
code .
```
**B** (ticket T04) :
```bash
git worktree add ../meteo-T04 -b chore/T04-valeurs-manquantes
cd ../meteo-T04
code .
```
Une nouvelle fenêtre d'éditeur s'ouvre sur le worktree : **c'est votre agent**.
Faites la modification d'une ligne décrite dans ISSUES.md, enregistrez (Ctrl+S), puis :
```bash
python main.py
git worktree list
```

## Étape 3 · Livrer (15 min)
Dans le worktree de votre ticket :
```bash
git add -p            # Git montre chaque morceau modifié : relisez, tapez y puis Entrée
git commit -m "T01 : une valeur manquante devient None"
git push -u origin fix/T01-valeurs-manquantes
```
(B : même chose avec son message et sa branche `chore/T04-valeurs-manquantes`.)

Sur GitHub : onglet **Pull requests → New pull request**, choisir votre branche → *Create pull request*.

**Revue croisée** : ouvrez la PR de l'autre, onglet *Files changed*, relisez le diff.
1. **B merge la PR T01 de A** (*Merge pull request → Confirm merge*).
2. Regardez la PR T04 : **« This branch has conflicts »**. C'est normal, T01 et T04 touchent les mêmes lignes.

## Étape 4 · Conflit ! (15 min)
**B**, dans `meteo-T04` :
```bash
git fetch origin
git merge origin/main
```
Git annonce `CONFLICT (content): Merge conflict in pipeline/clean.py`. Dans l'éditeur, le fichier contient :
```text
<<<<<<< HEAD
    if valeur in ("", "N/A", "NA", "-"):
        return 0.0
=======
    if valeur in ("", "N/A"):
        return None
>>>>>>> origin/main
```
En haut, votre version (T04) ; en bas, celle de `main` (T01). On garde **les deux corrections**,
et on supprime les 3 lignes de marqueurs `<<<<<<<`, `=======`, `>>>>>>>` :
```python
    if valeur in ("", "N/A", "NA", "-"):
        return None
```
Enregistrez, puis :
```bash
python main.py        # Anglet doit afficher 14.625
git add pipeline/clean.py
git commit -m "T04 : résolution du conflit avec T01"
git push
```
**A merge la PR T04** sur GitHub : elle n'est plus en conflit.

## Étape 5 · Tour 2 : même chose, rôles inversés (15 min, si le temps)
Revenez dans le dossier principal et mettez `main` à jour :
```bash
cd ../meteo
git pull
```
- **A** : `git worktree add ../meteo-T05 -b feat/T05-majuscules`, puis ticket T05.
- **B** : `git worktree add ../meteo-T06 -b fix/T06-arrondi`, puis ticket T06.

Livrez comme à l'étape 3. Cette fois, **A merge d'abord la PR T06 de B**, et c'est **A qui résout le conflit** de T05,
dans `meteo-T05`, avec `git fetch origin` puis `git merge origin/main`. Dans `main.py` :
```text
<<<<<<< HEAD
        print(f"{station.upper()} : température moyenne {temp[station]} °C, houle moyenne {houle[station]} m")
=======
        print(f"{station} : température moyenne {temp[station]:.1f} °C, houle moyenne {houle[station]:.1f} m")
>>>>>>> origin/main
```
Gardez **une seule ligne** qui combine les deux : `{station.upper()}` **et** les `:.1f`, enregistrez, puis :
```bash
python main.py        # ANGLET : ... 14.6 °C ... 2.5 m
git add main.py
git commit -m "T05 : résolution du conflit avec T06"
git push
```
**B merge la PR T05.**

## Étape 6 · Vérifier et ranger
Dans le dossier principal `meteo` :
```bash
cd ../meteo
git pull
python main.py
git log --oneline --graph --all
```
Le graphe montre vos branches, vos merges, et qui a fait quoi. Puis supprimez vos worktrees :
```bash
git worktree remove ../meteo-T01
git worktree list
```

## Pièges fréquents
- `fatal: 'main' is already checked out` : `main` est déjà ouvert dans le dossier `meteo`, c'est voulu.
- Rien ne change quand vous lancez `python main.py` : vous êtes dans le mauvais dossier, ou vous n'avez pas enregistré.
- `code ../meteo-T01` ouvre un fichier vide : vous n'étiez pas dans `meteo`. Utilisez `git worktree list` pour voir les chemins.
- Le push est refusé : avez-vous fait `git push -u origin <votre-branche>` la première fois ?

## Défis bonus (tech leads)
- Tickets T02, T03, T07, T08, T09 dans ISSUES.md (sans solution fournie)
- `git rebase -i` : transformer 5 commits « wip » en 1 commit propre avant la PR
- `git cherry-pick` : récupérer un seul commit d'une autre branche
- `git bisect` : retrouver automatiquement le commit qui a cassé un test
- `git reflog` : ressusciter une branche supprimée par erreur
