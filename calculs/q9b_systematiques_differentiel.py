"""Q9, version 2 — le PIRE decalage qu'autorise chaque systematique.

Deux corrections par rapport a la v1 (q9_systematiques.py) :

1. Matrice de la systematique k par DIFFERENCE entre fichiers : S_k = fichier_k - fichier_ref.
   Les 14 fichiers partagent un terme parasite (rang ~95, absent de STATONLY) qui noyait les
   systematiques faibles ; il s'annule exactement dans la difference. Deux references presque
   vides (MASSSTEP, MWCOLORLAW, lambda_1 = 0,051 = le seul terme parasite) : le resultat doit etre
   le meme avec l'une ou l'autre. On garde la partie positive de S_k (une covariance est positive).

2. Pire direction au lieu du seul mode dominant (VPEC : mode dominant = 13 % de sa variance).
   g = d(delta chi2)/d(magnitudes), calcule aux meilleurs ajustements (theoreme de l'enveloppe) ;
   le decalage 1 sigma de S_k qui change le plus delta chi2 est d_k = S_k g / sqrt(g' S_k g),
   effet attendu au premier ordre : sqrt(g' S_k g). On le VERIFIE par un vrai reajustement a +-1, +-2.

Usage : cd calculs && PYTHONIOENCODING=utf-8 ../.venv/Scripts/python q9b_systematiques_differentiel.py
"""
import json
import time
from pathlib import Path

import numpy as np

from cosmo import DATA, SN, ajuster, distance_comobile, lire_cov_pantheon, masque_pantheon, sigma
from q9_systematiques import AMPLITUDES, BORNES_CPL, BORNES_LCDM, SYSTEMATIQUES, Z_PROCHE, chi2

REFERENCES = ["MASSSTEP", "MWCOLORLAW"]
SORTIE = Path(__file__).parent / "resultats" / "q9b_systematiques.json"


def ajustements(mb, icov):
    lcdm = ajuster(lambda p: chi2([*p, -1, 0], mb, icov), [[0.302, 0.684, 0.0224]], BORNES_LCDM)
    cpl = ajuster(lambda p: chi2(p, mb, icov), [[0.311, 0.676, 0.0224, -0.85, -0.52], [*lcdm.x, -1, 0]], BORNES_CPL)
    return [*lcdm.x, -1, 0], list(cpl.x), lcdm.fun - cpl.fun


def gradient_chi2_sn(params, mb, icov):
    """d chi2_SN / d mb au point `params`, avec la marginalisation analytique de l'offset."""
    zhd, zhel, _, _ = SN
    om, h, _, w0, wa = params
    r = mb - 5 * np.log10((1 + zhel) * distance_comobile(zhd, om, h, w0, wa))
    c1 = icov.sum(axis=0)
    return 2 * (icov @ r) - 2 * (c1 @ r) / c1.sum() * c1


def partie_positive(m):
    valeurs, vecteurs = np.linalg.eigh(m)
    valeurs = np.clip(valeurs, 0, None)
    return (vecteurs * valeurs) @ vecteurs.T, valeurs


def main():
    t0 = time.time()
    zhd, _, mb0, icov = SN
    garde = masque_pantheon()
    lire = lambda nom: lire_cov_pantheon(DATA / "pantheon_sys" / f"{nom}.cov")[np.ix_(garde, garde)]
    refs = {r: lire(r) for r in REFERENCES}

    p_lcdm, p_cpl, delta0 = ajustements(mb0, icov)
    g = gradient_chi2_sn(p_lcdm, mb0, icov) - gradient_chi2_sn(p_cpl, mb0, icov)
    print(f"Reference : {sigma(delta0):.2f} sigma (delta chi2 {delta0:.2f}) | |g| = {np.linalg.norm(g):.1f}", flush=True)

    # Reprise : un calcul interrompu (memoire, veille) ne refait pas les systematiques deja sauvegardees.
    resultats = json.loads(SORTIE.read_text(encoding="utf-8")) if SORTIE.exists() else {"systematiques": {}}
    resultats["reference"] = {"delta_chi2": delta0, "sigma": sigma(delta0)}
    restantes = [s for s in SYSTEMATIQUES if s not in resultats["systematiques"]]
    print(f"A calculer : {', '.join(restantes) or 'rien'}", flush=True)
    proche = zhd < Z_PROCHE
    for nom in restantes:
        f_k = lire(nom)
        effets, directions = {}, {}
        for ref in REFERENCES:
            if ref == nom:
                continue
            s_k, _ = partie_positive(f_k - refs[ref])
            effet = float(np.sqrt(max(g @ s_k @ g, 0)))
            effets[ref] = effet
            directions[ref] = s_k @ g / effet if effet > 0 else np.zeros_like(g)
        ref_ok = max(effets, key=effets.get)
        d = directions[ref_ok]
        stable = None
        if len(effets) == 2:
            a, b = directions.values()
            stable = float(abs(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30))

        verif = {}
        for a in AMPLITUDES:
            _, _, dl = ajustements(mb0 + a * d, icov)
            verif[str(a)] = {"delta_chi2": dl, "sigma": sigma(dl)}
        poids_proche = float(np.sum(d[proche] ** 2) / max(np.sum(d ** 2), 1e-30))
        resultats["systematiques"][nom] = {
            "effet_1sigma_premier_ordre_delta_chi2": effets[ref_ok], "effets_par_reference": effets,
            "stabilite_direction_deux_references": stable, "decalage_typique_mag": float(np.sqrt(np.mean(d ** 2))),
            "poids_z_inf_0.1": poids_proche, "verification": verif,
        }
        sig = [v["sigma"] for v in verif.values()]
        st = f"{stable:.2f}" if stable is not None else "—"
        print(f"{nom:11s} pire 1 sigma : delta chi2 {effets[ref_ok]:+6.2f} (1er ordre) | decalage {np.sqrt(np.mean(d ** 2)) * 1000:5.1f} mmag/SN "
              f"| z<0,1 {poids_proche:4.0%} | stabilite {st} | verifie {min(sig):.2f} -> {max(sig):.2f} sigma | {time.time() - t0:5.0f} s",
              flush=True)
        SORTIE.write_text(json.dumps(resultats, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
