
# Selenium-Python Test Suite

[![CI Status](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml/badge.svg)](https://github.com/avshalombegler/selenium-python/actions/workflows/ci.yml)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modern, maintainable test automation suite for https://the-internet.herokuapp.com.  
Built with **Page Object Model**, **pytest**, **Allure reporting**, **video recording**, and **GitHub Actions CI/CD**.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables-env)
- [Running tests locally](#running-tests-locally)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Allure Reports](#allure-reports-live)
- [Project layout](#project-layout)

## Features
- Clean POM architecture with `BasePage` and `PageManager`
- Parallel execution via `pytest-xdist`
- Allure reports with history & trends
- Automatic video recording (attached to Allure)
- Multi-browser support (Chrome & Firefox)
- Headless & headed mode
- GitHub Actions CI with matrix strategy
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
    ```
    git clone https://github.com/avshalombegler/selenium-python.git
    cd selenium-python
    ```

2. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

**Note:** Allure CLI requires separate installation (not available via pip).  
See installation guide: https://docs.qameta.io/allure/#_installing_a_commandline

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
    ```
    pytest
    ```

- Run all tests in parallel:
    ```
    pytest -n auto
    ```

- Run a specific test file:
    ```
    pytest .\tests\test_test_name.py
    ```

- Generate Allure results (add this flag to the pytest run command):
    ```
    --alluredir=reports/allure-results
    ```

- View Allure Report Locally:
    ```
    allure serve reports/allure-results
    ```

- Optional: generate a static HTML report (requires Allure CLI):
    ```
    allure generate reports/allure-results -o reports/allure-report
    ```

## GitHub Actions CI/CD
- Runs automatically on every push/PR to main
- Matrix strategy: Chrome + Firefox (headless)
- Parallel execution with pytest-xdist
- Artifacts: Allure results, videos, junit.xml
- Allure reports automatically deployed to GitHub Pages

## Allure Reports (Live)
Latest reports are published automatically to GitHub Pages:

🔹 **Chrome (Latest Run):** [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-only/build-chrome-19505868108/)  

📊 **Chrome (With History):** [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-with-history/build-chrome-19505868108/)  

🔹 **Firefox (Latest Run):** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-only/build-firefox-19505868108/)  

📊 **Firefox (With History):** [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-with-history/build-firefox-19505868108/)  

> Reports update automatically after each CI run.

## Project layout
```
selenium-python/
├── .github/
│    └── workflows/ci.yml       # GitHub Actions workflow
├── config/env_config.py        # Loads .env variables
├── pages/                      # Page Object Model classes
│    ├── base/                  # BasePage, PageManager
│    ├── common/                # Shared components
│    └── features/              # Page objects per feature
├── reports/                    # Allure results and artifacts
├── tests/                      # Test cases
├── utils/                      # Helpers (logging, video, etc.)
├── conftest.py                 # Fixtures, hooks, driver setup
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (gitignored)
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