#!/bin/bash

echo "Starting Allure Server with Flask API..."

# Use Railway's PORT environment variable or default to 5050
PORT=${PORT:-5050}

# Create initial project structure if it doesn't exist
if [ ! -d "/app/projects/default" ]; then
    mkdir -p /app/projects/default/results
    echo "Created default project structure"
fi

# Generate initial reports if results exist
for project in /app/projects/*; do
    if [ -d "$project/results" ] && [ "$(ls -A $project/results)" ]; then
        project_name=$(basename "$project")
        echo "Generating report for project: $project_name"
        allure generate "$project/results" -o "/app/reports/$project_name" --clean || true
    fi
done

# Start Flask application with Gunicorn
echo "Starting Flask API server on port ${PORT}..."
cd /app
exec gunicorn -w 2 -b 0.0.0.0:${PORT} --timeout 120 --access-logfile - --error-logfile - allure_server_api:app