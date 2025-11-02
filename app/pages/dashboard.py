import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.states.server_state import ServerState


def nav_item(item: dict[str, str]) -> rx.Component:
    """A single navigation item in the sidebar."""
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["name"]),
        href=item["href"],
        class_name=rx.cond(
            DashboardState.active_page == item["href"],
            "flex items-center gap-3 rounded-lg px-3 py-2 text-orange-600 bg-orange-50 transition-all hover:text-orange-700 font-semibold",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-600 transition-all hover:text-gray-900 hover:bg-gray-50 font-medium",
        ),
    )


def sidebar() -> rx.Component:
    """The dashboard sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("square_terminal", class_name="h-8 w-8 text-orange-500"),
                rx.el.h1("PyDash", class_name="text-2xl font-bold"),
                class_name="flex items-center gap-3",
            ),
            class_name="flex h-16 items-center border-b px-6",
        ),
        rx.el.div(
            rx.el.nav(
                rx.foreach(DashboardState.sidebar_items, nav_item),
                class_name="flex flex-col gap-1 p-4",
            ),
            class_name="flex-1 overflow-auto",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("log-out", class_name="h-5 w-5 mr-2"),
                "Logout",
                on_click=AuthState.logout,
                class_name="w-full flex items-center justify-center bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg transition-colors",
            ),
            class_name="p-4 border-t",
        ),
        class_name="hidden md:flex flex-col bg-white border-r w-64 h-screen",
    )


def header() -> rx.Component:
    """The dashboard header component."""
    return rx.el.header(
        rx.el.div(),
        rx.el.div(
            rx.el.h1(
                "Welcome, admin!", class_name="text-xl font-semibold text-gray-800"
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon(
                    "github", class_name="w-6 h-6 text-gray-600 hover:text-gray-900"
                ),
                href="https://github.com/reflex-dev/reflex",
                target="_blank",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center h-16 border-b bg-white px-6 w-full",
    )


def metric_card(metric: rx.Var[dict]) -> rx.Component:
    """A card displaying a single server metric."""
    return rx.el.div(
        rx.el.div(
            rx.icon(metric["icon"], class_name="w-6 h-6 text-gray-500"),
            rx.el.p(metric["name"], class_name="font-semibold text-gray-700"),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.span(
                metric["value"].to_string() + metric["unit"],
                class_name="text-3xl font-bold text-gray-900",
            ),
            class_name="mt-4 mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-2 rounded-full",
                style={
                    "width": metric["value"].to_string() + "%",
                    "background_color": metric["color"],
                },
            ),
            class_name="w-full bg-gray-200 rounded-full h-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm w-full",
    )


def cpu_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Real-time CPU Usage", class_name="text-lg font-semibold mb-4 text-gray-800"
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
            rx.recharts.graphing_tooltip(
                cursor=False, content_style={"background_color": "#FFFFFF"}
            ),
            rx.recharts.x_axis(
                data_key="time", tick_line=False, axis_line=False, class_name="text-xs"
            ),
            rx.recharts.y_axis(
                tick_line=False, axis_line=False, class_name="text-xs", domain=[0, 100]
            ),
            rx.recharts.area(
                data_key="usage",
                stroke="#F59E0B",
                fill="#FEF3C7",
                type_="monotone",
                stroke_width=2,
                dot=False,
            ),
            data=ServerState.cpu_history,
            height=250,
            width="100%",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mt-6",
    )


def system_info_panel() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "System Information", class_name="text-lg font-semibold mb-4 text-gray-800"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Hostname", class_name="font-medium text-gray-500 text-sm"),
                rx.el.p(
                    ServerState.system_info["hostname"],
                    class_name="font-semibold text-gray-900",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(class_name="my-2 border-t border-gray-100"),
            rx.el.div(
                rx.el.p(
                    "Operating System", class_name="font-medium text-gray-500 text-sm"
                ),
                rx.el.p(
                    ServerState.system_info["os"],
                    class_name="font-semibold text-gray-900 text-right",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(class_name="my-2 border-t border-gray-100"),
            rx.el.div(
                rx.el.p("Uptime", class_name="font-medium text-gray-500 text-sm"),
                rx.el.p(
                    ServerState.system_info["uptime"],
                    class_name="font-semibold text-gray-900",
                ),
                class_name="flex items-center justify-between",
            ),
            class_name="space-y-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mt-6",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Server Resources", class_name="text-2xl font-bold mb-4 text-gray-800"
        ),
        rx.el.p(
            "Real-time monitoring of your server's performance and resource utilization.",
            class_name="text-gray-600 mb-6",
        ),
        rx.cond(
            ServerState.is_loading,
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-orange-500"),
                class_name="w-full flex justify-center p-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(ServerState.metrics, metric_card),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                cpu_chart(),
                system_info_panel(),
            ),
        ),
        class_name="p-6",
    )


def dashboard_page() -> rx.Component:
    """The main dashboard page layout."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(dashboard_content(), on_mount=ServerState.on_load),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )