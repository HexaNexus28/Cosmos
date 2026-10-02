#!/usr/bin/env bash
# Retelecharge les donnees publiques officielles dans calculs/data (non versionne : ~32 Mo).
set -euo pipefail
mkdir -p "$(dirname "$0")/data"
cd "$(dirname "$0")/data"

DESI=https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2
curl -sfO "$DESI/desi_gaussian_bao_ALL_GCcomb_mean.txt"
curl -sfO "$DESI/desi_gaussian_bao_ALL_GCcomb_cov.txt"

PANTHEON="https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR"
curl -sf -o pantheonplus.dat "$PANTHEON/Pantheon%2BSH0ES.dat"
curl -sf -o pantheonplus_statsys.cov "$PANTHEON/Pantheon%2BSH0ES_STAT%2BSYS.cov"

ls -la
