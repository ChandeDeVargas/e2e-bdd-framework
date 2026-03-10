@echo off
echo ================================================
echo E2E BDD Framework - Test Execution
echo ================================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate

echo [1/3] Running all tests...
pytest tests/ -v --html=reports/test_report.html --self-contained-html

echo.
echo [2/3] Running BDD scenarios...
pytest features/ -v --html=reports/bdd_report.html --self-contained-html

echo.
echo [3/3] Running multi-browser tests...
pytest tests/test_multi_browser.py -v --browser chromium --browser firefox --browser webkit

echo.
echo ================================================
echo Test execution complete!
echo Reports available in: reports/
echo ================================================
pause