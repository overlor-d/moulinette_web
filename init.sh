#!/bin/bash

source ./init_scripts/var.sh

if [ -e ./venv ]
then
    echo "Le dossier existe"
else
    echo "Le dossier n'existe pas il va être crée"
    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
fi


if [ -e ./data ]
then
    echo "Dossier de data déjà crée"
else
    echo "Création du lien symbolique à partir du chemin fourni dans les variables"
    ln -s $path_data data
fi