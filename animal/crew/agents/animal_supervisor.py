from crewai import Agent
from datetime import datetime
import random

class AnimalSupervisorAgent:
    """
    AI Agent: Animal Operations Supervisor
    =========================================
    A strategic brain overseeing all animal care operations.
    Precision, accountability, and smart delegation — every day.
    """

    def __init__(self):
        self.agent = Agent(
            role="Animal Operations Supervisor",
            goal="Maximize efficiency, health, and coordination of all animal-related farm tasks through intelligent oversight and delegation.",
            backstory=(
                "You are the central intelligence behind a high-performance livestock management system. "
                "With years of experience in animal welfare and farm logistics, you supervise a team of humans and AI agents. "
                "Every day, you analyze animal care requirements and assign tasks with military-grade precision — from feeding routines to vaccinations. "
                "You ensure zero delays, full accountability, and peak animal health across the farm."
            ),
            llm=None,  
            verbose=True,
            allow_delegation=False
        )

    def assign_tasks(self):
        self._log_event("ßß Starting task assignment workflow...")
        assignments = {
            "Feeding": self._assign_to("Ahmed"),
            "Sanitation": self._assign_to("Amira"),
            "Vaccination": self._assign_to("Health Checker Agent", is_ai=True),
        }
        self._display_assignments(assignments)
        self._log_event("✅ All tasks dispatched successfully.")
        return assignments

    def get(self):
        return self.agent

    # ========== Utility Functions ==========

    def _assign_to(self, assignee, is_ai=False):
        return f"{'AI Agent' if is_ai else 'Human Agent'}: {assignee}"

    def _log_event(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def _display_assignments(self, assignments: dict):
        print("\n📊 Daily Task Report:")
        for task, person in assignments.items():
            print(f"   🔹 {task.ljust(12)} ➜ {person}")
        print()

    def _generate_task_id(self):
        return f"TASK-{random.randint(1000, 9999)}-{datetime.now().strftime('%H%M')}"

    def _simulate_checklist(self):
        checklist = ["Verify animal health data", "Fetch today's weather", "Check staff availability"]
        print("\n🧾 Pre-task Checklist:")
        for item in checklist:
            status = random.choice(["OK ✅", "Pending ⚠️"])
            print(f" - {item}: {status}")
        print()

    def run_full_supervision_cycle(self):
        self._log_event("🔁 Full supervision cycle started.")
        self._simulate_checklist()
        task_id = self._generate_task_id()
        self._log_event(f"🆔 Generated Task Batch ID: {task_id}")
        assignments = self.assign_tasks()
        self._log_event("📡 Supervision cycle completed.\n")
        return {"task_id": task_id, "assignments": assignments}
