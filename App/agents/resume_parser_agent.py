from services.spacy_service import SpacyService
from prompts.resume_parser_prompt import resume_parser_prompt
from models.groq_model import llm
from models.candidate_profile_model import CandidateProfile


class ResumeParserAgent:

    def __init__(self):

        self.spacy = SpacyService()

        # Gemini will directly return CandidateProfile
        self.structured_llm = llm.with_structured_output(CandidateProfile)

        self.chain = resume_parser_prompt | self.structured_llm

    def parse_resume(self, resume_text: str):

        # ---------- spaCy ----------
        doc = self.spacy.process(resume_text)

        basic_info = {
            "full_name": self.spacy.extract_name(doc),
            "email": self.spacy.extract_email(resume_text),
            "phone": self.spacy.extract_phone(resume_text),
            "location": self.spacy.extract_location(
                        resume_text,
                        doc
            ),
            "linkedin": self.spacy.extract_linkedin(resume_text),
            "github": self.spacy.extract_github(resume_text),
        }

        # ---------- Gemini ----------
        profile = self.chain.invoke(
            {
                "resume": resume_text
            }
        )

        # Merge spaCy results
        profile.full_name = basic_info["full_name"]
        profile.email = basic_info["email"]
        profile.phone = basic_info["phone"]
        profile.location = basic_info["location"]
        profile.linkedin = basic_info["linkedin"]
        profile.github = basic_info["github"]

        return profile