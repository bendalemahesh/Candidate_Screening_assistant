from langchain_core.messages import HumanMessage

from App.workflows.analytics_workflow import analytics_workflow

response = analytics_workflow.invoke({

    "candidates": [],

    "jobs": [],

    "analytics": {}

})

print(response["analytics"])