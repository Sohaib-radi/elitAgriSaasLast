from crewai import Task
from animal.models import AnimalTaskAssignment 
from django.utils import timezone

def assign_daily_tasks(agent, created_by):
    def _execute_task():
        today = timezone.now().date()

        # Predefined assignments (this can be replaced by AI logic or dynamic scheduling)
        assignments = {
            "feeding": "Employee Ahmed",
            "cleaning": "Employee Amira",
            "vaccination": "Health Checker Agent"
        }

        created_records = []

        for task_type, assignee in assignments.items():
            obj, created = AnimalTaskAssignment.objects.get_or_create(
                task_type=task_type,
                date=today,
                defaults={
                    "assigned_to": assignee,
                    "status": "pending",
                    "created_by": created_by
                }
            )
            created_records.append({
                "task": task_type,
                "assigned_to": assignee,
                "created": created,
                "status": obj.status
            })

        return {
            "status": "success",
            "assigned_tasks": created_records,
            "message": "All critical animal tasks have been delegated and logged."
        }

    return Task(
        description="Assign today's feeding, cleaning, and vaccination tasks to employees and agents. Log each assignment and track confirmation.",
        expected_output="All critical animal tasks have been delegated and logged for today.",
        agent=agent.get(),
        tools=[_execute_task]  # Task will invoke this function
    )
