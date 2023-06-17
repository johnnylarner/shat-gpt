import os
import chainlit as cl
from dotenv import load_dotenv
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.vectorstores import Weaviate
from langchain.tools import BaseTool
from llm_agent import CustomSearchTool

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")
WEAVIATE_URL = os.environ["WEAVIATE_URL"]

llm = OpenAI(model_name="text-davinci-003", temperature=0)


tools = [CustomSearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

template = """
You're a search agent, that helps to find answers to the questions based on the MLOPs Community Database.
Question: {question}
"""


@cl.langchain_factory(use_async=False)
def main():
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(template=template, input_variables=["question"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


@cl.langchain_run
async def run(input_str):
    res = await cl.make_async(agent)(
        input_str, callbacks=[cl.ChainlitCallbackHandler()]
    )
    print(res)
    await cl.Message(content=res["output"]).send()
