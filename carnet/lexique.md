# Lexique

Tout terme qui apparaît dans le carnet est défini ici. On complète au fur et à mesure.

## Lire l'alphabet grec

| Lettre | Nom (prononciation) | Ce qu'elle désigne ici |
|---|---|---|
| Λ, λ | lambda | Λ : la constante cosmologique (énergie du vide, constante dans le temps) |
| Ω, ω | oméga | Ω : part d'une composante dans l'univers. Ωm = matière (~31 %). ω minuscule : Ω × h² |
| σ | sigma | « Combien d'écarts-types » : la force d'un signal statistique (voir plus bas) |
| χ | khi (« ki ») | χ² (« khi deux ») : la mesure de l'écart entre un modèle et des données |
| τ | tau | Profondeur optique de la réionisation (voir plus bas) |
| α | alpha | Paramètre auxiliaire de nos calculs (α = c / (H₀ · r_d)) |
| π | pi | 3,14159… |
| Δ | delta | « Différence ». Δχ² = différence de χ² entre deux modèles |
| ν | nu | Neutrino (ων : part des neutrinos) |
| θ | thêta | Un angle (θ* : taille angulaire de la règle étalon dans le fond diffus) |

Les petits chiffres en indice se lisent « zéro », « a », etc. : w₀ = « w zéro », wₐ = « w a ».

## Le cosmos et ses mesures

**Fond diffus cosmologique (CMB, *Cosmic Microwave Background*)** — La plus vieille lumière de
l'univers. Pendant ~380 000 ans après le Big Bang, l'univers était un plasma opaque, comme l'intérieur
du Soleil : la lumière ne pouvait pas voyager. En refroidissant à ~3 000 K, les électrons se sont
liés aux noyaux, l'univers est devenu transparent, et cette lumière s'est libérée d'un coup. Elle nous
arrive aujourd'hui de toutes les directions, refroidie à 2,7 K par l'expansion (ondes radio /
micro-ondes). Ses minuscules variations (1 sur 100 000) sont une photographie de l'univers bébé :
Planck (satellite européen, 2009-2013) l'a cartographiée avec une précision extrême.

**Redshift (z, « décalage vers le rouge »)** — L'expansion étire la lumière en route. z mesure cet
étirement, donc la distance et l'époque : z = 0 aujourd'hui, z ≈ 1 il y a ~8 milliards d'années,
z* ≈ 1 090 pour le fond diffus.

**H₀ (« H zéro », constante de Hubble)** — Vitesse d'expansion actuelle : environ 70 km/s de plus
chaque fois qu'on s'éloigne d'un mégaparsec. h = H₀ / 100.

**Mpc (mégaparsec)** — 3,26 millions d'années-lumière.

**BAO (oscillations acoustiques des baryons)** — Dans le plasma primitif, des ondes sonores se sont
propagées puis figées au moment de la transparence. Elles ont laissé une distance préférée entre
galaxies, ~147 Mpc : r_d, la **règle étalon**. La mesurer à différents z donne l'histoire de l'expansion.

**Supernova de type Ia (SN)** — Explosion d'étoile naine blanche, de luminosité connue : une
**chandelle standard**. Sa luminosité apparente donne sa distance.

**Énergie noire** — Ce qui fait accélérer l'expansion (~69 % de l'univers). Décrite par w :
- **w = −1** : constante cosmologique Λ, ne change jamais.
- **w₀, wₐ** : w(a) = w₀ + wₐ(1 − a), où a = 1/(1+z) est la taille de l'univers relative à aujourd'hui.
  w₀ = valeur actuelle, wₐ = vitesse à laquelle elle change. DESI trouve w₀ > −1 et wₐ < 0 : une
  énergie noire qui s'affaiblit.

**ΛCDM (« lambda-CDM »)** — Le modèle standard : Λ (constante cosmologique) + CDM (*Cold Dark Matter*,
matière noire froide). w₀wₐCDM = même modèle avec une énergie noire qui évolue.

**τ (tau), profondeur optique de la réionisation** — Quelques centaines de millions d'années après le
Big Bang, les premières étoiles ont réionisé le gaz intergalactique : les électrons libérés ont
diffusé une partie de la lumière du fond diffus, comme un léger brouillard. τ mesure l'épaisseur de ce
brouillard (≈ 0,06 d'après la polarisation du fond diffus). Pourquoi c'est brûlant : τ est mal mesuré
et lié à d'autres paramètres ; si τ valait ~0,09, la tension entre DESI et le fond diffus se réduit et
la préférence pour une énergie noire qui évolue tombe de ~3 σ à ~1,5 σ
([PRL 2025](https://journals.aps.org/prl/abstract/10.1103/6r54-8lv4),
[arXiv 2504.16932](https://arxiv.org/abs/2504.16932)). Voir Q5.

## Les outils statistiques

**χ² (khi deux)** — Somme des écarts² entre modèle et données, pondérés par les erreurs. Plus petit =
meilleur ajustement.

**σ (sigma)** — Traduit la force d'une préférence en « nombre d'écarts-types » : 1 σ ≈ banal,
2 σ ≈ 1 chance sur 20 que ce soit un hasard, 3 σ ≈ 1 sur 370 (« indice »), **5 σ ≈ 1 sur 3,5 millions
(seuil de découverte en physique)**.

**Covariance** — Tableau qui dit comment les erreurs de mesures différentes sont liées entre elles. On
ne peut pas l'ignorer : deux mesures corrélées ne valent pas deux mesures indépendantes.

**Priors compressés du fond diffus (R, ℓ_A, Ω_b h²)** — Trois nombres qui résument ce que le fond
diffus dit de l'expansion, sans refaire tourner tout le code de Planck : R (distance jusqu'au fond
diffus × matière), ℓ_A (taille angulaire de la règle étalon dans le fond diffus), Ω_b h² (quantité de
matière ordinaire). Rapide, mais perd une partie de l'information (lentilles, τ).
