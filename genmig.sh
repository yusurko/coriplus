#!/usr/bin/bash
# GENERATE MIGRATIONS

source venv/bin/activate && \
source .env && \
case "$1" in
    ("+") pw_migrate create --auto --auto-source=coriplus.models --directory=src/migrations --database="$DATABASE_URL" "${@:2}" ;;
    ("@") pw_migrate migrate --directory=src/migrations --database="$DATABASE_URL" "${@:2}" ;;
    (\\) pw_migrate rollback --directory=src/migrations --database="$DATABASE_URL" "${@:2}" ;; 
esac
