import os

from langchain_openai import ChatOpenAI
from schema import DatabaseSchema

def getStructuredLLM():

    os.environ["OPENAI_API_KEY"] = ""
    llm = ChatOpenAI(
        base_url = "",
        model="",
        temperature=0.0,
        max_tokens=4096
    )

    # Wrap the base LLM with LangChain's structured output parser, passing our Pydantic schema
    # This automatically handles the system instructions needed to force JSON formatting
    structuredLLM = llm.with_structured_output(DatabaseSchema)
    return structuredLLM