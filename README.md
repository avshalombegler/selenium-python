# Selenium-Python Test Suite

[![CI Status](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modern, maintainable test automation suite for <https://the-internet.herokuapp.com>.  
Built with **Page Object Model**, **pytest**, **Allure reporting**, **video recording**, and **CI/CD** (GitHub Actions & Jenkins).

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables-env)
- [Running tests locally](#running-tests-locally)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Jenkins CI/CD](#jenkins-cicd)
- [Docker Support](#docker-support)
- [Allure Reports](#allure-reports)
- [Project layout](#project-layout)

## Features

- Clean POM architecture with `BasePage` and `PageManager`
- Parallel execution via `pytest-xdist`
- Allure reports with history & trends
- Automatic video recording (attached to Allure)
- Multi-browser support (Chrome & Firefox)
- Headless & headed mode
- GitHub Actions CI with matrix strategy
- Jenkins pipeline support with Docker
- Allure reports automatically published to GitHub Pages

## Requirements

### System Requirements

- **Python:** 3.10 or higher
- **Git:** Latest version
- **Browsers:**
  - Chrome 120+ / ChromeDriver (auto-managed)
  - Firefox 121+ / GeckoDriver (auto-managed)

### Python Dependencies

Key packages (see `requirements.txt` for full list):

- `selenium==4.15.0`
- `pytest==7.4.3`
- `allure-pytest==2.13.2`
- `pytest-xdist==3.5.0`
- `python-dotenv==1.0.0`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/avshalombegler/selenium-python.git
    cd selenium-python
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

**Note:** Allure CLI requires separate installation (not available via pip).  
See installation guide: <https://docs.qameta.io/allure/#_installing_a_commandline>

## Environment Variables (.env)

Create a .env file in the project root:

```env
# Application
BASE_URL=https://the-internet.herokuapp.com/

# Browser Configuration
BROWSER=chrome             # Options: chrome, firefox
HEADLESS=True              # Run without UI (CI default)
MAXIMIZED=False            # Maximize browser window

# Timeouts (seconds)
SHORT_TIMEOUT=3            # For quick operations
LONG_TIMEOUT=10            # For slow operations

# Features
VIDEO_RECORDING=True       # Record test execution

# Test Credentials (for demo site)
USERNAME=tomsmith
PASSWORD=SuperSecretPassword!
```

**⚠️ Note:** Never commit `.env` with real credentials. Use CI secrets for production.

## Running tests locally

- Run all tests (sequential):

    ```bash
    pytest
    ```

- Run all tests in parallel:

    ```bash
    pytest -n auto
    ```

- Run a specific test file:

    ```bash
    pytest .\tests\test_test_name.py
    ```

- Generate Allure results (add this flag to the pytest run command):

    ```bash
    --alluredir=reports/allure-results
    ```

- View Allure Report Locally:

    ```bash
    allure serve reports/allure-results
    ```

- Optional: generate a static HTML report (requires Allure CLI):

    ```bash
    allure generate reports/allure-results -o reports/allure-report
    ```

## GitHub Actions CI/CD

- Runs automatically on every push/PR to main
- Matrix strategy: Chrome + Firefox (headless)
- Parallel execution with pytest-xdist
- Artifacts: Allure results, videos, junit.xml
- Allure reports automatically deployed to GitHub Pages

## Jenkins CI/CD

### Prerequisites

- Jenkins 2.400+ with Docker support
- Docker installed on Jenkins agent
- Required Jenkins plugins:
  - Docker Pipeline
  - Allure Plugin
  - HTML Publisher Plugin

### Pipeline Features

- Multi-browser execution (Chrome & Firefox)
- Parallel test execution
- Allure report generation
- Video recording for failed tests
- Automatic artifact archiving
- Post-build notifications

### Running in Jenkins

1. Create a new Pipeline job in Jenkins
2. Configure SCM to point to your repository
3. Set "Script Path" to `Jenkinsfile`
4. Configure build triggers (e.g., Poll SCM, GitHub webhook)
5. Run the pipeline

### Pipeline Parameters

The Jenkinsfile supports the following parameters:

- `BROWSER`: Browser choice (chrome/firefox/both)
- `HEADLESS`: Run in headless mode (true/false)
- `PARALLEL_WORKERS`: Number of parallel workers (default: auto)

## Docker Support

### Dockerfile.jenkins

The project includes a custom Jenkins agent image with all dependencies:

- Python 3.10
- Chrome & ChromeDriver
- Firefox & GeckoDriver
- Allure CLI
- All Python dependencies

### docker-compose.yml

The project utilizes Docker Compose to orchestrate a complete CI/CD environment, including:

- **Jenkins**: Automated build and test execution server
- **Allure Server**: Backend service for storing and managing Allure test reports
- **Allure UI**: Web interface for viewing and analyzing Allure reports
- **Nginx**: Reverse proxy for routing requests to Allure services

### Ngrok Integration

Ngrok is used to create secure tunnels for external access to Allure reports, enabling remote viewing of test results without exposing internal services directly.

## Allure Reports

### Jenkins Allure Reports

Reports generated from Jenkins pipeline runs are hosted locally and can be accessed publicly via ngrok tunneling. These reports are populated through the Allure server backend, served via the Allure UI, and exposed externally using ngrok for secure remote access.

🔹 **Local Access:** [View Report](http://localhost:8080) (via Nginx reverse proxy to Allure UI)

🔹 **Public Access:** [Placeholder for Ngrok Public URL](https://x-y-z.ngrok-free.dev) (dynamic tunnel URL provided by ngrok)

### GitHub Actions Allure Reports

Latest reports are published automatically to GitHub Pages:

**Chrome:** 🔹[View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-only/build-chrome-19849391347/) **(Latest Run)**     📊 [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-with-history/build-chrome-19849391347/)**(With History):**

**Firefox:** 🔹**(Latest Run)** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-only/build-firefox-19849391347/) 📊 **(With History):** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-with-history/build-firefox-19849391347/)  

> Reports update automatically after each CI run.

🔹 **Chrome (Latest Run):** [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-only/build-chrome-19849391347/)  

📊 **Chrome (With History):** [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-with-history/build-chrome-19849391347/)  

🔹 **Firefox (Latest Run):** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-only/build-firefox-19849391347/)  

📊 **Firefox (With History):** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-with-history/build-firefox-19849391347/)  

> Reports update automatically after each CI run.

## Project layout

```text
selenium-python/
├── .github/
│    └── workflows/ci.yml                   # GitHub Actions workflow
├── config/env_config.py                    # Loads .env variables
├── pages/                                  # Page Object Model classes
│    ├── base/                              # BasePage, PageManager
│    ├── common/                            # Shared components
│    └── features/                          # Page objects per feature
├── pytest_plugins/                         # Modular pytest plugins
│    ├── browser_fixtures.py                # Browser/driver setup
│    ├── browser_helpers.py                 # Browser utilities
│    ├── directory_fixtures.py              # Directory management
│    ├── hooks.py                           # Pytest hooks
│    ├── recording_fixtures.py              # Video recording
│    └── test_fixtures.py                   # Test-level fixtures
├── reports/                                # Allure results and artifacts
├── tests/                                  # Test cases
├── utils/                                  # Helpers (logging, video, etc.)
├── conftest.py                             # Main conftest - registers plugins
├── pyproject.toml                          # Project configuration
├── .env                                    # Environment variables (gitignored)
├── requirements.txt
└── README.md
```

## How to Add New Tests

1. Create page object in pages/features/your_feature/your_page.py
2. Register it in pages/base/page_manager.py
3. Add test in tests/test_your_feature.py
4. (Optional) Add @pytest.mark.smoke or other markers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
