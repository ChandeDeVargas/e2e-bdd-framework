"""
Base Page Class
Parent class for all page objects (POO pattern)

All page objects inherit from BasePage to share common methods.
"""
from playwright.sync_api import Page, expect
from typing import Optional

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
        self.page.goto(url, timeout=self.timeout)
        print(f"\n✔ Navigated to: {url}")

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
        self.page.click(selector, timeout=self.timeout)
        print(f"\n✔ Clicked on: {selector}")

    def fill(self, selector: str, text: str) -> None:
        """
        Fill input field.
        
        Args:
            selector: Input selector
            text: Text to fill
        """
        self.page.fill(selector, text, timeout=self.timeout)
        print(f"\n✔ Filled '{selector}' with text: {text}")

    def type_text(self, selector: str, text: str, delay: int = 100) -> None:
        """
        Type text with delay (simulates human typing).
        
        Args:
            selector: Input selector
            text: Text to type
            delay: Delay between keystrokes in ms
        """
        self.page.type(selector, text, delay=delay, timeout=self.timeout)
        print(f"\n✔ Typed: {text}")

    def press_key(self, selector: str, key: str) -> None:
        """
        Press keyboard key.
        
        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Escape')
        """
        self.page.press(selector, key, timeout=self.timeout)
        print(f"\n✔ Pressed key: '{key}' on: {selector}")

    def select_option(self, selector: str, value: str) -> None:
        """
        Select dropdown option.
        
        Args:
            selector: Select element selector
            value: Option value to select
        """
        self.page.select_option(selector, value, timeout=self.timeout)
        print(f"\n✔ Selected option: '{value}' in: {selector}")

    def check(self, selector: str) -> None:
        """
        Check checkbox.
        
        Args:
            selector: Checkbox selector
        """
        self.page.check(selector, timeout=self.timeout)
        print(f"\n✔ Checked: {selector}")

    def uncheck(self, selector: str) -> None:
        """
        Uncheck checkbox.
        
        Args:
            selector: Checkbox selector
        """
        self.page.uncheck(selector, timeout=self.timeout)
        print(f"\n✔ Unchecked: {selector}")

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
        print(f"\n✔ Element {state}: {selector}")

    def wait_for_url(self, url_pattern: str) -> None:
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern to wait for
        """
        self.page.wait_for_url(url_pattern, timeout=self.timeout)
        print(f"\n✔ URL matched: {url_pattern}")

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
        print(f"\n✔ Assertion passed: {selector} is visible")
    
    def assert_not_visible(self, selector: str) -> None:
        """
        Assert element is not visible.
        
        Args:
            selector: Element selector
        """
        expect(self.page.locator(selector)).not_to_be_visible(
            timeout=self.timeout
        )
        print(f"\n✔ Assertion passed: {selector} is not visible")

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
        print(f"\n✔ Assertion passed: {selector} contains text: {expected_text}")

    def assert_url_contains(self, url_part: str) -> None:
        """
        Assert URL contains text.
        
        Args:
            url_part: Expected URL part
        """
        expect(self.page).to_have_url(
            f".*{url_part}.*",
            timeout=self.timeout
        )
        print(f"\n✔ Assertion passed: URL contains: {url_part}")

    # ============================================
    # Get Methods
    # ============================================

    def get_text(self, selector: str) -> str:
        """
        Get element text content.
        
        Args:
            selector: Element selector
            
        Returns:
            str: Element text
        """
        text = self.page.locator(selector).text_content(timeout=self.timeout)
        print(f"\n✔ Got text from: {selector}: {text}")
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
        print(f"\n✔ Got attribute from: {selector}: {value}")
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
        print(f"📸 Screenshot saved: {filename}")
    
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def reload_page(self) -> None:
        """Reload current page"""
        self.page.reload()
        print("🔄 Page reloaded")
    
    
    def go_back(self) -> None:
        """Navigate back"""
        self.page.go_back()
        print("⬅️ Navigated back")
    
    
    def go_forward(self) -> None:
        """Navigate forward"""
        self.page.go_forward()
        print("➡️ Navigated forward")