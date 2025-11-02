import reflex as rx
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.states.auth_state import AuthState


def protected_page(page_component: rx.Component) -> rx.Component:
    """A wrapper to protect pages that require authentication."""
    return rx.cond(
        AuthState.is_authenticated,
        page_component,
        rx.center(
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-orange-500"),
                rx.el.p("Loading...", class_name="mt-2 text-gray-600"),
                class_name="flex flex-col items-center",
            )
        ),
    )


def index() -> rx.Component:
    """The root page, which redirects based on authentication status."""
    return rx.cond(
        AuthState.is_authenticated, protected_page(dashboard_page()), login_page()
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)


def initial_auth_check():
    return AuthState.set_is_authenticated(AuthState.is_authenticated)


app.add_page(index, on_load=initial_auth_check)
app.add_page(lambda: protected_page(dashboard_page()), route="/dashboard")
from app.pages.tasks import tasks_page
from app.pages.monitoring import monitoring_page


def routines_page():
    return protected_page(rx.el.p("Routines Page Content"))


app.add_page(tasks_page, route="/tasks")
app.add_page(monitoring_page, route="/monitoring")
app.add_page(routines_page, route="/routines")