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

llm = OpenAI(model_name="text-davinci-003", temperature=0.7)


tools = [CustomSearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

template = """
You're a friendly search tool
Question: {question}

Answer: Let's think step by step."""


@cl.langchain_factory(use_async=False)
def main():
    llm = OpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(template))
    return chain


# @cl.langchain_run
# async def run(input_str):
#     res = await cl.make_async(agent)(
#         input_str, callbacks=[cl.ChainlitCallbackHandler()]
#     )
#     print(res)
#     await cl.Message(content=res["output"]).send()
