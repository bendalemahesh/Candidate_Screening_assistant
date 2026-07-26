from App.workflows.dashboard_workflow import dashboard_workflow

response = dashboard_workflow.invoke({

    "dashboard": {}

})

print(response["dashboard"])