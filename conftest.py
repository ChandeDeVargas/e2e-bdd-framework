"""
Pytest Configuration and Fixtures
Global fixtures for E2E BDD testing with Playwright
"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from datetime import datetime
import os

# ============================================
# Browser Configuration (POO Pattern)
# ============================================

class BrowserConfig:
    """
    Browser configuration settings.
    
    Centralizes browser setup and configuration.
    """

    # Browser settings
    HEADLESS = False
    SLOW_MOW = 500 # milliseconds
    VIEWPORT = {"width": 1920, "height": 1080}

    # Timeouts
    DEFAULT_TIMEOUT = 30000 # 30 seconds
    NAVIGATION_TIMEOUT = 60000 # 60 seconds

    # Screenshots/Videos
    SCREENSHOT_DIR = "screenshots"
    VIDEO_DIR = "videos"

    @classmethod
    def get_browser_args(cls):
        """Get browser launch arguments"""
        return [
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]


# ============================================
# Playwright Fixtures
# ============================================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context.
    
    Sets viewport, user agent, and other context options.
    """
    return {
        **browser_context_args,
        "viewport": BrowserConfig.VIEWPORT,
        "record_video_dir": BrowserConfig.VIDEO_DIR,
        "record_video_size": BrowserConfig.VIEWPORT
    }

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """
    Create a new page for each test.
    
    Yields:
        Page: Playwright page instance
    """
    page = context.new_page()

    # Set default timeout
    page.set_default_timeout(BrowserConfig.DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(BrowserConfig.NAVIGATION_TIMEOUT)

    yield page

    # Cleanup
    page.close()

@pytest.fixture(scope="function")
def take_screenshot(page: Page, request):
    """
    Take screenshot on test failure.
    
    Automatically captures screenshot when test fails.
    """
    yield

    if request.node.rep_call.failed:
        # Create screenshots directory
        os.makedirs(BrowserConfig.SCREENSHOT_DIR, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        filename = f"{BrowserConfig.SCREENSHOT_DIR}/{test_name}_{timestamp}.png"

        # Take screenshot
        page.screenshot(path=filename, full_page=True)
        print(f"\nScreenshot saved: {filename}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Make test result available in fixtures.
    
    Allows fixtures to access test pass/fail status.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# ============================================
# Test Data Fixtures
# ============================================

@pytest.fixture(scope="session")
def test_config():
    """
    Load test configuration.
    
    Returns:
        dict: Test configuration settings
    """
    return {
        "base_url": "https://demo.playwright.dev/todomvc",
        "timeout": 30000,
        "headless": False
    }


# ============================================
# HTML Report Customization
# ============================================

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "E2E BDD Test Report - Playwright"


def pytest_configure(config):
    """Add custom metadata to report"""
    config._metadata = {
        "Project": "E2E BDD Framework",
        "Tester": "Chande De Vargas",
        "Framework": "Playwright + pytest-bdd",
        "Python Version": "3.13",
        "Test Type": "End-to-End BDD",
        "Browsers": "Chromium, Firefox, WebKit"
    }
# ============================================
# Test Data Fixtures (POO)
# ============================================

from test_data.todo_data import TodoTestData, TodoItem

@pytest.fixture
def todo_data():
    """
    Provide TodoTestData instance.
    
    Returns:
        TodoTestData: Test data provider
    """
    return TodoTestData()


@pytest.fixture
def sample_todos(todo_data):
    """
    Provide sample todo items.
    
    Returns:
        List[TodoItem]: Sample todos
    """
    return todo_data.create_sample_todos()


@pytest.fixture
def priority_todos(todo_data):
    """
    Provide priority todo items.
    
    Returns:
        List[TodoItem]: Priority todos
    """
    return todo_data.create_priority_todos()


@pytest.fixture
def mixed_todos(todo_data):
    """
    Provide mixed active/completed todos.
    
    Returns:
        List[TodoItem]: Mixed todos
    """
    return todo_data.create_mixed_todos(active_count=3, completed_count=2)

import os
import shutil

def pytest_sessionstart(session):
    if os.path.exists("reports"):
        shutil.rmtree("reports")

    os.makedirs("reports")
    
# ============================================
# Logging Fixtures
# ============================================

from utils.logger import test_logger

@pytest.fixture(autouse=True)
def log_test_info(request):
    """
    Automatically log test start/end.
    
    Runs for every test automatically.
    """
    test_name = request.node.name
    
    # Log test start
    test_logger.test_start(test_name)
    
    yield
    
    # Log test end
    if hasattr(request.node, 'rep_call'):
        status = "PASSED" if request.node.rep_call.passed else "FAILED"
    else:
        status = "PASSED"
    
    test_logger.test_end(test_name, status)