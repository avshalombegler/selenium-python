
# Selenium-Python Test Suite

This project is a Selenium-based test automation framework for testing web applications, specifically targeting https://the-internet.herokuapp.com.
It uses the Page Object Model (POM) pattern, Pytest for test execution, Allure for reporting, and custom logging for debugging.

## Project status

- Minimal, runnable pytest-based Selenium tests are included under `tests/`.
- Page objects live in the `pages/` package and are coordinated by `page_manager.py`.
- Test configuration and fixtures are provided in `conftest.py`.
- Allure results and a generated HTML report live under `reports/`.

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

    SHORT_TIMEOUT=3
    LONG_TIMEOUT=10

## Running tests

- Run the full pytest suite: `pytest tests`

- Run a single test file: `pytest tests\test_name.py`

- View Allure report: `allure serve reports`

- Then generate the HTML report (requires Allure CLI installed separately):
`allure generate reports/allure-results -o reports/allure-report`

Note: The Allure CLI is not a Python package; install it from https://docs.qameta.io/allure/ if needed.

## CI/CD with GitHub Actions
Tests are automatically run on every push/pull request to `main` using GitHub Actions.

## Allure Reports
Test reports are published to GitHub Pages after each CI run on the `main` branch:
- Latest report: https://avshalombegler.github.io/selenium-python/allure-report/build-<run_id>
- Find the Run ID in the [Actions tab](https://github.com/avshalombegler/selenium-python/actions).
- Note: Reports may take up to 10 minutes to appear after a successful run.

## Project layout

- `pages/` - Page Object Model classes
- `tests/` - Test cases
- `config/` - Configuration parameters
- `utils/` - Utilities (locators and helpers)
- `conftest.py` - Pytest fixtures and session setup
- `reports/` - Test run artifacts and Allure results

## Notes for maintainers

- Tests use the Page Object Model. Keep pages focused on element lookup and actions; assertions belong in tests.

## How to extend

- Add new page objects to `pages/` and expose them via `page_manager.py`.
- Add new fixtures to `conftest.py` for shared setup (browser/session-scoped fixtures are helpful).

## Contact

If you need help, open an issue or contact the repository owner.

