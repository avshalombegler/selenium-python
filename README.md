
# Selenium-Python Test Suite

A modern, maintainable test automation suite for https://the-internet.herokuapp.com  
Built with **Page Object Model**, **pytest**, **Allure reporting**, **video recording**, and **GitHub Actions CI/CD**.

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

- Python 3.10+
- Git
- Chrome/Firefox browser
- `webdriver-manager` handles drivers automatically

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

Note: Allure CLI is not installed via pip → install separately:
https://docs.qameta.io/allure/#_get_started

## Environment Variables (.env)

Create a .env file in the project root:
```
BASE_URL=https://the-internet.herokuapp.com/
BROWSER=chrome       # chrome or firefox
HEADLESS=True        # True/False
MAXIMIZED=False
SHORT_TIMEOUT=3
LONG_TIMEOUT=10
VIDEO_RECORDING=True
USERNAME=tomsmith
PASSWORD=SuperSecretPassword!
```

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
Latest reports are published automatically after every successful CI run:

- **Chrome - Latest Only (current run only)**: [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-only/build-chrome-19424355574/index.html)
- **Chrome - Latest with History**: [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest/build-chrome-19424355574/index.html)
- **Firefox - Latest Only (current run only)**: [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-only/build-firefox-19408184947/index.html)
- **Firefox - Latest with History**: [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest/build-firefox-19408184947/index.html)

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