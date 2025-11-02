import reflex as rx
from app.states.server_state import ServerState
from app.states.task_state import Task, TaskState


def metric_card_small(metric: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(metric["icon"], class_name="w-5 h-5 text-gray-500"),
            rx.el.p(metric["name"], class_name="font-semibold text-gray-700 text-sm"),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.el.span(
                metric["value"].to_string() + metric["unit"],
                class_name="text-2xl font-bold text-gray-900",
            ),
            class_name="mt-2",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm w-full",
    )


def monitored_task_row(task: Task) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            task["name"], class_name="px-5 py-3 text-sm font-medium text-gray-800"
        ),
        rx.el.td(task["last_run"], class_name="px-5 py-3 text-sm text-gray-600"),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-2 w-2 rounded-full bg-green-500 animate-pulse mr-2"
                ),
                "Running",
                class_name="flex items-center text-xs font-medium text-green-700",
            ),
            class_name="px-5 py-3",
        ),
    )


def monitoring_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Live Monitoring", class_name="text-2xl font-bold mb-4 text-gray-800"),
        rx.el.p(
            "An overview of system resources and tasks currently being monitored.",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Server Resources",
                class_name="text-lg font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.foreach(ServerState.metrics, metric_card_small),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Monitored Tasks", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Task Name",
                                class_name="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Last Run",
                                class_name="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(TaskState.monitored_tasks, monitored_task_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-hidden border border-gray-200 rounded-xl shadow-sm",
            ),
        ),
        class_name="p-6",
    )


def monitoring_page() -> rx.Component:
    from app.pages.dashboard import sidebar, header

    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(monitoring_content(), on_mount=ServerState.on_load),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )