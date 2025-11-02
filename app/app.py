import reflex as rx
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.states.auth_state import AuthState
from app.pages.tasks import tasks_page
from app.pages.task_details import task_details_page
from app.pages.monitoring import monitoring_page
from app.states.task_state import TaskState


def protected_page(page_component_func):
    def page_with_auth_check(*args, **kwargs):
        return rx.cond(
            AuthState.is_authenticated,
            page_component_func(*args, **kwargs),
            login_page(),
        )

    return page_with_auth_check


def loading_page(page_component_func):
    def page_with_loading_and_auth_check(*args, **kwargs):
        return rx.cond(
            AuthState.is_authenticated,
            page_component_func(*args, **kwargs),
            rx.center(
                rx.el.div(
                    rx.spinner(class_name="w-8 h-8 text-orange-500"),
                    rx.el.p("Loading...", class_name="mt-2 text-gray-600"),
                    class_name="flex flex-col items-center",
                )
            ),
        )

    return page_with_loading_and_auth_check


@loading_page
def index() -> rx.Component:
    return dashboard_page()


def routines_page():
    return rx.el.p("Routines Page Content")


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
app.add_page(
    protected_page(dashboard_page), route="/dashboard", on_load=initial_auth_check
)
app.add_page(protected_page(tasks_page), route="/tasks", on_load=initial_auth_check)
app.add_page(
    protected_page(task_details_page),
    route="/tasks/[task_id]",
    on_load=[initial_auth_check, TaskState.load_task_details],
)
app.add_page(
    protected_page(monitoring_page), route="/monitoring", on_load=initial_auth_check
)
app.add_page(
    protected_page(routines_page), route="/routines", on_load=initial_auth_check
)