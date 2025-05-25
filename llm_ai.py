import os
import getpass
from langchain_groq import ChatGroq

models = ["meta-llama/llama-4-scout-17b-16e-instruct","openai/o3"]


llm = ChatGroq(
    model= models[0],
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
