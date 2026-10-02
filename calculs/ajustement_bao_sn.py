"""Q1 etape 1 — BAO DESI DR2 et supernovas Pantheon+, SANS fond diffus.

Mesure ce que BAO et supernovas disent seuls de l'energie noire.
Usage : PYTHONIOENCODING=utf-8 .venv/Scripts/python calculs/ajustement_bao_sn.py
"""
from pathlib import Path

from cosmo import DESI, SN, Z_MIN_SN, ajuster, chi2_bao, chi2_sn, penalite, sigma

H_RAYONNEMENT = 0.68   # sans CMB, h n'est pas contraint ; il ne sert qu'a fixer le rayonnement (effet < 0,1 %)

JEUX = {"BAO (DESI DR2)": (True, False), "SN (Pantheon+)": (False, True), "BAO + SN": (True, True)}


def chi2(bao, sn, om, w0, wa, alpha):
    h = H_RAYONNEMENT
    return (chi2_bao(om, h, w0, wa, alpha) if bao else 0) + (chi2_sn(om, h, w0, wa) if sn else 0)


def main():
    lignes = [
        "# Q1 — BAO DESI DR2 + Pantheon+, sans CMB",
        "",
        f"Données : {len(DESI[0])} mesures BAO, {len(SN[0])} supernovas (z > {Z_MIN_SN}, covariance stat+sys).",
        "Univers plat. Δχ² = χ²(ΛCDM) − χ²(w₀wₐ) ; 2 paramètres de plus → σ via χ² à 2 ddl.",
        "",
        "| Jeu | Ωm (ΛCDM) | χ² ΛCDM | Ωm, w₀, wₐ | χ² w₀wₐ | Δχ² | préférence |",
        "|---|---|---|---|---|---|---|",
    ]
    for nom, (bao, sn) in JEUX.items():
        lcdm = ajuster(lambda p: chi2(bao, sn, p[0], -1, 0, p[1]),
                       [[0.30, 30], [0.25, 28], [0.35, 32]], [(0.05, 0.7), (20, 40)])
        cpl = ajuster(lambda p: chi2(bao, sn, *p) + penalite(p[1], p[2]),
                      [[0.30, -1, 0, 30], [0.32, -0.8, -0.8, 30], [0.35, -0.6, -1.5, 30]],
                      [(0.05, 0.7), (-3, 1), (-5, 3), (20, 40)])
        delta = lcdm.fun - cpl.fun
        lignes.append(f"| {nom} | {lcdm.x[0]:.4f} | {lcdm.fun:.2f} | {cpl.x[0]:.3f}, {cpl.x[1]:.2f}, {cpl.x[2]:.2f} "
                      f"| {cpl.fun:.2f} | {delta:.2f} | {sigma(delta):.1f} σ |")
    texte = "\n".join(lignes) + "\n"
    (Path(__file__).parent / "resultats" / "q1_bao_sn.md").write_text(texte, encoding="utf-8")
    print(texte)


if __name__ == "__main__":
    main()
