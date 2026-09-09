from langchain_core.prompts import ChatPromptTemplate

from prompts.ai_resume_analysis_prompt import AI_RESUME_ANALYSIS_PROMPT
from schemas.analysis_schema import ResumeAnalysis


class ResumeAnalyzer:
    def __init__(self, llm):
        self.llm = llm

        self.prompt = ChatPromptTemplate.from_template(
            AI_RESUME_ANALYSIS_PROMPT
        )

        self.chain = self.prompt | self.llm.with_structured_output(
            ResumeAnalysis
        )

    def analyze(self, candidate_data):
        return self.chain.invoke(
            {
                "candidate_data": candidate_data
            }
        )