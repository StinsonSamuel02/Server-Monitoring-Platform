import reflex as rx
from typing import TypedDict
import datetime


class Task(TypedDict):
    id: int
    name: str
    status: str
    last_run: str
    script_content: str


class TaskState(rx.State):
    tasks: list[Task] = []
    search_query: str = ""

    @rx.event
    def load_tasks(self):
        self.tasks = [
            {
                "id": 1,
                "name": "Daily Data Backup",
                "status": "completed",
                "last_run": "2024-07-29 02:00:00",
                "script_content": "print('Backing up data...')",
            },
            {
                "id": 2,
                "name": "Generate Weekly Report",
                "status": "failed",
                "last_run": "2024-07-28 10:30:00",
                "script_content": """import pandas as pd
print('Generating report...')""",
            },
            {
                "id": 3,
                "name": "Process User Signups",
                "status": "running",
                "last_run": "2024-07-29 11:00:00",
                "script_content": "print('Processing signups...')",
            },
            {
                "id": 4,
                "name": "System Health Check",
                "status": "idle",
                "last_run": "Never",
                "script_content": """import psutil
print(f'CPU: {psutil.cpu_percent()}%')""",
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