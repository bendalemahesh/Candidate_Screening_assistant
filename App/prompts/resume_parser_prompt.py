from langchain_core.prompts import ChatPromptTemplate

resume_parser_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert ATS Resume Parser.

Extract the following information from the resume.

Return ONLY valid JSON.

Schema:

{{
  "skills": [],
  "education": [],
  "experience": [],
  "projects": [],
  "certifications": [],
  "summary": ""
}}

Rules:
- Return only JSON.
- Do not explain anything.
- Do not use markdown.
- If a field is missing, return an empty list or null.
"""
        ),
        (
            "human",
            """
Resume:

{resume}
"""
        )
    ]
)