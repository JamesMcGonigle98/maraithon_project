"""
Using LLM Chains to Design a Meal Plan

Enter short description of the script
"""

__date__ = "2023-10-17"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from secret_keys import openai_key

# %% --------------------------------------------------------------------------
# Create Open AI Model
# -----------------------------------------------------------------------------
llm = OpenAI(openai_api_key= openai_key)

# %% --------------------------------------------------------------------------
# Prompt Templates
# -----------------------------------------------------------------------------
# First Template (for name)
prompt_template_meal_plan = PromptTemplate(
    input_variables=['day'],
    template = "Today is {day} and I am a marathon on Sunday. Design me a meal plan for this week. This should include breakfast, lunch, dinner and snacks. It is okay for meals to repeat on different days. The meals should be designed to optimise my marathon preparation as much as possible. Return this meal plan as a dictionary with the keys being Monday-Sunday for each respective day and the values being the meal plan for that day"
)

# Second Template (for items)
prompt_template_recipes = PromptTemplate(
    input_variables=['meal_plan'],
    template = "For each meal from Monday in the following meal plan: {meal_plan} write a recipe and cooking instructions. Return it as a comma seperated list"

)




# %% --------------------------------------------------------------------------
# Creating a Function
# -----------------------------------------------------------------------------
def generate_meal_plan(day):

    name_chain = LLMChain(llm=llm, prompt=prompt_template_meal_plan, output_key="meal_plan")

    items_chain = LLMChain(llm=llm, prompt=prompt_template_recipes, output_key="all_recipes")

    chain = SequentialChain(
    chains = [name_chain, items_chain],
    input_variables=['day'],
    output_variables=['meal_plan','all_recipes']
    )

    response = chain({'day':day})

    return response



# %% --------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
response = generate_meal_plan("Monday")

response['meal_plan']
# %%
