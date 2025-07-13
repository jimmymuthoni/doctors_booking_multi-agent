from fastapi import FastAPI
from pydantic import BaseModel
from agents import DoctorBookingAgent
from langchain_core.messages import HumanMessage
import os

os.environ.pop("SSL_CERT_FILE", None)

#app defination
app = FastAPI()

#pydantic model to eforce the shema of user query
class UserQuery(BaseModel):
    id_number: int
    messages: str

agent = DoctorBookingAgent()

@app.post("/execute")
def execute_agent(user_input: UserQuery):
    app_graph = agent.workflow()

    #agents state as expected by the workflow
    input = [
        HumanMessage(content=user_input.messages)
    ]
    input_data = {
        "messages": input,
        "id_number": user_input.id_number,
        "next": "",
        "query": "",
        "current_reasoning": "",
    }

    response = app_graph.invoke(input_data, config={"recursion_limit": 20})
    return {"messages": response["messages"]}