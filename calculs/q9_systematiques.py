"""Q9 — Laquelle des 14 systematiques officielles de Pantheon+ peut, a elle seule, fabriquer ou
effacer la preference de DESI DR2 pour une energie noire qui evolue ?

Combinaison : BAO DESI DR2 + fond diffus compresse (Planck 2018) + Pantheon+ (z > 0,01).
Reference : 2,3 sigma (etape 2, chaine validee).

Construction des fichiers (Brout et al. 2022) : chaque systematique psi est un DECALAGE des
distances, C_psi = sigma_psi * dmu_psi dmu_psi^T. On teste donc chaque systematique en deplacant
les supernovas le long de son motif dominant :
  - motif : vecteur propre dominant v_1 de (fichier_k - STATONLY), d'amplitude sqrt(lambda_1) ;
  - DECALAGE : magnitudes + a * sqrt(lambda_1) * v_1, a = -2, -1, +1, +2 ecarts-types
    -> la preference franchit-elle 2 ou 3 sigma ?
  - part du motif portee par les supernovas proches (z < 0,1).

Mesure du 2026-10-03 : les 14 fichiers ne se decomposent PAS en stat + systematique (somme des
traces 9,2 contre 6,3 au total ; un terme negatif commun, de rang ~95, valeur propre ~ -0,094).
D'ou : pas de test de RETRAIT (il exigerait cette decomposition), et un motif n'est retenu que si
lambda_1 depasse 3 fois ce terme parasite ; sinon il est marque non resolu.

Usage : cd calculs && PYTHONIOENCODING=utf-8 ../.venv/Scripts/python q9_systematiques.py
"""
import json
import time
from pathlib import Path

import numpy as np

from cosmo import (DATA, SN, ajuster, alpha_physique, chi2_bao, chi2_cmb, chi2_sn, lire_cov_pantheon,
                   masque_pantheon, penalite, sigma)

SYSTEMATIQUES = ["BS21", "C11", "CALIB", "CSP_RECAL", "G10", "HSTCALSPEC", "JLA_SALT2", "MASSSTEP",
                 "MWCOLORLAW", "MWEBV", "SCATTERMOD", "SPECEFF", "VPEC", "ZSHIFT"]
AMPLITUDES = [-2, -1, 1, 2]
Z_PROCHE = 0.1
TERME_PARASITE = 0.094        # valeur propre negative commune aux 14 fichiers (mesuree)
SEUIL_FIABILITE = 3           # lambda_1 doit depasser 3 x le terme parasite
SORTIE = Path(__file__).parent / "resultats"

BORNES_LCDM = [(0.2, 0.45), (0.55, 0.80), (0.018, 0.026)]
BORNES_CPL = BORNES_LCDM + [(-3, 1), (-5, 3)]


def chi2(p, mb, icov):
    om, h, ob, w0, wa = p
    return (chi2_bao(om, h, w0, wa, alpha_physique(om, h, ob)) + chi2_cmb(om, h, ob, w0, wa)
            + chi2_sn(om, h, w0, wa, mb=mb, icov=icov) + penalite(w0, wa))


def preference(mb, icov, depart_lcdm, depart_cpl):
    """Ajuste LCDM et w0wa, renvoie (delta_chi2, sigma, meilleur w0wa)."""
    lcdm = ajuster(lambda p: chi2([*p, -1, 0], mb, icov), [depart_lcdm], BORNES_LCDM)
    cpl = ajuster(lambda p: chi2(p, mb, icov), [depart_cpl, [*lcdm.x, -1, 0]], BORNES_CPL)
    delta = lcdm.fun - cpl.fun
    return delta, sigma(delta), cpl.x


def main():
    t0 = time.time()
    zhd, _, mb0, icov_total = SN
    garde = masque_pantheon()
    cov_stat = lire_cov_pantheon(DATA / "pantheonplus_statonly.cov")[np.ix_(garde, garde)]

    # Reference (doit redonner l'etape 2 : ~2,3 sigma)
    ref_delta, ref_sigma, ref_cpl = preference(mb0, icov_total, [0.302, 0.684, 0.0224], [0.311, 0.676, 0.0224, -0.85, -0.52])
    depart_lcdm, depart_cpl = [0.302, 0.684, 0.0224], list(ref_cpl)
    print(f"Reference : {ref_sigma:.2f} sigma (delta chi2 = {ref_delta:.2f})", flush=True)

    resultats = {"reference": {"delta_chi2": ref_delta, "sigma": ref_sigma}, "systematiques": {}}
    proche = zhd < Z_PROCHE
    for nom in SYSTEMATIQUES:
        d_k = lire_cov_pantheon(DATA / "pantheon_sys" / f"{nom}.cov")[np.ix_(garde, garde)] - cov_stat
        valeurs, vecteurs = np.linalg.eigh(d_k)
        lam, v = valeurs[-1], vecteurs[:, -1]
        positives = valeurs[valeurs > 0].sum()
        part_mode = lam / positives
        part_proche = float(np.sum(v[proche] ** 2))
        fiable = lam > SEUIL_FIABILITE * TERME_PARASITE
        typique = float(np.sqrt(lam / len(v)))      # decalage RMS par supernova, en magnitude
        base = {"lambda_1": float(lam), "decalage_typique_mag": typique, "fiable": bool(fiable),
                "part_variance_positive": float(part_mode), "part_mode_z_inf_0.1": part_proche}
        if not fiable:
            resultats["systematiques"][nom] = base
            print(f"{nom:11s} lambda_1 = {lam:.3f} < {SEUIL_FIABILITE * TERME_PARASITE:.2f} : non resolu", flush=True)
            continue

        decalages = {}
        for a in AMPLITUDES:
            d, s, x = preference(mb0 + a * np.sqrt(lam) * v, icov_total, depart_lcdm, depart_cpl)
            decalages[str(a)] = {"delta_chi2": d, "sigma": s, "w0": x[3], "wa": x[4]}
        resultats["systematiques"][nom] = {**base, "decalages": decalages}
        s_min = min(r["sigma"] for r in decalages.values())
        s_max = max(r["sigma"] for r in decalages.values())
        print(f"{nom:11s} motif {typique * 1000:5.1f} mmag/SN ({part_mode:4.0%} de la variance, {part_proche:4.0%} a z<0,1) | "
              f"decalage {s_min:.2f} -> {s_max:.2f} sigma | {time.time() - t0:5.0f} s", flush=True)
        (SORTIE / "q9_systematiques.json").write_text(json.dumps(resultats, indent=2), encoding="utf-8")

    (SORTIE / "q9_systematiques.json").write_text(json.dumps(resultats, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
