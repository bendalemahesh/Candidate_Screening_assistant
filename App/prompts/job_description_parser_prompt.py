from langchain_core.prompts import ChatPromptTemplate

job_description_prompt = ChatPromptTemplate.from_template("""
You are an expert HR recruiter.

Extract the following information from the Job Description.

Job Description:
{job_description}

Instructions:

- Extract Job Title
- Company
- Company Email
- Company LinkedIn
- Company Location
- Employment Type
- Work Mode
- Salary Range
- Notice Period
- Experience Required
- Education Required
- Required Skills
- Responsibilities
- Certifications
- Programming Languages

Only extract information explicitly mentioned.
If a value is missing, return null.
Return empty lists for missing arrays.
Do not guess any information.
""")