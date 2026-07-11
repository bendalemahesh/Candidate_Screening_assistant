from App.services.resume_analyzer import ResumeAnalyzer
from App.models.groq_model import llm


class CandidateScreeningWorkflow:
    def __init__(self, llm):
        self.resume_analyzer = ResumeAnalyzer(llm)

    def run(self, candidate_data):
        return self.resume_analyzer.analyze(candidate_data)
