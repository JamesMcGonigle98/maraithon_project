"""
LLM Agents

Testing different LLM Agents with the Strava Data
"""

__date__ = "2023-10-09"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from secret_keys import openai_key

from strava_access import DownloadData
from formatting_data import FormatData

# %% --------------------------------------------------------------------------
# Initiate Model
# -----------------------------------------------------------------------------
llm = ChatOpenAI(
        temperature=0, 
        model="gpt-3.5-turbo-16k", 
        openai_api_key= openai_key
        )


# %% --------------------------------------------------------------------------
# Download Data and Formatting
# -----------------------------------------------------------------------------
data = DownloadData()
data.get_access_token()
data.download_data() 
data.json_save()

formatted_data = FormatData(data.all_activities)
formatted_data.json_to_df()
formatted_data.cleaning_up_df()
formatted_data.month_agg()



# %% --------------------------------------------------------------------------
# Create Agent
# -----------------------------------------------------------------------------
model = create_pandas_dataframe_agent(
    llm = llm,
    df = formatted_data.activities_df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    max_iterations=3)


