"""Q1 etape 3 / Q5 — fond diffus COMPLET (CAMB + Cobaya) : le role de tau.

Contrairement a l'etape 2 (3 nombres compresses), on compare ici les spectres complets de Planck 2018
a ceux que CAMB calcule pour chaque univers, ce qui permet de laisser tau libre ou de le forcer.

Chaque configuration est un MINIMUM de chi2 (pas un MCMC) : suffisant pour comparer LCDM et w0wa.
Usage : PYTHONIOENCODING=utf-8 .venv/Scripts/python calculs/etape3_cmb_complet.py [A B C D E]
"""
import json
import sys
from pathlib import Path

from cobaya.run import run
from scipy import stats

ICI = Path(__file__).parent
PAQUETS = ICI / "cobaya_packages"
SORTIE = ICI / "resultats" / "etape3"

CMB_SANS_EE = {
    "planck_2018_lowl.TT": None,
    "planck_2018_highl_plik.TTTEEE_lite_native": None,
    "planck_2018_lensing.native": None,
}
CMB = {**CMB_SANS_EE, "planck_2018_lowl.EE_sroll2": None}
DESI = {"bao.desi_dr2": None}
PANTHEON = {"sn.pantheonplus": None}

# nom -> (vraisemblances, tau force ou None, compare-t-on w0wa ?)
CONFIGS = {
    "A": ("Fond diffus seul (validation)", CMB, None, False),
    "B": ("Fond diffus + DESI, tau libre", {**CMB, **DESI}, None, True),
    "C": ("Fond diffus + DESI, tau = 0,09", {**CMB, **DESI}, 0.09, True),
    "D": ("Sans polarisation grande echelle + DESI, tau libre", {**CMB_SANS_EE, **DESI}, None, True),
    "E": ("Fond diffus + DESI + Pantheon+, tau libre", {**CMB, **DESI, **PANTHEON}, None, True),
}


def parametres(tau_force, w0wa):
    p = {
        "logA": {"prior": {"min": 1.61, "max": 3.91}, "ref": 3.045, "proposal": 0.001, "drop": True},
        "As": {"value": "lambda logA: 1e-10*np.exp(logA)"},
        "ns": {"prior": {"min": 0.8, "max": 1.2}, "ref": 0.965, "proposal": 0.002},
        "theta_MC_100": {"prior": {"min": 0.5, "max": 10}, "ref": 1.04109, "proposal": 0.0002, "drop": True},
        "cosmomc_theta": {"value": "lambda theta_MC_100: 1.e-2*theta_MC_100", "derived": False},
        "H0": {"min": 20, "max": 100},
        "ombh2": {"prior": {"min": 0.005, "max": 0.1}, "ref": 0.0224, "proposal": 0.0001},
        "omch2": {"prior": {"min": 0.001, "max": 0.99}, "ref": 0.120, "proposal": 0.001},
        "tau": tau_force if tau_force is not None else
               {"prior": {"min": 0.01, "max": 0.8}, "ref": 0.055, "proposal": 0.003},
        "mnu": 0.06,
        "omegam": None,
    }
    if w0wa:
        p["w"] = {"prior": {"min": -3, "max": 1}, "ref": -0.8, "proposal": 0.05}
        p["wa"] = {"prior": {"min": -3, "max": 2}, "ref": -0.6, "proposal": 0.1}
    return p


def minimiser(nom, vraisemblances, tau_force, w0wa):
    info = {
        "packages_path": str(PAQUETS),
        "likelihood": vraisemblances,
        "theory": {"camb": {"extra_args": {
            "dark_energy_model": "ppf",          # permet de traverser w = -1 sans instabilite
            "num_massive_neutrinos": 1, "nnu": 3.044,
            "halofit_version": "mead", "lens_potential_accuracy": 1,
        }}},
        "params": parametres(tau_force, w0wa),
        "sampler": {"minimize": {"method": "iminuit", "best_of": 2}},
        "output": str(SORTIE / "chaines" / f"{nom}_{'w0wa' if w0wa else 'lcdm'}"),
        "force": True,
    }
    _, echantillonneur = run(info)
    m = echantillonneur.products()["minimum"]
    garder = ["H0", "omegam", "tau", "ombh2", "omch2", "ns", "w", "wa"]
    return {
        "chi2": float(m["chi2"]),
        "chi2_par_donnee": {k: float(v) for k, v in m.items() if k.startswith("chi2__")},
        "params": {k: float(m[k]) for k in garder if k in m},
    }


def sigma(delta):
    return float(stats.norm.isf(stats.chi2.sf(max(delta, 0), 2) / 2))


def main(choix):
    SORTIE.mkdir(parents=True, exist_ok=True)
    for cle in choix:
        titre, vraisemblances, tau_force, compare = CONFIGS[cle]
        print(f"\n===== {cle} — {titre} =====", flush=True)
        res = {"titre": titre, "lcdm": minimiser(cle, vraisemblances, tau_force, False)}
        if compare:
            res["w0wa"] = minimiser(cle, vraisemblances, tau_force, True)
            res["delta_chi2"] = res["lcdm"]["chi2"] - res["w0wa"]["chi2"]
            res["sigma"] = sigma(res["delta_chi2"])
        (SORTIE / f"{cle}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(res, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(CONFIGS))
