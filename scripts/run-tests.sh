#!/bin/bash

echo "Starting PostgreSQL..."
docker compose up -d --wait

echo "PostgreSQL is ready!"

pytest src

docker compose down