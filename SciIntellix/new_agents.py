import os
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from functions import research_papers, suggestions, throey_test, tools_func


research_message = [
    {
        "role": "system",
        "content": (
            "The Research Agent is responsible for assisting researchers by fetching relevant research papers, "
            "studies, and other materials related to the specified research topic. The agent will query the GPT model "
            "to search for existing data and offer useful insights, making it easier for researchers to access "
            "previous findings. It aims to ensure that no important research is overlooked and that the latest, "
            "most relevant resources are brought to the researcher's attention."
        )
    },
]
theory_message = [
    {
        "role": "system",
        "content": (
            "The Theory Testing Agent assists researchers in validating or analyzing proposed theories. By taking a "
            "given theory, this agent uses the GPT model to perform a thorough analysis, simulate potential outcomes, "
            "and offer insights based on previous research. The goal is to critically assess the theory, identifying "
            "any logical inconsistencies or gaps, and providing conclusions that may guide further research."
        )
    }
]
suggestion_message = [
    {
        "role": "system",
        "content": (
            "The Suggestion Agent is designed to offer advice and recommendations for researchers looking to expand "
            "or improve their current research. The agent leverages the GPT model to analyze the provided research "
            "topic and suggest new directions, areas of focus, or potential improvements. Its goal is to inspire "
            "new lines of inquiry and ensure that researchers explore innovative, impactful paths within their field."
        )
    },
]

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

# Function to interact with GPT-o1
def core_gpt_model(messages: List) -> str:
    """
    This function interacts with the GPT model and returns the response.
    
    :param messages: List of messages in chat format to be passed to the model.
    :return: Processed response from the model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools_func
        )
        # Return the model's response (strip any leading/trailing whitespace)
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        return f"Error interacting with GPT model: {str(e)}"



class ResearchAgent(BaseModel):
    role: str = "Research Assistant"
    goal: str = (
        "The Research Agent is responsible for assisting researchers by fetching relevant research papers, "
        "studies, and other materials related to the specified research topic. The agent will query the GPT model "
        "to search for existing data and offer useful insights, making it easier for researchers to access "
        "previous findings. It aims to ensure that no important research is overlooked and that the latest, "
        "most relevant resources are brought to the researcher's attention."
    )

    def perform_task(self, research_topic: str) -> str:
        # Create the user query
        user_query = {
            "role": "user",
            "content": f"Find research papers and studies on {research_topic}. Provide relevant findings and insights."
        }
        
        # Append user query to the message list
        research_message.append(user_query)
        
        # Get result from GPT model
        result = core_gpt_model(research_message)
        
        # Append GPT's response as 'assistant' role in the conversation
        research_message.append({"role": "assistant", "content": result})
        
        # Return the result
        return result

class TheoryTestingAgent(BaseModel):
    role: str = "Theory Tester"
    goal: str = (
        "The Theory Testing Agent assists researchers in validating or analyzing proposed theories. By taking a "
        "given theory, this agent uses the GPT model to perform a thorough analysis, simulate potential outcomes, "
        "and offer insights based on previous research. The goal is to critically assess the theory, identifying "
        "any logical inconsistencies or gaps, and providing conclusions that may guide further research."
    )

    def perform_task(self, theory: str) -> str:
        # Create the user query for theory testing
        user_query = {
            "role": "user",
            "content": f"Analyze and test the following theory: {theory}. Provide insights and conclusions."
        }
        
        # Prepare message list with system message for theory testing
        theory_message.append(user_query)
        
        # Get result from GPT model
        result = core_gpt_model(theory_message)
        
        # Append the assistant's response to the message list for conversation context
        theory_message.append({"role": "assistant", "content": result})
        
        # Return the result
        return result


class SuggestionAgent(BaseModel):
    role: str = "Research Advisor"
    goal: str = (
        "The Suggestion Agent is designed to offer advice and recommendations for researchers looking to expand "
        "or improve their current research. The agent leverages the GPT model to analyze the provided research "
        "topic and suggest new directions, areas of focus, or potential improvements. Its goal is to inspire "
        "new lines of inquiry and ensure that researchers explore innovative, impactful paths within their field."
    )

    def perform_task(self, research_topic: str) -> str:
        # Create the user query for research suggestions
        user_query = {
            "role": "user",
            "content": f"Provide suggestions and improvements for research on {research_topic}. Recommend new directions or areas of focus."
        }
        
        # Prepare message list with system message for suggestions
        suggestion_message.append(user_query)

        # Get result from GPT model
        result = core_gpt_model(suggestion_message)
        
        # Append the assistant's response to the message list for conversation context
        suggestion_message.append({"role": "assistant", "content": result})
        
        # Return the result
        return result