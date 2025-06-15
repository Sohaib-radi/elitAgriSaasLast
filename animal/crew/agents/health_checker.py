from crewai import Agent
from datetime import datetime, timedelta
import random

class HealthCheckerAgent:
    """
     AI Agent: Animal Health Technician
    ====================================
    A hyper-intelligent diagnostic unit equipped with expert-level knowledge in veterinary protocols, 
    livestock behavior analysis, anomaly detection, and vaccine lifecycle management.

    Role: Real-time guardian of herd health.
    Mission: Eliminate delays, reduce risk, and ensure proactive treatment — before any issue becomes critical.
    """

    def __init__(self):
        self.agent = Agent(
            role="Animal Health Technician",
            goal=(
                "Continuously monitor animal health, detect early warning signs of disease or distress, "
                "track vaccination cycles, and provide intelligent recommendations to maintain herd-wide wellness."
            ),
            backstory=(
                "You are the brain of a high-tech livestock wellness system deployed on modern smart farms. "
                "Developed using the latest advancements in artificial intelligence and veterinary medicine, "
                "you analyze biometric data, detect behavioral anomalies, and ensure each animal receives the right vaccine at the right time. "
                "You work alongside supervisors and task agents, proactively preventing disease spread and optimizing long-term productivity."
            ),
            llm=None,  # Replace with actual LLM when deployed
            verbose=True
        )

    def check_health(self):
        self._log_event("🧠 Initiating full diagnostic health scan across all active animals...")
        self._simulate_environmental_scan()
        report = self._generate_health_report()
        self._display_report(report)
        self._log_event("📤 Health analysis completed. Recommendations prepared.\n")
        return report

    def get(self):
        return self.agent

    def run_full_diagnostic_cycle(self):
        self._log_event("🔄 Beginning complete diagnostic cycle with system-level scan...")
        self._simulate_environmental_conditions()
        self._simulate_sensor_integrity_check()
        report = self.check_health()
        self._log_event("✅ Diagnostic cycle finalized and dispatched to supervising agents.")
        return report

    # ========== Utility Functions ==========

    def _generate_health_report(self):
        # Simulated logic — in real use, replace with sensor data or API integrations
        return {
            "unvaccinated_animals": ["Cow #3", "Goat #7", "Sheep #2"],
            "health_alerts": [
                "Goat #7: Abnormal temperature (39.6°C), reduced movement.",
                "Cow #3: Slight limping detected via motion pattern analysis.",
            ],
            "vaccines_due": self._generate_due_vaccines(),
            "recommendations": [
                "🔧 Immediate on-site inspection for Goat #7 within 2 hours.",
                "💉 Administer scheduled booster for Sheep #2 within 48 hours.",
                "📡 Apply motion tracking tag to Cow #3 and review for 72 hours.",
                "📝 Generate daily health summary for at-risk animals.",
            ],
        }

    def _generate_due_vaccines(self):
        return [
            f"Sheep #2 ➜ Deworming due on {self._format_date(2)}",
            f"Goat #7 ➜ Rabies booster due on {self._format_date(0)}",
            f"Cow #3 ➜ Foot-and-mouth vaccine overdue by 3 days"
        ]

    def _display_report(self, report: dict):
        print("\n📋 Full Diagnostic Health Report:\n")
        for section, items in report.items():
            title = section.replace('_', ' ').title()
            print(f"🔹 {title}:")
            for entry in items:
                print(f"   - {entry}")
            print()

    def _log_event(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def _format_date(self, days_from_now: int):
        date = datetime.now() + timedelta(days=days_from_now)
        return date.strftime("%Y-%m-%d")

    def _simulate_environmental_scan(self):
        print("🌡️  Scanning temperature and humidity conditions across barns...")
        barn_conditions = {
            "North Barn": "26°C | 70% Humidity",
            "East Barn": "28°C | 65% Humidity",
            "South Field": "30°C | 60% Humidity"
        }
        for location, condition in barn_conditions.items():
            print(f"    {location}: {condition}")
        print()

    def _simulate_environmental_conditions(self):
        print("🌍 Performing environmental stress check (heat, humidity, space)...")
        print("   🔎 No critical stressors detected today.\n")

    def _simulate_sensor_integrity_check(self):
        print("📶 Running integrity scan on biometric and motion sensors...")
        issues = random.choice([[], ["Sensor #14: Weak signal", "Sensor #8: Battery low"]])
        if not issues:
            print("   All systems operational.")
        else:
            for issue in issues:
                print(f"   ⚠️  {issue}")
        print()
