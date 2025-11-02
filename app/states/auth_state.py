import reflex as rx
import asyncio


class AuthState(rx.State):
    """Manages user authentication state and logic."""

    is_authenticated: bool = False
    is_loading: bool = False
    error_message: str = ""

    @rx.event
    async def login(self, form_data: dict[str, str]):
        """Handles the login process."""
        self.is_loading = True
        self.error_message = ""
        yield
        await asyncio.sleep(1.5)
        username = form_data.get("username")
        password = form_data.get("password")
        if username == "admin" and password == "admin":
            self.is_authenticated = True
            self.is_loading = False
            yield rx.redirect("/dashboard")
        else:
            self.error_message = "Invalid username or password"
            self.is_authenticated = False
            self.is_loading = False

    @rx.event
    def logout(self):
        """Logs the user out and redirects to the login page."""
        self.is_authenticated = False
        yield rx.redirect("/")