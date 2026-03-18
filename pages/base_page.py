"""
Base Page Class
Parent class for all page objects (POO pattern)

All page objects inherit from BasePage to share common methods.
"""
from playwright.sync_api import Page, expect
from typing import Optional
from utils.logger import test_logger

class BasePage:
    """
    Base Page Object class.
    
    Provides common methods used across all pages.
    All page classes should inherit from this class.
    
    Attributes:
        page: Playwright Page instance
        timeout: Default timeout for actions
    """
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize BasePage.
        
        Args:
            page: Playwright Page instance
            timeout: Default timeout in milliseconds
        """
        self.page = page
        self.timeout = timeout

    # ============================================
    # Navigation Methods
    # ============================================

    def navigate_to(self, url: str) -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        """
        test_logger.action(f"Navigating to: {url}")
        self.page.goto(url, timeout=self.timeout)
        test_logger.info(f"\n✔ Navigated to: {url}")

    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.page.url

    def get_title(self) -> str:
        """
        Get page title.

        Returns:
            str: Page title
        """
        return self.page.title()

    # ============================================
    # Element Interaction Methods
    # ============================================

    def click(self, selector: str) -> None:
        """
        Click on element.
        
        Args:
            selector: Element selector
        """
        test_logger.action(f"Clicking on: {selector}")
        self.page.click(selector, timeout=self.timeout)
        test_logger.info(f"\n✔ Clicked on: {selector}")

    def fill(self, selector: str, text: str) -> None:
        """
        Fill input field.
        
        Args:
            selector: Input selector
            text: Text to fill
        """
        test_logger.action(f"Filling '{selector}' with text: {text}")
        self.page.fill(selector, text, timeout=self.timeout)
        test_logger.info(f"\n✔ Filled '{selector}' with text: {text}")

    def type_text(self, selector: str, text: str, delay: int = 100) -> None:
        """
        Type text with delay (simulates human typing).
        
        Args:
            selector: Input selector
            text: Text to type
            delay: Delay between keystrokes in ms
        """
        test_logger.action(f"Typing '{text}' into '{selector}'")
        self.page.type(selector, text, delay=delay, timeout=self.timeout)
        test_logger.info(f"\n✔ Typed: {text}")

    def press_key(self, selector: str, key: str) -> None:
        """
        Press keyboard key.
        
        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Escape')
        """
        test_logger.action(f"Pressing key: '{key}' on: {selector}")
        self.page.press(selector, key, timeout=self.timeout)
        test_logger.info(f"\n✔ Pressed key: '{key}' on: {selector}")

    def select_option(self, selector: str, value: str) -> None:
        """
        Select dropdown option.
        
        Args:
            selector: Select element selector
            value: Option value to select
        """
        test_logger.action(f"Selecting option: '{value}' in: {selector}")
        self.page.select_option(selector, value, timeout=self.timeout)
        test_logger.info(f"\n✔ Selected option: '{value}' in: {selector}")

    def check(self, selector: str) -> None:
        """
        Check checkbox.
        
        Args:
            selector: Checkbox selector
        """
        test_logger.action(f"Checking: {selector}")
        self.page.check(selector, timeout=self.timeout)
        test_logger.info(f"\n✔ Checked: {selector}")

    def uncheck(self, selector: str) -> None:
        """
        Uncheck checkbox.
        
        Args:
            selector: Checkbox selector
        """
        test_logger.action(f"Unchecking: {selector}")
        self.page.uncheck(selector, timeout=self.timeout)
        test_logger.info(f"\n✔ Unchecked: {selector}")

    # ============================================
    # Wait Methods
    # ============================================

    def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        """
        Wait for element to be in specific state.
        
        Args:
            selector: Element selector
            state: Element state ('visible', 'hidden', 'attached')
        """
        self.page.wait_for_selector(
            selector,
            state=state,
            timeout=self.timeout
        )
        test_logger.info(f"\n✔ Element {state}: {selector}")

    def wait_for_url(self, url_pattern: str) -> None:
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern to wait for
        """
        self.page.wait_for_url(url_pattern, timeout=self.timeout)
        test_logger.info(f"\n✔ URL matched: {url_pattern}")

    def wait_for_timeout(self, milliseconds: int) -> None:
        """
        Wait for fixed time.
        
        Args:
            milliseconds: Time to wait in ms
        """
        self.page.wait_for_timeout(milliseconds)

    # ============================================
    # Assertion Methods (using Playwright expect)
    # ============================================

    def assert_visible(self, selector: str) -> None:
        """
        Assert element is visible.
        
        Args:
            selector: Element selector
        """
        expect(self.page.locator(selector)).to_be_visible(
            timeout=self.timeout
        )
        test_logger.info(f"\n✔ Assertion passed: {selector} is visible")
    
    def assert_not_visible(self, selector: str) -> None:
        """
        Assert element is not visible.
        
        Args:
            selector: Element selector
        """
        expect(self.page.locator(selector)).not_to_be_visible(
            timeout=self.timeout
        )
        test_logger.info(f"\n✔ Assertion passed: {selector} is not visible")

    def assert_text(self, selector: str, expected_text: str) -> None:
        """
        Assert element contains text.
        
        Args:
            selector: Element selector
            expected_text: Expected text
        """
        expect(self.page.locator(selector)).to_contain_text(
            expected_text,
            timeout=self.timeout
        )
        test_logger.info(f"\n✔ Assertion passed: {selector} contains text: {expected_text}")

    def assert_url_contains(self, url_part: str) -> None:
        """
        Assert URL contains text.
        
        Args:
            url_part: Expected URL part
        """
        actual_url = self.page.url
        assert url_part in actual_url, \
            f"Expected URL to contain '{url_part}', but got '{actual_url}'"
        test_logger.info(f"\n✔ Assertion passed: URL contains: {url_part}")

    def get_text(self, selector: str) -> str:
        """
        Get element text content.
        
        Args:
            selector: Element selector
            
        Returns:
            str: Element text
        """
        text = self.page.locator(selector).text_content(timeout=self.timeout)
        test_logger.info(f"\n✔ Got text from: {selector}: {text}")
        return text

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """
        Get element attribute value.
        
        Args:
            selector: Element selector
            attribute: Attribute name
            
        Returns:
            str: Attribute value
        """
        value = self.page.locator(selector).get_attribute(
            attribute,
            timeout=self.timeout
        )
        test_logger.info(f"\n✔ Got attribute from: {selector}: {value}")
        return value

    def is_visible(self, selector: str) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: Element selector
            
        Returns:
            bool: True if visible, False otherwise
        """
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled.
        
        Args:
            selector: Element selector
            
        Returns:
            bool: True if enabled, False otherwise
        """
        return self.page.locator(selector).is_enabled()

    # ============================================
    # Screenshot Methods
    # ============================================

    def take_screenshot(self, filename: str, full_page: bool = True) -> None:
        """
        Take screenshot.
        
        Args:
            filename: Screenshot filename
            full_page: Capture full page or viewport only
        """
        self.page.screenshot(path=filename, full_page=full_page)
        test_logger.info(f"Screenshot saved: {filename}")
    
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def reload_page(self) -> None:
        """Reload current page"""
        self.page.reload()
        test_logger.info("Page reloaded")
    
    
    def go_back(self) -> None:
        """Navigate back"""
        self.page.go_back()
        test_logger.info("Navigated back")
    
    
    def go_forward(self) -> None:
        """Navigate forward"""
        self.page.go_forward()
        test_logger.info("Navigated forward")
        
    # ============================================
    # Additional Assertion Methods (IMPROVEMENTS)
    # ============================================

    def assert_element_count(self, selector: str, expected_count: int) -> None:
        """
        Assert exact number of elements.

        Useful for verifying lists, tables, etc.

        Args:
            selector: Element selector
            expected_count: Expected number of elements
        """
        actual_count = self.page.locator(selector).count()

        assert actual_count == expected_count, \
            f"Expected {expected_count} elements, but found {actual_count}"

        test_logger.info(f"Assertion passed: Found {expected_count} elements matching '{selector}'")


    def assert_url_exact(self, expected_url: str) -> None:
        """
        Assert exact URL match (not pattern).

        Different from assert_url_contains - this is exact.

        Args:
            expected_url: Exact expected URL
        """
        actual_url = self.page.url

        assert actual_url == expected_url, \
            f"Expected URL '{expected_url}', but got '{actual_url}'"

        test_logger.info(f"Assertion passed: URL is exactly '{expected_url}'")


    def assert_enabled(self, selector: str) -> None:
        """
        Assert element is enabled (clickable/editable).

        Useful for verifying that buttons or inputs are enabled.

        Args:
            selector: Element selector
        """
        is_enabled = self.page.locator(selector).is_enabled()

        assert is_enabled, \
            f"Element '{selector}' should be enabled but is disabled"

        test_logger.info(f"Assertion passed: Element '{selector}' is enabled")


    def assert_disabled(self, selector: str) -> None:
        """
        Assert element is disabled.

        Useful for verifying that certain fields are blocked.

        Args:
            selector: Element selector
        """
        is_disabled = not self.page.locator(selector).is_enabled()

        assert is_disabled, \
            f"Element '{selector}' should be disabled but is enabled"

        test_logger.info(f"Assertion passed: Element '{selector}' is disabled")


    def assert_checked(self, selector: str) -> None:
        """
        Assert checkbox/radio is checked.

        Args:
            selector: Checkbox/radio selector
        """
        is_checked = self.page.locator(selector).is_checked()

        assert is_checked, \
            f"Element '{selector}' should be checked but is not"

        test_logger.info(f"Assertion passed: Element '{selector}' is checked")


    def assert_not_checked(self, selector: str) -> None:
        """
        Assert checkbox/radio is NOT checked.

        Args:
            selector: Checkbox/radio selector
        """
        is_not_checked = not self.page.locator(selector).is_checked()

        assert is_not_checked, \
            f"Element '{selector}' should NOT be checked but is"

        test_logger.info(f"Assertion passed: Element '{selector}' is NOT checked")


    def assert_has_class(self, selector: str, class_name: str) -> None:
        """
        Assert element has specific CSS class.

        Useful for verifying visual states (active, disabled, error, etc).

        Args:
            selector: Element selector
            class_name: Expected CSS class
        """
        element_class = self.page.locator(selector).get_attribute("class") or ""

        assert class_name in element_class, \
            f"Element '{selector}' should have class '{class_name}' but has '{element_class}'"

        test_logger.info(f"Assertion passed: Element '{selector}' has class '{class_name}'")


    # ============================================
    # Scroll Methods (IMPROVEMENTS)
    # ============================================

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to make element visible.

        Useful when element is out of view.

        Args:
            selector: Element selector
        """
        self.page.locator(selector).scroll_into_view_if_needed()
        test_logger.info(f"Scrolled to element '{selector}'")


    def scroll_to_bottom(self) -> None:
        """
        Scroll to bottom of page.

        Useful for loading lazy-loaded content or viewing footers.
        """
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        test_logger.info("Scrolled to bottom of page")


    def scroll_to_top(self) -> None:
        """
        Scroll to top of page.

        Useful for returning to the top after scrolling down.
        """
        self.page.evaluate("window.scrollTo(0, 0)")
        test_logger.info("Scrolled to top of page")


    def scroll_by_pixels(self, x: int = 0, y: int = 500) -> None:
        """
        Scroll by specific pixel amount.

        Args:
            x: Horizontal pixels (default: 0)
            y: Vertical pixels (default: 500)
        """
        self.page.evaluate(f"window.scrollBy({x}, {y})")
        test_logger.info(f"Scrolled by {x}px horizontally and {y}px vertically")


    # ============================================
    # Enhanced Screenshot Methods (IMPROVEMENTS)
    # ============================================

    def take_screenshot_with_timestamp(self, name: str, full_page: bool = True) -> str:
        """
        Take screenshot with automatic timestamp.

        Useful for saving multiple screenshots without overwriting.

        Args:
            name: Base name for screenshot
            full_page: Capture full page or viewport only

        Returns:
            str: Path to saved screenshot
        """
        from datetime import datetime
        import os

        # Create a directory if not exist
        os.makedirs("screenshot", exist_ok=True)

        # Generate a name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"

        # Take screenshot
        self.page.screenshot(path=filename, full_page=full_page)
        test_logger.info(f"Screenshot saved: {filename}")

        return filename


    def take_element_screenshot(self, selector: str, filename: str) -> str:
        """
        Take screenshot of specific element only.

        Useful for capturing only a specific component.

        Args:
            selector: Element selector
            filename: Screenshot filename

        Returns:
            str: Path to saved screenshot
        """
        import os
        os.makedirs("screenshots", exist_ok=True)

        filepath = f"screenshots/{filename}"
        self.page.locator(selector).screenshot(path=filepath)
        test_logger.info(f"Element screenshot saved: {filepath}")

        return filepath


    # ============================================
    # Additional Utility Methods (IMPROVEMENTS)
    # ============================================

    def hover(self, selector: str) -> None:
        """
        Hover over element.

        Useful for dropdown menus or tooltips.
        
        Args:
            selector: Element selector
        """
        self.page.locator(selector).hover()
        test_logger.info(f"Hovered over: {selector}")
    
    
    def double_click(self, selector: str) -> None:
        """
        Double click element.
        
        Args:
            selector: Element selector
        """
        self.page.locator(selector).dblclick()
        test_logger.info(f"Double clicked: {selector}")
    
    
    def right_click(self, selector: str) -> None:
        """
        Right click element (context menu).
        
        Args:
            selector: Element selector
        """
        self.page.locator(selector).click(button="right")
        test_logger.info(f"Right clicked: {selector}")
    
    
    def get_page_title(self) -> str:
        """
        Get page title.
        
        Returns:
            str: Page title
        """
        title = self.page.title()
        test_logger.info(f"Page title: {title}")
        return title
    
    
    def clear_input(self, selector: str) -> None:
        """
        Clear input field.
        
        Useful before filling a field that already has content.
        
        Args:
            selector: Input selector
        """
        self.page.locator(selector).clear()
        test_logger.info(f"Cleared input: {selector}")