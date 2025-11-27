import os
import shutil
import subprocess
import tarfile
import logging
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# Configure logging to stdout for Railway
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

logger.info("=" * 50)
logger.info("STARTING ALLURE SERVER")
logger.info("=" * 50)
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")
logger.info(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
logger.info("=" * 50)

app = Flask(__name__)

BASE_DIR = Path("/app")
PROJECTS_DIR = BASE_DIR / "projects"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist at startup
try:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"✓ Created/verified directories:")
    logger.info(f"  - Projects: {PROJECTS_DIR}")
    logger.info(f"  - Reports: {REPORTS_DIR}")
except Exception as e:
    logger.error(f"✗ Failed to create directories: {e}")

@app.route("/")
def index() -> str:
    """List all available projects and reports"""
    logger.info("Index page accessed")
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
    logger.info(f"Report requested: {project_name}")
    report_path = REPORTS_DIR / project_name / "index.html"
    if report_path.exists():
        return send_from_directory(REPORTS_DIR / project_name, "index.html")
    logger.warning(f"Report not found: {report_path}")
    return jsonify({"error": "Report not found"}), 404


@app.route("/reports/<project_name>/<path:filename>")
def serve_report_files(project_name, filename):
    """Serve report static files"""
    logger.debug(f"Serving file: {project_name}/{filename}")
    report_dir = REPORTS_DIR / project_name
    if report_dir.exists():
        return send_from_directory(report_dir, filename)
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
        request.data and upload_file.write_bytes(request.data)
        logger.info(f"Saved upload file: {upload_file}")

        # Extract results
        with tarfile.open(upload_file, "r:gz") as tar:
            tar.extractall(results_dir)
        logger.info("Extracted results")

        # Generate report
        report_dir = REPORTS_DIR / project_name
        report_dir.mkdir(parents=True, exist_ok=True)

        # Copy history if exists
        history_src = report_dir / "history"
        history_dst = results_dir / "allure-results" / "history"
        if history_src.exists():
            shutil.copytree(history_src, history_dst, dirs_exist_ok=True)
            logger.info("Copied history")

        # Generate Allure report
        logger.info("Generating Allure report...")
        subprocess.run(
            ["allure", "generate", str(results_dir / "allure-results"), "-o", str(report_dir), "--clean"], 
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Allure report generated successfully")

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
    logger.info("Health check endpoint called")
    port = os.environ.get("PORT", "NOT SET")
    return jsonify({
        "status": "healthy",
        "port": port,
        "projects_dir": str(PROJECTS_DIR),
        "reports_dir": str(REPORTS_DIR)
    }), 200


@app.before_request
def log_request():
    """Log all incoming requests"""
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
