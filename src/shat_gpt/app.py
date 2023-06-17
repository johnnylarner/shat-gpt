import os
import chainlit as cl
from dotenv import load_dotenv
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.agents import load_tools, initialize_agent, AgentType
from llm_agent import CustomSearchTool

load_dotenv()
API_KEY = os.environ.get("API_KEY")

llm = OpenAI(model_name="text-davinci-003", temperature=0.7, openai_api_key=API_KEY)

tools = [CustomSearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

template = """
You're a friendly
Question: {question}

Answer: Let's think step by step."""


@cl.langchain_factory(use_async=True)
def factory():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    tools = [CustomSearchTool()]
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    return agent.run(prompt)
