"""Q1 — L'energie noire evolue-t-elle ? Ajustement DESI DR2 BAO + Pantheon+.

Deux modeles d'univers plat :
  LCDM   : w = -1 (constante cosmologique)
  w0waCDM: w(a) = w0 + wa (1 - a)   (parametrage CPL, celui de DESI)

Sans fond diffus (CMB) : on mesure ce que BAO et supernovas disent SEULS,
pour voir d'ou vient la preference publiee par DESI.

Usage : .venv/Scripts/python calculs/ajustement_bao_sn.py
"""
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

ICI = Path(__file__).parent
DATA = ICI / "data"
SORTIE = ICI / "resultats"

OMEGA_R = 8.5e-5          # rayonnement (photons + neutrinos), h ~ 0.68 : effet < 0,1 % ici
Z_MIN_SN = 0.01           # coupure standard : sous z = 0,01, les vitesses propres dominent

# --- donnees ---------------------------------------------------------------

def charger_desi():
    lignes = [l.split() for l in (DATA / "desi_gaussian_bao_ALL_GCcomb_mean.txt").read_text().splitlines()
              if l and not l.startswith("#")]
    z = np.array([float(l[0]) for l in lignes])
    valeur = np.array([float(l[1]) for l in lignes])
    type_ = [l[2] for l in lignes]
    cov = np.loadtxt(DATA / "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    return z, valeur, type_, np.linalg.inv(cov)


def charger_pantheon():
    entete = (DATA / "pantheonplus.dat").read_text().splitlines()[0].split()
    tab = np.genfromtxt(DATA / "pantheonplus.dat", skip_header=1, dtype=None, encoding=None)
    col = {nom: i for i, nom in enumerate(entete)}
    zhd = np.array([r[col["zHD"]] for r in tab], dtype=float)
    zhel = np.array([r[col["zHEL"]] for r in tab], dtype=float)
    mb = np.array([r[col["m_b_corr"]] for r in tab], dtype=float)

    brut = np.loadtxt(DATA / "pantheonplus_statsys.cov")
    n = int(brut[0])
    cov = brut[1:].reshape(n, n)

    garde = zhd > Z_MIN_SN
    cov = cov[np.ix_(garde, garde)]
    return zhd[garde], zhel[garde], mb[garde], np.linalg.inv(cov)


# --- cosmologie -------------------------------------------------------------

Z_GRILLE = np.linspace(0, 2.5, 25001)


def E(z, om, w0, wa):
    """H(z)/H0 pour un univers plat."""
    a = 1 / (1 + z)
    de = (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(om * (1 + z) ** 3 + OMEGA_R * (1 + z) ** 4 + (1 - om - OMEGA_R) * de)


def distance_comobile(z, om, w0, wa):
    """D_C(z) en unites c/H0, integree une fois sur la grille puis interpolee."""
    dc = integrate.cumulative_trapezoid(1 / E(Z_GRILLE, om, w0, wa), Z_GRILLE, initial=0)
    return np.interp(z, Z_GRILLE, dc)


# --- vraisemblances -----------------------------------------------------------

DESI = charger_desi()
SN = charger_pantheon()


def chi2_bao(om, w0, wa, alpha):
    """alpha = c / (H0 r_d) : seule combinaison que les BAO contraignent."""
    z, valeur, type_, icov = DESI
    dm = alpha * distance_comobile(z, om, w0, wa)
    dh = alpha / E(z, om, w0, wa)
    modele = np.array([
        dm[i] if t == "DM_over_rs" else dh[i] if t == "DH_over_rs" else (z[i] * dm[i] ** 2 * dh[i]) ** (1 / 3)
        for i, t in enumerate(type_)
    ])
    r = valeur - modele
    return r @ icov @ r


def chi2_sn(om, w0, wa):
    """Magnitude absolue M et H0 sont degeneres : on marginalise analytiquement leur somme."""
    zhd, zhel, mb, icov = SN
    mu = 5 * np.log10((1 + zhel) * distance_comobile(zhd, om, w0, wa))
    r = mb - mu
    a = r @ icov @ r
    b = icov.sum(axis=0) @ r
    c = icov.sum()
    return a - b * b / c


# --- ajustements -----------------------------------------------------------------

def ajuster(fonction, depart, bornes):
    meilleur = None
    for essai in depart:
        res = optimize.minimize(fonction, essai, method="L-BFGS-B", bounds=bornes)
        if meilleur is None or res.fun < meilleur.fun:
            meilleur = res
    return meilleur


def penalite(w0, wa):
    # w0 + wa < 0 : l'energie noire doit rester sous-dominante dans l'univers jeune
    return 0 if w0 + wa < 0 else 1e6 * (w0 + wa) ** 2 + 1e3


JEUX = {
    "BAO (DESI DR2)": (True, False),
    "SN (Pantheon+)": (False, True),
    "BAO + SN": (True, True),
}


def chi2_total(bao, sn, om, w0, wa, alpha):
    return (chi2_bao(om, w0, wa, alpha) if bao else 0) + (chi2_sn(om, w0, wa) if sn else 0)


def sigma_depuis_delta_chi2(delta, ddl):
    p = stats.chi2.sf(delta, ddl)
    return stats.norm.isf(p / 2)


def main():
    SORTIE.mkdir(exist_ok=True)
    lignes = []
    for nom, (bao, sn) in JEUX.items():
        lcdm = ajuster(lambda p: chi2_total(bao, sn, p[0], -1, 0, p[1]),
                       [[0.30, 30], [0.25, 28], [0.35, 32]], [(0.05, 0.7), (20, 40)])
        cpl = ajuster(lambda p: chi2_total(bao, sn, p[0], p[1], p[2], p[3]) + penalite(p[1], p[2]),
                      [[0.30, -1, 0, 30], [0.32, -0.8, -0.8, 30], [0.35, -0.6, -1.5, 30]],
                      [(0.05, 0.7), (-3, 1), (-5, 3), (20, 40)])
        delta = lcdm.fun - cpl.fun
        sig = sigma_depuis_delta_chi2(delta, 2)
        lignes.append((nom, lcdm, cpl, delta, sig))

    n_bao, n_sn = len(DESI[0]), len(SN[0])
    rapport = [
        "# Q1 — Résultat brut : BAO DESI DR2 + Pantheon+, sans CMB",
        "",
        f"Données : {n_bao} mesures BAO (DESI DR2), {n_sn} supernovas Pantheon+ (z > {Z_MIN_SN}, covariance stat+sys).",
        "Univers plat. Δχ² = χ²(ΛCDM) − χ²(w₀wₐ) ; 2 paramètres de plus → significativité via χ² à 2 ddl.",
        "",
        "| Jeu | Ωm (ΛCDM) | χ² ΛCDM | Ωm, w₀, wₐ (w₀wₐ) | χ² w₀wₐ | Δχ² | préférence |",
        "|---|---|---|---|---|---|---|",
    ]
    for nom, lcdm, cpl, delta, sig in lignes:
        rapport.append(
            f"| {nom} | {lcdm.x[0]:.4f} | {lcdm.fun:.2f} | {cpl.x[0]:.3f}, {cpl.x[1]:.2f}, {cpl.x[2]:.2f} "
            f"| {cpl.fun:.2f} | {delta:.2f} | {sig:.1f} σ |"
        )
    texte = "\n".join(rapport) + "\n"
    (SORTIE / "q1_bao_sn.md").write_text(texte, encoding="utf-8")
    print(texte)


if __name__ == "__main__":
    main()
