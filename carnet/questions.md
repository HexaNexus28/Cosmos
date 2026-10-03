# Questions ouvertes

Formulées pour qu'une donnée puisse y répondre. Statut : `ouverte`, `en cours`, `tranchée`.

## Q1 — L'énergie noire évolue-t-elle ? · en cours

La préférence de DESI pour une énergie noire qui évolue (3 à 4 σ publiés) survit-elle :
- à des **échantillons de supernovas indépendants** (Pantheon+, Union3, DES-Y5) ?
- au **retrait du fond diffus** (CMB) ?
- à un **autre paramétrage** que w₀–wₐ (le « phantom crossing » est-il un artefact de la forme imposée) ?

Premier résultat : `calculs/resultats/q1_bao_sn.md`. Voir le journal du 2026-10-02.

## Q2 — D'où vient la tension sur H₀ ? · ouverte

Univers jeune ≈ 67,4 km/s/Mpc, univers proche 70,4 (CCHP, TRGB) à 73,2 (SH0ES, Céphéides).
L'écart est-il dans l'échelle des distances locales ou dans la physique de l'univers jeune ?
Test possible : comparer les calibrations TRGB / JAGB / Céphéides sur les **mêmes** galaxies hôtes.

## Q3 — Pourquoi le vide pèse-t-il si peu ? · ouverte

La physique quantique prédit une énergie du vide ~10¹²⁰ fois trop grande. Quelles pistes font une
prédiction **testable** (et pas seulement une explication après coup) ? Point de départ : l'argument
anthropique de Weinberg (1987), seule prédiction réussie de la valeur de Λ à ce jour.

## Q5 — τ (profondeur optique de la réionisation) explique-t-il la préférence DESI ? · ouverte

Si τ ≈ 0,09 au lieu de 0,06, la préférence pour une énergie noire qui évolue tomberait de ~3 σ à
~1,5 σ (PRL 2025, arXiv 2504.16932, arXiv 2606.30903). Test : refaire Q1 avec une vraisemblance CMB
**complète** (CAMB + Cobaya), en laissant τ libre puis en le fixant à 0,06 et 0,09. Nos priors
compressés ne contiennent pas τ explicitement : ils ne peuvent pas répondre seuls.

## Q6 — Que nous apprennent les trous noirs sur l'univers ? · ouverte

Pistes : ondes gravitationnelles (GWOSC, données brutes publiques) comme « sirènes standard » pour
mesurer H₀ sans échelle des distances (lien avec Q2) ; masse de Sgr A* (déjà calculée au chapitre 0) ;
paradoxe de l'information. Pour l'user : élargir au-delà de l'énergie noire.

## Q7 — Où va-t-on : trajectoire de la Voie lactée et destin de l'univers · ouverte

Collision avec Andromède : plus « certaine » (Sawala et al. 2025 : ~50 % en 10 milliards d'années).
Destin final : dépend de l'énergie noire (Q1) — si w < −1 durablement, « Big Rip » ; si Λ, mort
thermique. Données : Gaia DR3 pour les mouvements locaux.

## Q8 — Peut-on obtenir nos propres données ? · ouverte

Voir `lectures/sources-donnees.md`. Piste concrète : mesurer la rotation de la Voie lactée à la raie
de l'hydrogène 21 cm avec une clé SDR (~30-40 €).

## Q9 — Une seule systématique de Pantheon+ peut-elle fabriquer ou effacer le signal DESI DR2 ? · en cours

Première question **nouvelle** du carnet (l'user veut comprendre quelque chose de non établi, pas
reproduire). Ce qui existe : 2409.18668 (DESI 2024, systématiques simulées par les auteurs, pas de σ
par systématique) ; 2502.04212 (le signal vient des SN à z < 0,1). Ce qui manque : DR2 + les 14
matrices officielles de Pantheon+ + l'effet de chacune sur la préférence en σ. Script :
`calculs/q9_systematiques.py`.

## Q4 — Q1 et Q2 sont-elles liées ? · ouverte

Une énergie noire qui évolue ou une énergie noire précoce peut-elle réduire **à la fois** la
préférence DESI et la tension sur H₀, ou chaque solution aggrave-t-elle l'autre ?
