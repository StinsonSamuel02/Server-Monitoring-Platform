import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    """The login form component."""
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.icon("square_terminal", class_name="w-8 h-8 text-orange-500"),
                rx.el.h1("PyDash", class_name="text-2xl font-bold text-gray-800"),
                class_name="flex items-center gap-3 mb-8",
            ),
            rx.el.div(
                rx.el.label(
                    "Username", class_name="text-sm font-medium text-gray-600 mb-1"
                ),
                rx.el.input(
                    name="username",
                    placeholder="admin",
                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password", class_name="text-sm font-medium text-gray-600 mb-1"
                ),
                rx.el.input(
                    name="password",
                    type="password",
                    placeholder="admin",
                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="w-4 h-4 mr-2"),
                    rx.el.span(AuthState.error_message),
                    class_name="flex items-center text-sm bg-red-100 text-red-600 p-3 rounded-lg mb-6",
                ),
                None,
            ),
            rx.el.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.spinner(class_name="w-5 h-5"),
                    rx.el.span("Sign In"),
                ),
                type="submit",
                disabled=AuthState.is_loading,
                class_name="w-full bg-orange-500 text-white font-semibold py-3 rounded-lg hover:bg-orange-600 transition-colors flex items-center justify-center disabled:bg-orange-300",
            ),
            rx.el.div(
                rx.el.p("Demo: Use ", class_name="text-xs text-gray-500"),
                rx.el.kbd(
                    "admin",
                    class_name="px-1.5 py-0.5 text-xs font-semibold text-gray-800 bg-gray-100 border border-gray-200 rounded-md",
                ),
                rx.el.p(" / ", class_name="text-xs text-gray-500"),
                rx.el.kbd(
                    "admin",
                    class_name="px-1.5 py-0.5 text-xs font-semibold text-gray-800 bg-gray-100 border border-gray-200 rounded-md",
                ),
                class_name="flex items-center gap-1 mt-4 text-xs text-gray-500 justify-center",
            ),
            class_name="bg-white p-8 rounded-xl shadow-lg border border-gray-100 w-full max-w-md",
        ),
        on_submit=AuthState.login,
        reset_on_submit=False,
    )


def login_page() -> rx.Component:
    """The main login page."""
    return rx.el.main(
        rx.el.div(
            login_form(),
            class_name="min-h-screen w-full flex items-center justify-center bg-gray-50 p-4",
        ),
        class_name="font-['Lato']",
    )