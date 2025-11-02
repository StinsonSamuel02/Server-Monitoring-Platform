import reflex as rx
import psutil
import platform
import asyncio
from datetime import datetime, timedelta
from typing import TypedDict, Any


class Metric(TypedDict):
    name: str
    value: float
    unit: str
    icon: str
    color: str


class SystemInfo(TypedDict):
    os: str
    hostname: str
    uptime: str


class CpuHistory(TypedDict):
    time: str
    usage: float


class ServerState(rx.State):
    """State for monitoring server resources."""

    is_loading: bool = True
    metrics: list[Metric] = []
    system_info: SystemInfo = {"os": "", "hostname": "", "uptime": ""}
    cpu_history: list[CpuHistory] = []
    MAX_HISTORY_POINTS: int = 30

    @rx.event
    async def on_load(self):
        """Initial data load and start background monitoring."""
        await self.update_metrics()
        self.is_loading = False
        return ServerState.monitor_resources

    @rx.event(background=True)
    async def monitor_resources(self):
        """Continuously monitor server resources in the background."""
        while True:
            async with self:
                await self.update_metrics()
            await asyncio.sleep(2)

    @rx.event
    async def update_metrics(self):
        """Fetches and updates the server metrics."""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        self.metrics = [
            {
                "name": "CPU Usage",
                "value": round(cpu_percent, 1),
                "unit": "%",
                "icon": "cpu",
                "color": "#F59E0B",
            },
            {
                "name": "Memory Usage",
                "value": round(memory.percent, 1),
                "unit": "%",
                "icon": "memory-stick",
                "color": "#10B981",
            },
            {
                "name": "Disk Space",
                "value": round(disk.percent, 1),
                "unit": "%",
                "icon": "hard-drive",
                "color": "#3B82F6",
            },
        ]
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days, remainder = divmod(uptime.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"
        self.system_info = {
            "os": f"{platform.system()} {platform.release()}",
            "hostname": platform.node(),
            "uptime": uptime_str,
        }
        current_time = datetime.now().strftime("%H:%M:%S")
        self.cpu_history.append({"time": current_time, "usage": cpu_percent})
        if len(self.cpu_history) > self.MAX_HISTORY_POINTS:
            self.cpu_history.pop(0)