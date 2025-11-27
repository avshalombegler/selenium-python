import os
import shutil
import subprocess
import tarfile
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

BASE_DIR = Path("/app")
PROJECTS_DIR = BASE_DIR / "projects"
REPORTS_DIR = BASE_DIR / "reports"


@app.route("/")
def index() -> str:
    """List all available projects and reports"""
    projects = []
    if REPORTS_DIR.exists():
        for project_dir in REPORTS_DIR.iterdir():
            if project_dir.is_dir():
                projects.append({"name": project_dir.name, "url": f"/reports/{project_dir.name}"})

    html = "<h1>Allure Server</h1><h2>Available Reports:</h2><ul>"
    for project in projects:
        html += f'<li><a href="{project["url"]}">{project["name"]}</a></li>'
    html += "</ul>"
    return html


@app.route("/reports/<project_name>")
@app.route("/reports/<project_name>/")
def serve_report(project_name):
    """Serve the report index"""
    report_path = REPORTS_DIR / project_name / "index.html"
    if report_path.exists():
        return send_from_directory(REPORTS_DIR / project_name, "index.html")
    return jsonify({"error": "Report not found"}), 404


@app.route("/reports/<project_name>/<path:filename>")
def serve_report_files(project_name, filename):
    """Serve report static files"""
    report_dir = REPORTS_DIR / project_name
    if report_dir.exists():
        return send_from_directory(report_dir, filename)
    return jsonify({"error": "File not found"}), 404


@app.route("/api/upload/<project_name>", methods=["POST"])
def upload_results(project_name):
    """Receive and process test results"""
    try:
        build_id = request.args.get("buildId", "unknown")

        # Create project directories
        project_dir = PROJECTS_DIR / project_name
        results_dir = project_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file
        upload_file = results_dir / f"allure-results-{build_id}.tar.gz"
        request.data and upload_file.write_bytes(request.data)

        # Extract results
        with tarfile.open(upload_file, "r:gz") as tar:
            tar.extractall(results_dir)

        # Generate report
        report_dir = REPORTS_DIR / project_name
        report_dir.mkdir(parents=True, exist_ok=True)

        # Copy history if exists
        history_src = report_dir / "history"
        history_dst = results_dir / "allure-results" / "history"
        if history_src.exists():
            shutil.copytree(history_src, history_dst, dirs_exist_ok=True)

        # Generate Allure report
        subprocess.run(
            ["allure", "generate", str(results_dir / "allure-results"), "-o", str(report_dir), "--clean"], check=True
        )

        # Clean up
        upload_file.unlink()

        return jsonify(
            {"status": "success", "project": project_name, "buildId": build_id, "reportUrl": f"/reports/{project_name}"}
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
