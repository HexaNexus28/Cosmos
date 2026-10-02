# Journal

## 2026-10-02 — Ouverture du carnet, premier calcul (Q1)

**Fait**
- Projet créé. Données officielles téléchargées : DESI DR2 BAO (13 mesures + covariance) et
  Pantheon+ (1 701 supernovas, covariance stat + sys).
- Script `calculs/ajustement_bao_sn.py` : univers plat, ΛCDM contre w₀wₐ, sans fond diffus.

**Validation de la chaîne** (avant toute interprétation)
- BAO seul, ΛCDM : Ωm = 0,2972 — DESI publie 0,2975 ± 0,0086. ✓
- Pantheon+ seul, ΛCDM : Ωm = 0,331 — Pantheon+ publie 0,334 ± 0,018. ✓

**Résultat** (`calculs/resultats/q1_bao_sn.md`)

| Données | Δχ² (ΛCDM − w₀wₐ) | Préférence pour une énergie noire qui évolue |
|---|---|---|
| BAO DESI DR2 | 4,66 | 1,7 σ |
| Pantheon+ | 0,30 | 0,2 σ |
| BAO + Pantheon+ | 4,83 | 1,7 σ |

**Lecture** : sans fond diffus, la préférence est modeste (1,7 σ) et Pantheon+ seul ne voit rien.
Les 3 à 4 σ publiés viennent donc de la combinaison avec le CMB et du choix du catalogue de
supernovas.

**Limites de ce calcul** : minimum de χ² seulement (pas d'échantillonnage MCMC, donc pas d'intervalles
de confiance) ; rayonnement fixé ; pas de CMB.

**Prochaine étape** : ajouter le fond diffus sous forme compressée (les « priors » CMB utilisés par
DESI), puis refaire le calcul avec Union3 et DES-Y5 à la place de Pantheon+.
