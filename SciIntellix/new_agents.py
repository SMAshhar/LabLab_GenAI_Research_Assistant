import os
from crewai import Agent
from pydantic import BaseModel
from openai import OpenAI

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
def core_gpt_model(query: str) -> str:
    """
    This function interacts with the GPT-o1 model and returns the response.
    
    :param query: The query or task for GPT-o1 to process.
    :return: Processed response from the model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                    ],
                }
            ],
        )
                # Return the model's response
        return response['choices'][0]['text'].strip()
    
    except Exception as e:
        return f"Error interacting with GPT-o1 model: {str(e)}"


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
        query = f"Find research papers and studies on {research_topic}. Provide relevant findings and insights."
        return core_gpt_model(query)

class TheoryTestingAgent(BaseModel):
    role: str = "Theory Tester"
    goal: str = (
        "The Theory Testing Agent assists researchers in validating or analyzing proposed theories. By taking a "
        "given theory, this agent uses the GPT model to perform a thorough analysis, simulate potential outcomes, "
        "and offer insights based on previous research. The goal is to critically assess the theory, identifying "
        "any logical inconsistencies or gaps, and providing conclusions that may guide further research."
    )

    def perform_task(self, theory: str) -> str:
        query = f"Analyze and test the following theory: {theory}. Provide insights and conclusions."
        return core_gpt_model(query)

class SuggestionAgent(BaseModel):
    role: str = "Research Advisor"
    goal: str = (
        "The Suggestion Agent is designed to offer advice and recommendations for researchers looking to expand "
        "or improve their current research. The agent leverages the GPT model to analyze the provided research "
        "topic and suggest new directions, areas of focus, or potential improvements. Its goal is to inspire "
        "new lines of inquiry and ensure that researchers explore innovative, impactful paths within their field."
    )


    def perform_task(self, research_topic: str) -> str:
        query = f"Provide suggestions and improvements for research on {research_topic}. Recommend new directions or areas of focus."
        return core_gpt_model(query)
