from crewai import Task
from django.utils import timezone
from media.models import MediaSubmission

def verify_media_proof(agent):
    def _execute_media_validation():
        today = timezone.now().date()
        submissions = MediaSubmission.objects.filter(
            timestamp__date=today,
            is_valid__isnull=True  # Not yet reviewed
        )

        validated = []
        flagged = []

        for submission in submissions:
            # Simulate a basic validation based on quality_score
            if submission.quality_score >= 75:
                submission.is_valid = True
                validated.append(f"{submission.media_type.upper()} - {submission.task_type} by {submission.employee_name}")
            else:
                submission.is_valid = False
                flagged.append(f"{submission.media_type.upper()} - {submission.task_type} by {submission.employee_name} (score: {submission.quality_score})")

            submission.reviewed_at = timezone.now()
            submission.save()

        return {
            "status": "reviewed",
            "valid_submissions": validated,
            "flagged_submissions": flagged,
            "total_reviewed": len(submissions),
            "message": "Media validation complete. Report ready for supervisor."
        }

    return Task(
        description="Inspect all submitted images and videos from today's shift to validate cleaning and feeding tasks.",
        expected_output="Detailed report listing valid and flagged media submissions with reasons.",
        agent=agent.get(),
        tools=[_execute_media_validation]
    )
