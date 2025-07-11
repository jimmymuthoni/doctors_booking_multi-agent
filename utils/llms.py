import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

#loading and setting keys as envronment varibales
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
QROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ['QROQ_API_KEY'] = QROQ_API_KEY

class LLMModel:
    def __init__(self, model_name = 'gemma2-9b-it'):
        if not model_name:
            raise ValueError("Model is not defined")
        self.model_name = model_name
        self.groq_model = ChatGroq(model=model_name)

    def get_model(self):
        return self.groq_model
    
if __name__ == "__main__":
    llm_instance = LLMModel()
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("hello there")

    print(response.content)