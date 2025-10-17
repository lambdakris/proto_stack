#!/bin/bash


# Database migration script using Flyway
# Usage: ./scripts/migrate.sh [command]
# Commands: migrate, info, validate, undo (not supported in Community), clean


COMMAND=${1:-migrate}

echo "Running Flyway migration: $COMMAND"


# Ensure PostgreSQL is running
docker compose up -d postgres

# Wait for PostgreSQL to be healthy
echo "Waiting for PostgreSQL to be ready..."
while ! docker compose exec postgres pg_isready -U postgres >/dev/null 2>&1; do
    sleep 1
done

echo "PostgreSQL is ready. Running Flyway $COMMAND..."

case $COMMAND in
    "migrate")
        docker compose run --rm flyway -url=jdbc:postgresql://postgres:5432/postgres -user=postgres -password=postgres migrate
        ;;
    "info")
        docker compose run --rm flyway -url=jdbc:postgresql://postgres:5432/postgres -user=postgres -password=postgres info
        ;;
    "validate")
        docker compose run --rm flyway -url=jdbc:postgresql://postgres:5432/postgres -user=postgres -password=postgres validate
        ;;
    "clean")
        docker compose run --rm flyway -url=jdbc:postgresql://postgres:5432/postgres -user=postgres -password=postgres clean
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Available commands: migrate, info, validate, clean"
        exit 1
        ;;
esac

echo "Flyway $COMMAND completed."