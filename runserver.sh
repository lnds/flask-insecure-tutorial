#!/bin/bash

echo "RUN SERVER"

bash ./wait-for-it.sh -h db -p 5432 -t 120

sleep 5

echo "INIT DB"
python3 init_db.py

sleep 5

echo "INIT SERVER"

python3 main.py 

