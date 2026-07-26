from langchain_core.messages import HumanMessage

from App.workflows.candidate_screening_workflow import screening_workflow

response = screening_workflow.invoke({

    "candidate_id": 1,

    "job_id": 1,

    "candidate": {},

    "job": {},

    "match": {},

    "recommendation": ""

})

print(response["match"])
print()
print(response["recommendation"])