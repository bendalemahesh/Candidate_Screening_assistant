from services.spacy_service import SpacyService
from prompts.job_description_parser_prompt import job_description_prompt
from models.groq_model import llm
from models.job_description_model import JobDescription


class JobDescriptionAgent:

    def __init__(self):

        self.spacy = SpacyService()

        self.structured_llm = llm.with_structured_output(
            JobDescription
        )

        self.chain = (
            job_description_prompt
            | self.structured_llm
        )

    def parse_job_description(
        self,
        jd_text: str
    ):

        # ---------- spaCy ----------
        doc = self.spacy.process(jd_text)

        basic_info = {

            "location": self.spacy.extract_location(
                jd_text,
                doc
            ),

        }

        # ---------- Groq ----------
        print("Calling Job Description Extraction...")

        job = self.chain.invoke(
            {
                "job_description": jd_text
            }
        )

        print("Job Description Extraction Success")

        # Merge spaCy output

        if basic_info["location"]:
            job.company_location = basic_info["location"]

        return job