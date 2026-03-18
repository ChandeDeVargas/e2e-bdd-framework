"""
Logging Utilities
Professional logging system for tests with colors and formatting
"""
import logging
import colorlog
from datetime import datetime
import os

class TestLogger:
    """
    Custom logger for tests.
    
    Features:
    - Console logs with colors
    - File logs
    - Different levels (DEBUG, INFO, WARNING, ERROR)
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - only one instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize logger (only once)"""
        if self._initialized:
            return
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/test_{timestamp}.log"
        
        # Setup logger
        self.logger = logging.getLogger("E2E_BDD_Tests")
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # ============================================
        # CONSOLE handler (with colors)
        # ============================================
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Color format
        console_format = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s | "
            "%(cyan)s%(name)s%(reset)s | "
            "%(message)s",
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        
        # ============================================
        # FILE handler (without colors)
        # ============================================
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # File format
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self._initialized = True
        
        # Initial log
        self.logger.info("=" * 60)
        self.logger.info("Test Logger initialized")
        self.logger.info(f"Log file: {log_file}")
        self.logger.info("=" * 60)
        
    def get_logger(self):
        """Get logger instance"""
        return self.logger
    
    # ============================================
    # Convenience methods
    # ============================================
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
        
    def step(self, message):
        """Log test step (special format)"""
        self.logger.info(f"STEP: {message}")
        
    def action(self, message):
        """Log action (special format)"""
        self.logger.info(f"ACTION: {message}")
        
    def assertion(self, message):
        """Log assertion (special format)"""
        self.logger.info(f"ASSERT: {message}")
        
    def test_start(self, test_name):
        """Log test start"""
        self.logger.info("")
        self.logger.info("=" * 60)
        self.logger.info(f"Test started: {test_name}")
        self.logger.info("=" * 60)
        
    def test_end(self, test_name, status="PASSED"):
        """Log test end"""
        self.logger.info("=" * 60)
        self.logger.info(f"TEST {status}: {test_name}")
        self.logger.info("=" * 60)
        self.logger.info("")


# ============================================
# Global instance
# ============================================
test_logger = TestLogger()
logger = test_logger.get_logger()