"""Page Objects module"""
from .base_page import BasePage
from .todo_page import TodoPage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .login_demo_page import LoginDemoPage  # ← NUEVO

__all__ = [
    'BasePage',
    'TodoPage',
    'LoginPage',
    'DashboardPage',
    'LoginDemoPage'  # ← NUEVO
]