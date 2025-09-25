#!/bin/bash

# Database migration script using Liquibase
# Usage: ./scripts/migrate.sh [command]
# Commands: update, status, rollback-count <count>, validate

COMMAND=${1:-update}

echo "Running Liquibase migration: $COMMAND"

# Ensure PostgreSQL is running
docker compose up -d postgres

# Wait for PostgreSQL to be healthy
echo "Waiting for PostgreSQL to be ready..."
while ! docker compose exec postgres pg_isready -U postgres >/dev/null 2>&1; do
    sleep 1
done

echo "PostgreSQL is ready. Running Liquibase $COMMAND..."

case $COMMAND in
    "update")
        docker compose run --rm liquibase update
        ;;
    "status")
        docker compose run --rm liquibase status
        ;;
    "validate")
        docker compose run --rm liquibase validate
        ;;
    "rollback-count")
        if [ -z "$2" ]; then
            echo "Error: rollback-count requires a count parameter"
            echo "Usage: ./scripts/migrate.sh rollback-count <count>"
            exit 1
        fi
        docker compose run --rm liquibase rollback-count "$2"
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Available commands: update, status, validate, rollback-count <count>"
        exit 1
        ;;
esac

echo "Liquibase $COMMAND completed."