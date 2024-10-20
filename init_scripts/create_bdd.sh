#!/bin/bash

flask db init
flask db migrate -m "Init"
flask db upgrade

cd data
mkdir users exercices groupes