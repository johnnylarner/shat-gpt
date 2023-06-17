import os
import chainlit as cl
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import Weaviate
import weaviate


load_dotenv()
API_KEY = os.environ.get("COHERE_API_KEY")
WEAVIATE_URL = os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY = os.environ["WEAVIATE_API_KEY"]
CLASS_NAME = "TextItem"  # TextItem is our best index
auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)

# Instantiate the client with the auth config
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config,
    additional_headers={"X-Cohere-Api-Key": API_KEY},
)

weaviate_instance = Weaviate(
    client=client, index_name=CLASS_NAME, text_key="text", attributes=["source"]
)
llm = OpenAI(model_name="text-davinci-003", temperature=0.0)

template = """
You're a search agent, that helps to find answers to the questions based on the MLOPs Community Database.
Question: {question}
"""


@cl.langchain_factory(use_async=False)
def main():
    # Use RetrievalQAWithSourcesChain to return source of answer.
    # TODO: Display sources
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm, chain_type="stuff", retriever=weaviate_instance.as_retriever()
    )
    return chain


@cl.langchain_postprocess
async def postprocess(output: str):
    print(output)
    output = f"""
    Answer: {output["answer"]}
    Source: {output["sources"]}
    """
    await cl.Message(content=output).send()
