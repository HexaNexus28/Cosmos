"""Physique et donnees partagees par les ajustements.

Univers plat ; energie noire w(a) = w0 + wa (1 - a) (CPL, parametrage de DESI) ;
LCDM = cas w0 = -1, wa = 0.
"""
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

DATA = Path(__file__).parent / "data"
C_KMS = 299792.458
T_CMB = 2.7255                       # K
OMEGA_NU_H2 = 0.06 / 93.14           # une espece massive, somme des masses = 0,06 eV
Z_MIN_SN = 0.01                      # sous z = 0,01, les vitesses propres des galaxies dominent


# --- expansion ------------------------------------------------------------------

def omega_r(om, h):
    """Rayonnement (photons + neutrinos), via l'egalite matiere-rayonnement (Chen et al. 2019)."""
    z_eq = 2.5e4 * om * h ** 2 * (T_CMB / 2.7) ** -4
    return om / (1 + z_eq)


def E(z, om, h, w0, wa):
    """H(z) / H0."""
    a = 1 / (1 + z)
    orad = omega_r(om, h)
    de = (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(orad * (1 + z) ** 4 + om * (1 + z) ** 3 + (1 - om - orad) * de)


Z_GRILLE = np.linspace(0, 2.5, 25001)


def distance_comobile(z, om, h, w0, wa):
    """D_C en unites de c/H0, pour z <= 2,5 (BAO, supernovas)."""
    dc = integrate.cumulative_trapezoid(1 / E(Z_GRILLE, om, h, w0, wa), Z_GRILLE, initial=0)
    return np.interp(z, Z_GRILLE, dc)


def r_d(om, h, ob_h2):
    """Horizon sonore au decouplage des baryons, en Mpc (ajustement d'Aubourg et al. 2015, precision 0,02 %)."""
    ocb_h2 = om * h ** 2 - OMEGA_NU_H2
    return 55.154 * np.exp(-72.3 * (OMEGA_NU_H2 + 0.0006) ** 2) / (ocb_h2 ** 0.25351 * ob_h2 ** 0.12807)


# --- donnees -------------------------------------------------------------------

def charger_desi():
    lignes = [l.split() for l in (DATA / "desi_gaussian_bao_ALL_GCcomb_mean.txt").read_text().splitlines()
              if l and not l.startswith("#")]
    z = np.array([float(l[0]) for l in lignes])
    valeur = np.array([float(l[1]) for l in lignes])
    type_ = [l[2] for l in lignes]
    cov = np.loadtxt(DATA / "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    return z, valeur, type_, np.linalg.inv(cov)


def lire_cov_pantheon(chemin):
    """Format Pantheon+ : premiere ligne N, puis les N x N elements a la suite."""
    brut = np.loadtxt(chemin)
    n = int(brut[0])
    return brut[1:].reshape(n, n)


def masque_pantheon():
    """Supernovas gardees (z > Z_MIN_SN), dans l'ordre du fichier : sert a couper les covariances."""
    entete = (DATA / "pantheonplus.dat").read_text().splitlines()[0].split()
    tab = np.genfromtxt(DATA / "pantheonplus.dat", skip_header=1, dtype=None, encoding=None)
    return np.array([r[entete.index("zHD")] for r in tab], dtype=float) > Z_MIN_SN


def charger_pantheon():
    entete = (DATA / "pantheonplus.dat").read_text().splitlines()[0].split()
    col = {nom: i for i, nom in enumerate(entete)}
    tab = np.genfromtxt(DATA / "pantheonplus.dat", skip_header=1, dtype=None, encoding=None)
    zhd = np.array([r[col["zHD"]] for r in tab], dtype=float)
    zhel = np.array([r[col["zHEL"]] for r in tab], dtype=float)
    mb = np.array([r[col["m_b_corr"]] for r in tab], dtype=float)
    cov = lire_cov_pantheon(DATA / "pantheonplus_statsys.cov")
    garde = zhd > Z_MIN_SN
    return zhd[garde], zhel[garde], mb[garde], np.linalg.inv(cov[np.ix_(garde, garde)])


# Fond diffus compresse : Planck 2018 TT,TE,EE+lowE, cas LCDM (Chen, Huang & Wang 2019, table I).
CMB_MOYENNE = np.array([1.7502, 301.471, 0.02236])          # R, l_A, Omega_b h^2
_CMB_SIGMA = np.array([0.0046, 0.0895, 0.00015])
_CMB_CORR = np.array([[1.00, 0.46, -0.66],
                      [0.46, 1.00, -0.33],
                      [-0.66, -0.33, 1.00]])
CMB_ICOV = np.linalg.inv(_CMB_CORR * np.outer(_CMB_SIGMA, _CMB_SIGMA))

DESI = charger_desi()
SN = charger_pantheon()


# --- vraisemblances (chi2) ----------------------------------------------------------

def chi2_bao(om, h, w0, wa, alpha):
    """alpha = c / (H0 r_d), sans dimension : les BAO seuls ne contraignent que ce produit."""
    z, valeur, type_, icov = DESI
    dm = alpha * distance_comobile(z, om, h, w0, wa)
    dh = alpha / E(z, om, h, w0, wa)
    modele = np.array([
        dm[i] if t == "DM_over_rs" else dh[i] if t == "DH_over_rs" else (z[i] * dm[i] ** 2 * dh[i]) ** (1 / 3)
        for i, t in enumerate(type_)
    ])
    r = valeur - modele
    return r @ icov @ r


def alpha_physique(om, h, ob_h2):
    return C_KMS / (100 * h) / r_d(om, h, ob_h2)


def chi2_sn(om, h, w0, wa, mb=None, icov=None):
    """Magnitude absolue et H0 sont degeneres : leur somme est marginalisee analytiquement.

    `mb` et `icov` remplacent les magnitudes et l'inverse de covariance publies (tests de
    systematiques) ; par defaut, les valeurs officielles.
    """
    zhd, zhel, mb0, icov0 = SN
    mb = mb0 if mb is None else mb
    icov = icov0 if icov is None else icov
    r = mb - 5 * np.log10((1 + zhel) * distance_comobile(zhd, om, h, w0, wa))
    b = icov.sum(axis=0) @ r
    return r @ icov @ r - b * b / icov.sum()


def z_etoile(om, h, ob_h2):
    """Redshift du decouplage des photons, formule de Hu & Sugiyama.

    Coefficient 0,0738 : celui de Chen et al. 2019 (eq. 9), avec lequel les priors CMB ont ete
    construits. Le 0,0783 de Hu & Sugiyama 1996 donne z* = 1092,0 au lieu de 1090,7.
    """
    om_h2 = om * h ** 2
    g1 = 0.0738 * ob_h2 ** -0.238 / (1 + 39.5 * ob_h2 ** 0.763)
    g2 = 0.560 / (1 + 21.1 * ob_h2 ** 1.81)
    return 1048 * (1 + 0.00124 * ob_h2 ** -0.738) * (1 + g1 * om_h2 ** g2)


def chi2_cmb(om, h, ob_h2, w0, wa):
    zs = z_etoile(om, h, ob_h2)
    dm = integrate.quad(lambda z: 1 / E(z, om, h, w0, wa), 0, zs, limit=200)[0]
    rb = 31500 * ob_h2 * (T_CMB / 2.7) ** -4
    rs = integrate.quad(lambda a: 1 / (a * a * E(1 / a - 1, om, h, w0, wa) * np.sqrt(3 * (1 + rb * a))),
                        1e-8, 1 / (1 + zs), limit=200)[0]
    r = np.array([np.sqrt(om) * dm, np.pi * dm / rs, ob_h2]) - CMB_MOYENNE
    return r @ CMB_ICOV @ r


# --- outils d'ajustement ---------------------------------------------------------------

def penalite(w0, wa):
    """w0 + wa < 0 : l'energie noire doit rester negligeable dans l'univers jeune."""
    return 0 if w0 + wa < 0 else 1e6 * (w0 + wa) ** 2 + 1e3


def ajuster(fonction, departs, bornes):
    meilleur = None
    for depart in departs:
        res = optimize.minimize(fonction, depart, method="L-BFGS-B", bounds=bornes)
        if meilleur is None or res.fun < meilleur.fun:
            meilleur = res
    return meilleur


def sigma(delta_chi2, ddl=2):
    """Equivalent gaussien bilateral d'un gain de chi2 obtenu avec `ddl` parametres de plus."""
    return stats.norm.isf(stats.chi2.sf(max(delta_chi2, 0), ddl) / 2)
