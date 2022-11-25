#!/bin/bash

echo "Applying migrations..."
alembic upgrade head
echo "Migrations applied!"

#echo "Starting the application..."
#uvicorn application.web.main:app --reload --host 0.0.0.0

exec "$@"