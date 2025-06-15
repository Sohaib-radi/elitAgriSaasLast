from crewai import Agent
from datetime import datetime
import random

class MediaInspectorAgent:
    """
    🧠 AI Agent: Media Proof Inspector
    ==================================
    A computer vision-trained AI specialist that reviews, validates, and audits media evidence submitted by farm workers.
    
    Role: Enforce accountability and verify task completion through photo and video analysis.
    """

    def __init__(self):
        self.agent = Agent(
            role="Media Proof Inspector",
            goal=(
                "Audit and validate photo/video submissions from farm employees to ensure tasks like cleaning, "
                "feeding, and maintenance are executed correctly, on time, and without manipulation."
            ),
            backstory=(
                "You are a computer vision-powered AI designed for operational transparency on smart farms. "
                "Your mission is to analyze image and video submissions, detect inconsistencies, and confirm that media "
                "evidence aligns with assigned tasks. You look for cleaning quality, timestamp mismatches, "
                "potential editing artifacts, and discrepancies in reported vs actual progress."
            ),
            llm=None,  # Can be extended with a CV model or vision LLM
            verbose=True
        )

    def analyze_media(self):
        self._log_event("🔍 Starting media inspection on submitted visual evidence...")
        self._simulate_media_preprocessing()

        results = self._generate_media_analysis_result()
        self._display_results(results)

        self._log_event(" Media inspection completed. Audit report dispatched.\n")
        return results

    def get(self):
        return self.agent

    def run_full_media_review(self):
        self._log_event("📦 Full review cycle initialized (video, photo, metadata)...")
        results = self.analyze_media()
        self._log_event("📈 Visual audit cycle finalized.")
        return results

    # ========== Utility Functions ==========

    def _generate_media_analysis_result(self):
        return {
            "pen_cleanliness": "Pen B2 marked as partially cleaned (dust traces remain in corners).",
            "video_valid": True,
            "photo_timestamp_match": False,  # Example mismatch
            "detected_anomalies": [
                "Metadata inconsistency: Photo timestamp predates assigned task time by 2 hours.",
                "Possible frame skip detected in video sequence between 00:01:43 and 00:01:46."
            ],
            "suspicious": True,
            "confidence_score": f"{random.randint(82, 95)}%"
        }

    def _simulate_media_preprocessing(self):
        print("🧪 Preprocessing media files (frame extraction, metadata parsing, quality scoring)...")
        print("   - Video duration: 2m 15s")
        print("   - Photo resolution: 1920x1080")
        print("   - Metadata parsed successfully\n")

    def _display_results(self, results: dict):
        print("Media Inspection Report:")
        for key, value in results.items():
            if isinstance(value, list):
                for item in value:
                    print(f"   -  {item}")
            else:
                label = key.replace('_', ' ').title()
                symbol = "✅" if value is True else "❌" if value is False else "ℹ️"
                print(f"   - {label}: {symbol} {value}")
        print()

    def _log_event(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
