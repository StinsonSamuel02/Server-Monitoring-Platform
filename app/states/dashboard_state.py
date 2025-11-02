import reflex as rx
from typing import TypedDict


class NavItem(TypedDict):
    name: str
    icon: str
    href: str


class DashboardState(rx.State):
    """State for the main dashboard layout and navigation."""

    @rx.var
    def active_page(self) -> str:
        return self.router.page.path

    sidebar_items: list[NavItem] = [
        {"name": "Server Resources", "icon": "server", "href": "/dashboard"},
        {"name": "Tasks", "icon": "list-checks", "href": "/tasks"},
        {"name": "Monitoring", "icon": "activity", "href": "/monitoring"},
        {"name": "Routines", "icon": "repeat", "href": "/routines"},
    ]