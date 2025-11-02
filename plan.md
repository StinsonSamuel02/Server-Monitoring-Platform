# Server Monitoring and Task Management Platform

## Phase 1: Authentication and Dashboard Layout ✅
- [x] Create login page with modern SaaS styling (orange primary, gray secondary, Lato font)
- [x] Implement authentication state management with login/logout
- [x] Build base dashboard layout with header, sidebar navigation, and content area
- [x] Add navigation links for Server Resources, Tasks, Monitoring, and Routines sections
- [x] Create protected route system that redirects to login if not authenticated

---

## Phase 2: Real-time Server Resources Monitoring ✅
- [x] Create server metrics monitoring page with real-time CPU, Memory, and Disk usage
- [x] Implement backend integration using psutil library for system metrics
- [x] Add auto-refresh mechanism to update metrics every few seconds
- [x] Design visual cards and charts showing resource utilization with progress bars
- [x] Include system information display (OS, hostname, uptime)

---

## Phase 3: Python Task/Script Management System ✅
- [x] Build task management table with columns: name, status, last run, duration, actions
- [x] Implement CRUD operations for Python scripts (create, edit, delete, view)
- [x] Create "New Task" dialog with dynamic form based on task type
- [x] Add web scraping task type with URL input, tag selection (links, documents), and add custom tags
- [x] Implement execution schedule options: "Run Once" (default) and "Monitor"
- [x] Add task name auto-generation based on configuration (e.g., "Scrape example.com")
- [x] Implement search and pagination for tasks table
- [x] Install scrapegraphai library for AI-powered web scraping

---

## Phase 4: Live Monitoring Overview Page ✅
- [x] Create monitoring/overview page showing real-time server resources at top
- [x] Display compact metric cards for CPU, Memory, and Disk usage
- [x] Add table below showing only tasks that are in "monitoring" mode
- [x] Filter tasks table to show only "running" status tasks
- [x] Update navigation to include "Monitoring" section

---

## Phase 5: Scheduled Monitoring (Task Scheduling)
- [ ] Add scheduling configuration UI for individual tasks (cron-like interface)
- [ ] Implement schedule options: interval-based (every X minutes/hours) and cron expressions
- [ ] Create monitoring dashboard showing scheduled tasks status and next run times
- [ ] Add enable/disable toggle for scheduled tasks
- [ ] Display execution history with timestamps and status (success/failed)

---

## Phase 6: Routines System (Multi-Script Orchestration)
- [ ] Build routines management page for creating/editing routine workflows
- [ ] Implement drag-and-drop or ordered list for defining script execution sequence
- [ ] Add routine detail view showing all scripts in the routine with their order
- [ ] Create routine execution engine that runs scripts in specified order
- [ ] Implement routine scheduling system similar to task scheduling
- [ ] Display routine execution logs showing progress through each script step

---

## Phase 7: Web Scraping Implementation
- [ ] Implement actual web scraping logic using scrapegraphai
- [ ] Add AI-powered extraction option (optional toggle)
- [ ] Process selected tags (links, documents, images, etc.) for targeted extraction
- [ ] Store scraped data and make it viewable in task details
- [ ] Add export functionality for scraped data (JSON, CSV)

---

## Phase 8: Advanced Features and Polish
- [ ] Add real-time notifications for task/routine completion or failures
- [ ] Implement user settings page for notification preferences
- [ ] Add data visualization charts for historical resource usage and task performance
- [ ] Implement export functionality for logs (CSV, JSON)
- [ ] Add keyboard shortcuts and command palette (cmd+k) for quick navigation