import os
import re
import sys
import requests
from llm_ai import llm
from langchain.tools import tool, Tool
from langchain_community.utilities import SQLDatabase
from langchain.agents import initialize_agent, AgentType

import warnings
warnings.filterwarnings("ignore")

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a specified city using wttr.in API.
    """
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises an error for unsuccessful responses
    except requests.RequestException as e:
        return f"Error fetching weather: {e}"
    
    try:
        data = response.json()
        temp = data["current_condition"][0]["temp_C"]
        condition = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"The weather in {city} is {temp}°C with {condition}."
    except (KeyError, IndexError) as e:
        return f"Error processing weather data: {e}"



tools = [get_weather]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

query = "I want to know the sum of weather in Darker and Lagos"


response = agent.invoke(query)
print(response)
print("\n\n")
