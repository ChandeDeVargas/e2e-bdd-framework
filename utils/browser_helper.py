"""
Browser Helper Utilities
POO approach to browser management

Demonstrates:
- Singleton pattern
- Class variables
- Instance tracking
"""
from typing import Dict, List, Optional
from datetime import datetime


class BrowserSession:
    """
    Browser session tracker.
    
    Tracks active browser sessions and their metadata.
    """
    
    # Class variable - shared across all instances
    _active_sessions: List['BrowserSession'] = []
    
    
    def __init__(self, browser_name: str, session_id: str):
        """
        Initialize browser session.
        
        Args:
            browser_name: Browser name
            session_id: Unique session ID
        """
        self.browser_name = browser_name
        self.session_id = session_id
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.tests_run = 0
        
        # Add to active sessions
        BrowserSession._active_sessions.append(self)
    
    
    def end_session(self) -> None:
        """End the session"""
        self.end_time = datetime.now()
        
        # Remove from active sessions
        if self in BrowserSession._active_sessions:
            BrowserSession._active_sessions.remove(self)
    
    
    @property
    def duration(self) -> float:
        """
        Get session duration in seconds.
        
        Returns:
            float: Duration in seconds
        """
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    
    @classmethod
    def get_active_sessions(cls) -> List['BrowserSession']:
        """
        Get all active sessions.
        
        Returns:
            List[BrowserSession]: Active sessions
        """
        return cls._active_sessions.copy()
    
    
    @classmethod
    def get_session_by_browser(cls, browser_name: str) -> List['BrowserSession']:
        """
        Get sessions for specific browser.
        
        Args:
            browser_name: Browser name to filter
            
        Returns:
            List[BrowserSession]: Sessions for browser
        """
        return [
            session for session in cls._active_sessions
            if session.browser_name == browser_name
        ]
    
    
    def __repr__(self) -> str:
        """String representation"""
        status = "active" if self.end_time is None else "ended"
        return f"BrowserSession({self.browser_name}, {status}, {self.duration:.1f}s)"


class BrowserConfig:
    """
    Browser configuration manager.
    
    Singleton pattern for browser settings.
    """
    
    _instance: Optional['BrowserConfig'] = None
    
    
    def __new__(cls):
        """
        Singleton pattern - only one instance exists.
        
        Returns:
            BrowserConfig: The single instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    
    def __init__(self):
        """Initialize configuration (only once)"""
        if self._initialized:
            return
        
        self._config: Dict[str, Dict] = {
            "chromium": {
                "headless": False,
                "viewport": {"width": 1920, "height": 1080},
                "args": ["--start-maximized"]
            },
            "firefox": {
                "headless": False,
                "viewport": {"width": 1920, "height": 1080},
            },
            "webkit": {
                "headless": False,
                "viewport": {"width": 1920, "height": 1080},
            }
        }
        
        self._initialized = True
    
    
    def get_config(self, browser_name: str) -> Dict:
        """
        Get configuration for browser.
        
        Args:
            browser_name: Browser name
            
        Returns:
            Dict: Browser configuration
        """
        return self._config.get(browser_name, {})
    
    
    def update_config(self, browser_name: str, config: Dict) -> None:
        """
        Update browser configuration.
        
        Args:
            browser_name: Browser name
            config: Configuration dict
        """
        if browser_name in self._config:
            self._config[browser_name].update(config)
        else:
            self._config[browser_name] = configs