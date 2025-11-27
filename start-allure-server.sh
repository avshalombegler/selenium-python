#!/bin/bash

echo "Starting Allure Server..."

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

# Start simple HTTP server to serve reports
echo "Starting HTTP server on port 5050..."
cd /app/reports
python3 -m http.server 5050