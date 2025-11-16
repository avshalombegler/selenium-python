
# Selenium-Python Test Suite

This project is a Selenium-based test automation framework for testing web applications, specifically targeting https://the-internet.herokuapp.com.
It uses the Page Object Model (POM) pattern, Pytest for test execution, and Allure for reporting, with video recordings as attachment.

## Requirements

- Python 3.10+
- Git
- Chrome/Firefox browser
- WebDriver (managed by webdriver-manager)

## Installation

1. Clone the repository:

git clone https://github.com/avshalombegler/selenium-python.git
cd selenium-python

2. Create a virtual environment:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

    pip install -r requirements.txt

4. Set up environment variables: Create a .env file with:

    BASE_URL=
    BROWSER=
    SHORT_TIMEOUT=
    LONG_TIMEOUT=
    VIDEO_RECORDING=
    HEADLESS=
    MAXIMIZED=
    USERNAME=tomsmith
    PASSWORD=SuperSecretPassword!

## Running tests

- Run the full pytest suite: `pytest tests`

- Run a single test file: `pytest tests\test_test_name.py`

Note: The Allure CLI is not a Python package; install it from https://docs.qameta.io/allure/ if needed.

## CI/CD with GitHub Actions
Tests are automatically run on every push/pull request to `main` using GitHub Actions.

## Allure Reports
Access the latest Allure reports below (updated automatically after each successful run):

- **Chrome - Latest Only (current run only)**: [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest-only/build-chrome-19404512021/index.html)
- **Chrome - Latest with History**: [View Report](https://avshalombegler.github.io/selenium-python/chrome/latest/build-chrome-19404512021/index.html)
- **Firefox - Latest Only (current run only)**: [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest-only/build-firefox-19404512021/index.html)
- **Firefox - Latest with History**: [View Report](https://avshalombegler.github.io/selenium-python/firefox/latest/build-firefox-19404512021/index.html)

### Notes
- Reports are generated for Chrome and Firefox browsers separately.
- "Latest Only" shows results from the most recent run without historical trends.
- "Latest with History" includes merged data from previous runs for trend analysis.

## Project layout

selenium-python/
├── `.github/workflows/`
│    ├── `ci.yml` - GitHub Actions CI workflow configuration
├── `config/` 
│    ├── `env_config.py` - Configuration parameters
├── `pages/` - Page Object Model classes
│    ├── `base/` - Base page classes and page manager
│    ├── `common/` - Common page objects
│    ├── `features/` - Feature-specific page objects
├── `reports/` - Test run artifacts and Allure results
├── `tests/` - Test cases
├── `utils/` - Utilities and helpers
├── `conftest.py` - Pytest fixtures/hooks and session set
├── `pytest.ini` - Pytest configuration file
├── `.env` - Environment variables file
└── README.md

## How to extend

- Add new page objects to `pages/` and expose them via `page_manager.py`.
- Add new Pytest fixtures/hooks to `conftest.py` for shared setup (browser/session-scoped fixtures are helpful).

