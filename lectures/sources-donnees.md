# Où récupérer les données de l'univers

Réponse à la question « comment récupérer les données ? » : presque tout ce que les grands
instruments mesurent devient **public**, après une période réservée aux équipes. Accès en Python
via [astroquery](https://astroquery.readthedocs.io/) pour la plupart.

## Archives publiques

| Archive | Ce qu'on y trouve | Questions du carnet |
|---|---|---|
| [DESI](https://data.desi.lbl.gov/) | Spectres de millions de galaxies (DR1 public), mesures BAO | Q1 |
| [Planck Legacy Archive](https://pla.esac.esa.int/) | Cartes du fond diffus, vraisemblances | Q1, Q5 |
| [Pantheon+](https://github.com/PantheonPlusSH0ES/DataRelease), [DES-SN5YR](https://github.com/des-science/DES-SN5YR) | Supernovas de type Ia | Q1, Q2 |
| [Gaia DR3](https://gea.esac.esa.int/archive/) | Position et mouvement de 1,8 milliard d'étoiles | Q7 (trajectoire, galaxie) |
| [GWOSC](https://gwosc.org/) | Signaux bruts des ondes gravitationnelles (LIGO / Virgo / KAGRA) | Q6 (trous noirs), Q2 (sirènes standard) |
| [EHT](https://eventhorizontelescope.org/for-astronomers/data) | Données des images de trous noirs (M87*, Sgr A*) | Q6 |
| [MAST](https://mast.stsci.edu/) | Hubble, JWST, TESS | Q2 |
| [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) | Éphémérides du Système solaire | chapitre 0 (Kepler) |
| [arXiv astro-ph](https://arxiv.org/list/astro-ph/new) | Les articles, avant même leur publication | veille |

## Mesurer soi-même

- **Raie de l'hydrogène à 21 cm** : avec une clé radio logicielle (SDR, ~30-40 €) et une antenne
  cornet faite maison, des amateurs mesurent la **rotation de la Voie lactée**, donc la courbe de
  rotation qui a révélé la matière noire (carte 4 du chapitre 0). C'est la façon la plus directe
  d'obtenir une donnée cosmique avec ses propres instruments.
- Petit télescope + capteur : courbes de lumière de supernovas proches ou d'exoplanètes en transit.
