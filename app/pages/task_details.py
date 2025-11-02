import reflex as rx
from app.states.task_state import TaskState
from app.pages.dashboard import sidebar, header


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name=rx.match(
                status,
                ("running", "h-2 w-2 rounded-full bg-green-500 animate-pulse"),
                ("completed", "h-2 w-2 rounded-full bg-blue-500"),
                ("failed", "h-2 w-2 rounded-full bg-red-500"),
                "h-2 w-2 rounded-full bg-gray-400",
            )
        ),
        rx.el.span(status.capitalize(), class_name="ml-2"),
        class_name=rx.match(
            status,
            (
                "running",
                "flex items-center text-xs font-medium text-green-700 bg-green-100 px-2.5 py-1 rounded-full w-fit",
            ),
            (
                "completed",
                "flex items-center text-xs font-medium text-blue-700 bg-blue-100 px-2.5 py-1 rounded-full w-fit",
            ),
            (
                "failed",
                "flex items-center text-xs font-medium text-red-700 bg-red-100 px-2.5 py-1 rounded-full w-fit",
            ),
            "flex items-center text-xs font-medium text-gray-700 bg-gray-100 px-2.5 py-1 rounded-full w-fit",
        ),
    )


def task_details_content() -> rx.Component:
    return rx.el.div(
        rx.cond(
            TaskState.selected_task.is_none(),
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-orange-500"),
                rx.el.p("Loading task details...", class_name="mt-2 text-gray-600"),
                class_name="flex flex-col justify-center items-center h-64",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                    "Back to Tasks",
                    href="/tasks",
                    class_name="flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.h2(
                        TaskState.selected_task["name"],
                        class_name="text-2xl font-bold text-gray-800",
                    ),
                    status_badge(TaskState.selected_task["status"]),
                    class_name="flex items-center justify-between mb-1",
                ),
                rx.el.p(
                    rx.text.strong("Last run: "),
                    TaskState.selected_task["last_run"],
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Scraped Links",
                            class_name="text-lg font-semibold text-gray-800 mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(
                                TaskState.selected_task["scraped_links"],
                                lambda link: rx.el.a(
                                    rx.icon(
                                        "link",
                                        class_name="w-4 h-4 text-gray-400 mr-3 shrink-0",
                                    ),
                                    rx.el.span(
                                        link,
                                        class_name="truncate text-blue-600 hover:underline",
                                    ),
                                    href=link,
                                    target="_blank",
                                    class_name="flex items-center p-3 hover:bg-gray-50 rounded-lg transition-colors text-sm",
                                ),
                            ),
                            class_name="divide-y divide-gray-100",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Scraped Documents",
                            class_name="text-lg font-semibold text-gray-800 mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(
                                TaskState.selected_task["scraped_documents"],
                                lambda doc: rx.el.div(
                                    rx.icon(
                                        "file-text",
                                        class_name="w-4 h-4 text-gray-400 mr-3 shrink-0",
                                    ),
                                    rx.el.span(
                                        doc,
                                        class_name="truncate text-gray-800 font-medium",
                                    ),
                                    rx.el.div(class_name="flex-grow"),
                                    rx.el.button(
                                        rx.icon(
                                            "cloud_download", class_name="w-4 h-4 mr-2"
                                        ),
                                        "Download",
                                        on_click=rx.download(
                                            url=f"/placeholder.svg", filename=doc
                                        ),
                                        class_name="flex items-center text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold px-3 py-1.5 rounded-md transition-colors",
                                    ),
                                    class_name="flex items-center p-3 hover:bg-gray-50 rounded-lg transition-colors text-sm",
                                ),
                            ),
                            class_name="divide-y divide-gray-100",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                ),
            ),
        ),
        class_name="p-6",
    )


def task_details_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(task_details_content()),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Lato']",
    )