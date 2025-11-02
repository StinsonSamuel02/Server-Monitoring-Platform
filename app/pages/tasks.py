import reflex as rx
from app.states.task_state import TaskState, Task


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name=rx.cond(
                status == "running",
                "h-2 w-2 rounded-full bg-green-500 animate-pulse",
                rx.cond(
                    status == "completed",
                    "h-2 w-2 rounded-full bg-blue-500",
                    rx.cond(
                        status == "failed",
                        "h-2 w-2 rounded-full bg-red-500",
                        "h-2 w-2 rounded-full bg-gray-400",
                    ),
                ),
            )
        ),
        rx.el.span(status.capitalize(), class_name="ml-2"),
        class_name=rx.cond(
            status == "running",
            "flex items-center text-xs font-medium text-green-700 bg-green-100 px-2.5 py-1 rounded-full w-fit",
            rx.cond(
                status == "completed",
                "flex items-center text-xs font-medium text-blue-700 bg-blue-100 px-2.5 py-1 rounded-full w-fit",
                rx.cond(
                    status == "failed",
                    "flex items-center text-xs font-medium text-red-700 bg-red-100 px-2.5 py-1 rounded-full w-fit",
                    "flex items-center text-xs font-medium text-gray-700 bg-gray-100 px-2.5 py-1 rounded-full w-fit",
                ),
            ),
        ),
    )


def task_row(task: Task) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            task["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800",
        ),
        rx.el.td(
            status_badge(task["status"]),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            task["last_run"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(tag="play", class_name="h-4 w-4"),
                    class_name="p-1.5 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-md transition-colors",
                ),
                rx.el.button(
                    rx.icon(tag="eye", class_name="h-4 w-4"),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors",
                ),
                rx.el.button(
                    rx.icon(tag="trash-2", class_name="h-4 w-4"),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium",
        ),
        class_name="hover:bg-gray-50",
    )


def tasks_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Python Tasks", class_name="text-2xl font-bold text-gray-800"),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                    rx.el.input(
                        placeholder="Search tasks...",
                        on_change=TaskState.set_search_query.debounce(300),
                        class_name="w-full pl-10 pr-4 py-2 border-none focus:ring-0 bg-transparent",
                    ),
                    class_name="relative flex items-center w-full max-w-sm",
                ),
                rx.el.button(
                    rx.icon(tag="plus", class_name="h-4 w-4 mr-2"),
                    "New Task",
                    class_name="flex items-center bg-orange-500 text-white font-semibold px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Last Run",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(TaskState.filtered_tasks, task_row),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-hidden border border-gray-200 rounded-xl shadow-sm",
        ),
        class_name="p-6",
    )


def tasks_page() -> rx.Component:
    from app.pages.dashboard import sidebar, header

    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(tasks_table(), on_mount=TaskState.load_tasks),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )