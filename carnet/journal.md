# Journal

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
