from crewai import Crew, Process

from crew.agents.animal_supervisor import AnimalSupervisorAgent
from crew.agents.media_inspector import MediaInspectorAgent
from crew.agents.health_checker import HealthCheckerAgent

from crew.tasks.assign_daily_tasks import assign_daily_tasks
from crew.tasks.verify_media_proof import verify_media_proof
from crew.tasks.flag_sick_animals import flag_sick_animals

def run_farm_ai_crew():
    # Instantiate agents
    supervisor = AnimalSupervisorAgent()
    inspector = MediaInspectorAgent()
    health_checker = HealthCheckerAgent()

    # Agents perform their smart duties (simulated)
    supervisor.assign_tasks()
    inspector.analyze_media()
    health_checker.check_health()

    # Create crew with tasks
    crew = Crew(
        agents=[
            supervisor.get(),
            inspector.get(),
            health_checker.get()
        ],
        tasks=[
            assign_daily_tasks(supervisor),
            verify_media_proof(inspector),
            flag_sick_animals(health_checker)
        ],
        process=Process.sequential
    )

    print("\n🚀 Running CrewAI for Farm Operations")
    crew.kickoff()
