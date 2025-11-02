import reflex as rx
from typing import TypedDict, Optional, Literal
import datetime


class Task(TypedDict):
    id: int
    name: str
    status: str
    last_run: str
    script_content: str
    scraped_links: list[str]
    scraped_documents: list[str]


class ScrapingConfig(TypedDict):
    url: str
    tags: list[str]
    use_ai: bool
    schedule: Literal["once", "monitor"]


class TaskState(rx.State):
    tasks: list[Task] = []
    selected_task: Optional[Task] = None
    search_query: str = ""
    show_new_task_dialog: bool = False
    new_task_type: str = ""
    new_tag: str = ""
    scraping_config: ScrapingConfig = {
        "url": "",
        "tags": ["links", "documents"],
        "use_ai": False,
        "schedule": "once",
    }

    @rx.event
    def toggle_new_task_dialog(self):
        self.show_new_task_dialog = not self.show_new_task_dialog
        if not self.show_new_task_dialog:
            self._reset_new_task_form()

    def _reset_new_task_form(self):
        self.new_task_type = ""
        self.new_tag = ""
        self.scraping_config = {
            "url": "",
            "tags": ["links", "documents"],
            "use_ai": False,
            "schedule": "once",
        }

    @rx.var
    def task_name_suggestion(self) -> str:
        if self.new_task_type == "web_scraping" and self.scraping_config["url"]:
            try:
                domain = self.scraping_config["url"].split("//")[1].split("/")[0]
                return f"Scrape {domain}"
            except IndexError as e:
                import logging

                logging.exception(f"Error parsing URL for task name suggestion: {e}")
                return "Web Scraping Task"
        return "New Task"

    @rx.event
    def add_tag(self):
        if self.new_tag and self.new_tag not in self.scraping_config["tags"]:
            self.scraping_config["tags"].append(self.new_tag)
            self.new_tag = ""

    @rx.event
    def remove_tag(self, tag: str):
        self.scraping_config["tags"].remove(tag)

    @rx.event
    def set_scraping_url(self, url: str):
        self.scraping_config["url"] = url

    @rx.event
    def set_scraping_schedule(self, schedule: Literal["once", "monitor"]):
        self.scraping_config["schedule"] = schedule

    @rx.event
    def create_new_task(self, form_data: dict):
        print("Creating new task with data:", form_data)
        self.toggle_new_task_dialog()
        return rx.toast.info("Task creation logic not yet implemented.")

    @rx.event
    def load_task_details(self):
        """Load the details of a specific task based on the task_id from the URL."""
        self.selected_task = None
        if not self.tasks:
            self.load_tasks()
        task_id_str = self.router.page.params.get("task_id", "")
        if task_id_str.isdigit():
            task_id = int(task_id_str)
            found_task = next(
                (task for task in self.tasks if task["id"] == task_id), None
            )
            self.selected_task = found_task
        else:
            print(f"Invalid task_id: {task_id_str}")
            self.selected_task = None

    @rx.event
    def load_tasks(self):
        self.tasks = [
            {
                "id": 1,
                "name": "Daily Data Backup",
                "status": "completed",
                "last_run": "2024-07-29 02:00:00",
                "script_content": "print('Backing up data...')",
                "scraped_links": [],
                "scraped_documents": [],
            },
            {
                "id": 2,
                "name": "Generate Weekly Report",
                "status": "failed",
                "last_run": "2024-07-28 10:30:00",
                "script_content": """import pandas as pd
print('Generating report...')""",
                "scraped_links": [
                    "https://example.com/report/1",
                    "https://example.com/report/2",
                ],
                "scraped_documents": [
                    "weekly_report_2024_w30.pdf",
                    "sales_data_w30.csv",
                ],
            },
            {
                "id": 3,
                "name": "Process User Signups",
                "status": "running",
                "last_run": "2024-07-29 11:00:00",
                "script_content": "print('Processing signups...')",
                "scraped_links": [],
                "scraped_documents": [],
            },
            {
                "id": 4,
                "name": "System Health Check",
                "status": "idle",
                "last_run": "Never",
                "script_content": """import psutil
print(f'CPU: {psutil.cpu_percent()}%')""",
                "scraped_links": [],
                "scraped_documents": [],
            },
        ]

    @rx.var
    def filtered_tasks(self) -> list[Task]:
        if not self.search_query.strip():
            return self.tasks
        lower_query = self.search_query.lower()
        return [
            task
            for task in self.tasks
            if lower_query in task["name"].lower()
            or lower_query in task["status"].lower()
        ]

    @rx.var
    def monitored_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task["status"] == "running"]