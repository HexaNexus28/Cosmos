# DESI DR2 — préférence pour une énergie noire qui évolue

- **Sources** : [DESI DR2 BAO + supernovas (arXiv 2508.10514)](https://arxiv.org/pdf/2508.10514) ·
  [carte complète, avril 2026](https://www.cmu.edu/mcs/news-events/2026/0415-desi-survey) ·
  [Lyman-α DR2, juillet 2026](https://www.desi.lbl.gov/2026/07/30/new-desi-dr2-lyman-alpha-results-shed-light-on-dark-energy/)
- **Données publiques** : [CobayaSampler/bao_data](https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2)

## Ce qu'ils mesurent

Les oscillations acoustiques des baryons (BAO) : une distance caractéristique (~150 Mpc) figée dans
la répartition des galaxies, qui sert de règle étalon. Mesurée à 7 époques (z de 0,3 à 2,33), elle
donne D_M/r_d (distance transverse) et D_H/r_d (lié à H(z)) : l'histoire de l'expansion.

## Résultat annoncé

DR2 (3 premières années, ~2× DR1) préfère une énergie noire qui évolue à ~3 à 4 σ selon la
combinaison (BAO + CMB + un catalogue de supernovas). Le relevé de 5 ans est terminé (avril 2026) ;
premiers résultats complets attendus en 2027. L'observation continue jusqu'en 2028.

## Points faibles à garder en tête

- La significativité **dépend du catalogue de supernovas** (Pantheon+, Union3, DES-Y5).
- La solution préférée franchit w = −1 (« phantom crossing ») : difficile à obtenir avec une théorie
  physiquement saine. Possible artefact du paramétrage w₀–wₐ.
- Notre calcul maison (journal 2026-10-02) : BAO seul 1,7 σ, sans CMB.
