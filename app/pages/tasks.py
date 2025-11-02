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
                rx.el.a(
                    rx.icon(tag="eye", class_name="h-4 w-4"),
                    href=f"/tasks/{task['id']}",
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


def tag_item(tag: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(tag),
        rx.el.button(
            rx.icon("x", class_name="h-3 w-3"),
            on_click=lambda: TaskState.remove_tag(tag),
            class_name="ml-2 text-gray-500 hover:text-red-600",
        ),
        class_name="flex items-center bg-gray-100 text-gray-800 text-sm font-medium px-2.5 py-1 rounded-full",
    )


def web_scraping_form_section() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "URL to Scrape", class_name="block text-sm font-medium text-gray-700 mb-1"
        ),
        rx.el.input(
            name="url",
            placeholder="https://example.com",
            on_change=TaskState.set_scraping_url,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500",
        ),
        rx.el.div(
            rx.el.label(
                "Data to Extract",
                class_name="block text-sm font-medium text-gray-700 mt-4 mb-2",
            ),
            rx.el.div(
                rx.foreach(TaskState.scraping_config["tags"], tag_item),
                class_name="flex flex-wrap gap-2",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Add a new tag",
                    on_change=TaskState.set_new_tag,
                    class_name="flex-grow px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-orange-500",
                    default_value=TaskState.new_tag,
                ),
                rx.el.button(
                    "Add",
                    on_click=TaskState.add_tag,
                    class_name="px-4 py-2 bg-gray-200 text-gray-700 font-semibold rounded-r-md hover:bg-gray-300",
                ),
                class_name="flex mt-2",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            rx.el.label(
                "Execution Schedule",
                class_name="block text-sm font-medium text-gray-700 mt-4 mb-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Run Once",
                    on_click=lambda: TaskState.set_scraping_schedule("once"),
                    class_name=rx.cond(
                        TaskState.scraping_config["schedule"] == "once",
                        "px-4 py-2 border border-orange-500 bg-orange-100 text-orange-700 font-semibold rounded-l-md z-10",
                        "px-4 py-2 border border-gray-300 bg-white text-gray-700 font-medium rounded-l-md hover:bg-gray-50",
                    ),
                ),
                rx.el.button(
                    "Monitor",
                    on_click=lambda: TaskState.set_scraping_schedule("monitor"),
                    class_name=rx.cond(
                        TaskState.scraping_config["schedule"] == "monitor",
                        "px-4 py-2 border border-orange-500 bg-orange-100 text-orange-700 font-semibold rounded-r-md z-10 -ml-px",
                        "px-4 py-2 border border-gray-300 bg-white text-gray-700 font-medium rounded-r-md -ml-px hover:bg-gray-50",
                    ),
                ),
                class_name="flex",
            ),
        ),
        class_name="mt-4 space-y-4",
    )


def new_task_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                style={
                    "background_color": "rgba(0,0,0,0.5)",
                    "position": "fixed",
                    "inset": "0",
                    "z_index": "40",
                }
            ),
            rx.radix.primitives.dialog.content(
                rx.el.form(
                    rx.radix.primitives.dialog.title("Create New Task"),
                    rx.el.div(
                        rx.el.label(
                            "Task Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="task_name",
                            placeholder="e.g., Scrape Example.com",
                            default_value=TaskState.task_name_suggestion,
                            key=TaskState.task_name_suggestion,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500",
                        ),
                        rx.el.label(
                            "Task Type",
                            class_name="block text-sm font-medium text-gray-700 mt-4 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Select task type...", value="", disabled=True
                            ),
                            rx.el.option("Scrape a website", value="web_scraping"),
                            name="task_type",
                            on_change=TaskState.set_new_task_type,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500",
                            default_value="",
                        ),
                        rx.cond(
                            TaskState.new_task_type == "web_scraping",
                            web_scraping_form_section(),
                            None,
                        ),
                        class_name="py-4",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                class_name="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-md hover:bg-gray-300",
                            )
                        ),
                        rx.el.button(
                            "Create Task",
                            type="submit",
                            class_name="px-4 py-2 bg-orange-500 text-white font-semibold rounded-md hover:bg-orange-600",
                        ),
                        class_name="flex justify-end gap-3 mt-4 pt-4 border-t",
                    ),
                    on_submit=TaskState.create_new_task,
                ),
                style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "background_color": "white",
                    "padding": "1.5rem",
                    "border_radius": "0.75rem",
                    "box_shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                    "width": "90vw",
                    "max_width": "42rem",
                    "z_index": "50",
                },
            ),
        ),
        open=TaskState.show_new_task_dialog,
        on_open_change=TaskState.set_show_new_task_dialog,
    )


def tasks_table() -> rx.Component:
    return rx.el.div(
        new_task_dialog(),
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
                    on_click=TaskState.toggle_new_task_dialog,
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