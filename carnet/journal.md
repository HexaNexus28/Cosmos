# Journal

## 2026-10-03 — Q9 : les systématiques de Pantheon+ face à DESI DR2 (10/14, en cours)

**Nouveauté vérifiée avant de lancer** : 2409.18668 traite DESI 2024 avec des systématiques
simulées, sans σ par systématique. Personne n'a utilisé les 14 matrices officielles contre DR2.

**Ce qu'on a appris sur les données elles-mêmes**
- Les 14 fichiers `sytematic_groupings` ne se décomposent PAS en stat + systématique : somme des
  traces 9,2 contre 6,3 au total ; un terme commun (rang ~95, valeur propre −0,094) absent de
  STATONLY. BS21/C11/G10/SCATTERMOD sont des modèles de dispersion ALTERNATIFS, pas additifs.
  MASSSTEP, MWCOLORLAW, MWEBV, JLA_SALT2, ZSHIFT ont tous λ₁ = 0,051 vs STATONLY : c'est le terme commun.
- Méthode retenue (v2, `q9b_systematiques_differentiel.py`) : S_k = fichier_k − fichier_ref
  (le terme commun s'annule), puis le PIRE décalage à 1 σ qu'autorise S_k (projection du gradient
  de Δχ² par rapport aux magnitudes). Prédiction au 1er ordre, puis vrai réajustement à ±1, ±2.
- Test « retrait » abandonné : il exigerait une décomposition additive que les fichiers n'offrent pas.

**Validation**
- Référence BAO + CMB compressé + Pantheon+ : 2,27 σ (= étape 2). ✓
- Contrôle positif : SN z < 0,1 décalées de −0,05 / +0,05 mag → 1,14 σ / 5,99 σ. Le code réagit. ✓
- Direction identique avec les deux références (stabilité 0,99-1,00) pour toutes les systématiques testables.

**Résultats (pire décalage, de −2 à +2 écarts-types de la systématique)**

| Systématique | Ce que c'est | Préférence | Décalage typique | Part à z < 0,1 |
|---|---|---|---|---|
| **CALIB** | étalonnage photométrique | **1,70 → 2,84 σ** | 5,6 mmag | 47 % |
| **JLA_SALT2** | modèle de standardisation SALT2 | **1,90 → 2,66 σ** | 3,2 mmag | 34 % |
| **MWEBV** | poussière de la Voie lactée | **1,95 → 2,59 σ** | 5,6 mmag | 75 % |
| HSTCALSPEC | étoiles de référence de Hubble | 2,16 → 2,38 σ | 7,5 mmag | 24 % |
| MWCOLORLAW | loi de rougissement galactique | 2,16 → 2,38 σ | 2,8 mmag | 69 % |
| CSP_RECAL | réétalonnage des SN proches CSP | 2,19 → 2,35 σ | 3,8 mmag | 94 % |
| BS21, C11, G10 | modèles de dispersion | 2,20 → 2,33 σ | 6-28 mmag | 39-47 % |
| MASSSTEP | correction masse de l'hôte | 2,27 σ (aucun effet) | 3,1 mmag | 40 % |

**Lecture provisoire** : aucune systématique seule, à ±2 écarts-types, ne fabrique le signal
(max 2,84 σ) ni ne l'efface (min 1,70 σ). Les trois qui comptent sont l'étalonnage, SALT2 et la
poussière galactique — pas le réétalonnage CSP, pourtant concentré à 94 % sur les SN proches.
Les modèles de dispersion, les plus gros en amplitude, sont sans effet : ils secouent les SN une à
une sans tendance avec la distance.

**Interrompu** par manque de mémoire du PC : restent SCATTERMOD, SPECEFF, VPEC, ZSHIFT (le script
reprend où il s'est arrêté).

## 2026-10-02 (suite) — Q1 étape 2 : ajout du fond diffus

**Fait**
- Physique et données regroupées dans `calculs/cosmo.py` (une seule implémentation des équations).
- Fond diffus sous forme compressée : Planck 2018 TT,TE,EE+lowE, cas ΛCDM, table I de
  [Chen, Huang & Wang 2019](https://arxiv.org/abs/1808.05724) : R = 1,7502 ± 0,0046,
  ℓ_A = 301,471 ± 0,090, Ω_b h² = 0,02236 ± 0,00015, et leurs corrélations.
- r_d calculé (formule d'Aubourg et al. 2015) au lieu d'être laissé libre.

**Validation de la chaîne**
- CMB seul, ΛCDM : Ωm = 0,3163, H₀ = 67,33 — Planck publie 0,315 ± 0,007 et 67,4 ± 0,5. ✓
- z* = 1090,7 (Planck 1089,9) ; r_d = 146,97 Mpc (Planck 147,1, écart 0,1 %). ✓
- Piège trouvé et corrigé : la formule de z* doit utiliser le coefficient **0,0738** de Chen et al.
  (celui avec lequel les priors ont été construits), pas le 0,0783 de Hu & Sugiyama (z* = 1092,0).

**Résultat** (`calculs/resultats/q1_cmb.md`)

| Données | ΛCDM : Ωm, H₀ | w₀, wₐ | Préférence | DESI publie |
|---|---|---|---|---|
| BAO + CMB | 0,300, 68,5 | −0,44, −1,67 | 2,4 σ | 3,1 σ |
| BAO + CMB + Pantheon+ | 0,302, 68,4 | −0,85, −0,52 | 2,3 σ | 2,8 σ |

**Lecture** : ajouter le fond diffus fait passer la préférence de 1,7 σ à 2,4 σ. Le fond diffus est
donc bien un des moteurs du signal. Notre valeur reste sous celle de DESI : nos priors compressés
n'ont que Planck (DESI combine Planck + ACT avec les lentilles) et perdent l'information sur τ.

**Prochaines étapes**
1. Vraisemblance CMB complète (CAMB + Cobaya) avec τ libre → retrouver ~3 σ, puis tester τ = 0,09 (Q5).
2. Remplacer Pantheon+ par Union3 et DES-Y5 (P1).
3. Ouvrir Q6-Q8 (trous noirs, trajectoire, données personnelles) à la demande de l'user.

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
