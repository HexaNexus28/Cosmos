"""Q1 etape 2 — on ajoute le fond diffus (CMB) : d'ou viennent les 3 a 4 sigma de DESI ?

Le CMB est utilise sous forme compressee (Planck 2018, Chen et al. 2019) : R, l_A, Omega_b h^2.
Il fixe la taille de la regle BAO (r_d) et la distance jusqu'a l'univers jeune.

Usage : PYTHONIOENCODING=utf-8 .venv/Scripts/python calculs/ajustement_cmb.py
"""
from pathlib import Path

from cosmo import (ajuster, alpha_physique, chi2_bao, chi2_cmb, chi2_sn, penalite, r_d, sigma, z_etoile)

JEUX = {
    "CMB seul": (False, True, False),
    "BAO + CMB": (True, True, False),
    "BAO + CMB + SN (Pantheon+)": (True, True, True),
}

# Valeurs publiees pour valider la chaine (DESI DR2 Results II, arXiv 2503.14738).
PUBLIE = {
    "BAO + CMB": "DESI : 3,1 σ",
    "BAO + CMB + SN (Pantheon+)": "DESI : 2,8 σ",
}


def chi2(jeu, om, h, ob_h2, w0, wa):
    bao, cmb, sn = jeu
    total = 0.0
    if bao:
        total += chi2_bao(om, h, w0, wa, alpha_physique(om, h, ob_h2))
    if cmb:
        total += chi2_cmb(om, h, ob_h2, w0, wa)
    if sn:
        total += chi2_sn(om, h, w0, wa)
    return total


BORNES_LCDM = [(0.2, 0.45), (0.55, 0.80), (0.018, 0.026)]
DEPARTS_LCDM = [[0.31, 0.68, 0.0224], [0.30, 0.69, 0.0223], [0.32, 0.67, 0.0225]]


def main():
    lignes = [
        "# Q1 — avec le fond diffus (CMB compressé, Planck 2018)",
        "",
        "| Jeu | ΛCDM : Ωm, H₀ | χ² ΛCDM | w₀wₐ : Ωm, H₀, w₀, wₐ | χ² w₀wₐ | Δχ² | préférence | publié |",
        "|---|---|---|---|---|---|---|---|",
    ]
    validation = []
    for nom, jeu in JEUX.items():
        lcdm = ajuster(lambda p: chi2(jeu, p[0], p[1], p[2], -1, 0), DEPARTS_LCDM, BORNES_LCDM)
        if not jeu[0] and not jeu[2]:
            # CMB seul : 3 nombres ne contraignent pas 5 parametres, pas de comparaison w0wa.
            om, h, ob = lcdm.x
            validation = [
                f"- CMB seul, ΛCDM : Ωm = {om:.4f}, H₀ = {100 * h:.2f}, Ω_b h² = {ob:.5f} "
                f"(Planck 2018 publie Ωm = 0,315 ± 0,007, H₀ = 67,4 ± 0,5)",
                f"- z* = {z_etoile(om, h, ob):.1f} (Planck : 1089,9) ; r_d = {r_d(om, h, ob):.2f} Mpc (Planck : 147,1)",
            ]
            lignes.append(f"| {nom} | {om:.4f}, {100 * h:.2f} | {lcdm.fun:.2f} | — | — | — | — | |")
            continue
        cpl = ajuster(lambda p: chi2(jeu, *p) + penalite(p[3], p[4]),
                      [x + [-1, 0] for x in DEPARTS_LCDM] + [[0.33, 0.66, 0.0224, -0.7, -1.0]],
                      BORNES_LCDM + [(-3, 1), (-5, 3)])
        delta = lcdm.fun - cpl.fun
        om, h, _, w0, wa = cpl.x
        lignes.append(
            f"| {nom} | {lcdm.x[0]:.4f}, {100 * lcdm.x[1]:.2f} | {lcdm.fun:.2f} "
            f"| {om:.3f}, {100 * h:.2f}, {w0:.2f}, {wa:.2f} | {cpl.fun:.2f} | {delta:.2f} "
            f"| {sigma(delta):.1f} σ | {PUBLIE.get(nom, '')} |"
        )
    texte = "\n".join(lignes + ["", "## Validation de la chaîne", ""] + validation) + "\n"
    (Path(__file__).parent / "resultats" / "q1_cmb.md").write_text(texte, encoding="utf-8")
    print(texte)


if __name__ == "__main__":
    main()
