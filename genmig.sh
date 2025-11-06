#!/usr/bin/bash
# GENERATE MIGRATIONS

source venv/bin/activate && \
source .env && \
pw_migrate create --auto --auto-source=coriplus.models --directory=src/migrations --database="$DATABASE_URL" "$@"