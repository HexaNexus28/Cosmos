# Cosmos — carnet de recherche

Raisonner comme des chercheurs sur ce qui reste ouvert en cosmologie : l'énergie noire, le vide,
la tension sur H₀. On repart des **données publiques**, on refait les calculs, on note des paris
chiffrés et on les révise quand de nouvelles mesures tombent.

## Méthode

1. **Séparer** ce qui est mesuré, ce qui est en tension, et ce qu'on parie.
2. **Valider avant d'interpréter** : tout calcul doit d'abord retrouver une valeur publiée.
3. **Parier avec un chiffre** et écrire ce qui ferait changer d'avis (`carnet/paris.md`).
4. **Noter les désaccords** entre nous deux, avec ce qui permettrait de trancher.

## Plan

| Dossier | Contenu |
|---|---|
| `carnet/questions.md` | Questions ouvertes, formulées pour être testables |
| `carnet/paris.md` | Registre des paris : probabilité, critère de révision, historique |
| `carnet/journal.md` | Ce qu'on a fait, daté |
| `carnet/desaccords.md` | Points où l'on ne pense pas pareil |
| `lectures/` | Fiches d'articles : ce qu'ils mesurent, comment, leurs points faibles |
| `calculs/` | Scripts Python ; `data/` est retéléchargeable, `resultats/` est versionné |

## Chapitre 0

[Planétaire Kepler](https://claude.ai/artifact/PVGdVNXczuGaDFkVoZXDPv) : retrouver les lois de Kepler,
Newton, la masse de Sgr A*, la matière noire et la relativité **à partir des données**, de l'échelle du
Système solaire à celle de la galaxie. Cosmos reprend la même démarche à l'échelle de l'univers.

## Lancer les calculs

```bash
py -3 -m venv .venv
.venv/Scripts/python -m pip install -r calculs/requirements.txt
bash calculs/telecharger_donnees.sh
PYTHONIOENCODING=utf-8 .venv/Scripts/python calculs/ajustement_bao_sn.py
```
