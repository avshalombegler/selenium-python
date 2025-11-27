import os
import shutil
import subprocess
import tarfile
import logging
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BASE_DIR = Path("/app")
PROJECTS_DIR = BASE_DIR / "projects"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist at startup
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
logger.info(f"Initialized directories - Projects: {PROJECTS_DIR}, Reports: {REPORTS_DIR}")


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
    logger.info(f"Attempting to serve report: {report_path}, exists: {report_path.exists()}")
    if report_path.exists():
        return send_from_directory(REPORTS_DIR / project_name, "index.html")
    return jsonify({"error": "Report not found"}), 404


@app.route("/reports/<project_name>/latest")
@app.route("/reports/<project_name>/latest/")
def serve_latest_report(project_name):
    """Serve the latest report"""
    report_path = REPORTS_DIR / project_name / "index.html"
    logger.info(f"Attempting to serve latest report: {report_path}, exists: {report_path.exists()}")
    if report_path.exists():
        return send_from_directory(REPORTS_DIR / project_name, "index.html")
    return jsonify({"error": "Report not found"}), 404


@app.route("/reports/<project_name>/<path:filename>")
def serve_report_files(project_name, filename):
    """Serve report static files"""
    report_dir = REPORTS_DIR / project_name
    if report_dir.exists():
        try:
            return send_from_directory(report_dir, filename)
        except Exception as e:
            logger.error(f"Error serving file {filename}: {e}")
            return jsonify({"error": "File not found"}), 404
    return jsonify({"error": "File not found"}), 404


@app.route("/api/upload/<project_name>", methods=["POST"])
def upload_results(project_name):
    """Receive and process test results"""
    try:
        logger.info(f"Upload request for project: {project_name}")
        build_id = request.args.get("buildId", "unknown")

        # Create project directories
        project_dir = PROJECTS_DIR / project_name
        results_dir = project_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file
        upload_file = results_dir / f"allure-results-{build_id}.tar.gz"
        upload_file.write_bytes(request.data)
        logger.info(f"Saved upload: {upload_file.name}, size: {upload_file.stat().st_size} bytes")

        # Extract results
        with tarfile.open(upload_file, "r:gz") as tar:
            tar.extractall(results_dir)
            logger.info(f"Extracted files: {tar.getnames()}")

        # Generate report
        report_dir = REPORTS_DIR / project_name
        report_dir.mkdir(parents=True, exist_ok=True)

        # Copy history if exists
        history_src = report_dir / "history"
        history_dst = results_dir / "allure-results" / "history"
        if history_src.exists():
            shutil.copytree(history_src, history_dst, dirs_exist_ok=True)

        # Generate Allure report
        result = subprocess.run(
            ["allure", "generate", str(results_dir / "allure-results"), "-o", str(report_dir), "--clean"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Generated report for {project_name}")
        logger.info(f"Allure output: {result.stdout}")
        
        # List generated files
        generated_files = list(report_dir.glob("*"))
        logger.info(f"Generated files in report dir: {[f.name for f in generated_files]}")

        # Clean up
        upload_file.unlink()

        return jsonify(
            {"status": "success", "project": project_name, "buildId": build_id, "reportUrl": f"/reports/{project_name}"}
        ), 200

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
