#!/bin/bash

mkdir -pv ~/.harvest/api/ ~/.harvest/cli/ -pv ~/.harvest/mongo

docker compose up -d --wait

python harvest/__main__.py

docker compose down
