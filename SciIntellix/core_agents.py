import openai
from crewai import Agent

# Function to interact with GPT-o1
def core_gpt_model(query: str) -> str:
    """
    This function interacts with the GPT-o1 model and returns the response.
    
    :param query: The query or task for GPT-o1 to process.
    :return: Processed response from the model.
    """
    try:
        response = openai.Completion.create(
            model="gpt-o1",  # GPT-o1 model identifier
            prompt=query,
            max_tokens=1000,  # Adjust token limit as needed
            temperature=0.7   # Controls randomness, adjust as needed
        )
        # Return the model's response
        return response['choices'][0]['text'].strip()
    
    except Exception as e:
        return f"Error interacting with GPT-o1 model: {str(e)}"



class ResearchAgent(Agent):
    def __init__(self):
        """
        Initializes the Research Agent with a specific role and goal.
        """
        self.role = "Research Assistant"
        self.goal = "Fetch relevant research papers and information based on the query."
    
    def perform_task(self, research_topic: str) -> str:
        """
        Performs the research task by querying the GPT-o1 model to find relevant research material.
        
        :param research_topic: The topic of research that the agent will investigate.
        :return: Research findings or related information based on the topic.
        """
        # Construct the query for GPT-o1
        query = f"Find research papers and studies on {research_topic}. Provide relevant findings and insights."
        
        # Use the core GPT model to fetch results
        return core_gpt_model(query)
    

class TheoryTestingAgent(Agent):
    def __init__(self):
        """
        Initializes the Theory Testing Agent with a specific role and goal.
        """
        self.role = "Theory Tester"
        self.goal = "Test the given theory and provide insights."
    
    def perform_task(self, theory: str) -> str:
        """
        Performs the theory testing task by querying GPT-o1 to analyze and test the theory.
        
        :param theory: The theory provided for testing.
        :return: Insights or analysis based on the theory.
        """
        # Construct the query for GPT-o1
        query = f"Analyze and test the following theory: {theory}. Provide insights and conclusions."
        
        # Use the core GPT model to analyze and test the theory
        return core_gpt_model(query)
    

class SuggestionAgent(Agent):
    def __init__(self):
        """
        Initializes the Suggestion Agent with a specific role and goal.
        """
        self.role = "Research Advisor"
        self.goal = "Suggest improvements or new directions based on existing research."
    
    def perform_task(self, research_topic: str) -> str:
        """
        Performs the suggestion task by querying GPT-o1 to provide recommendations for further research or improvements.
        
        :param research_topic: The research topic where suggestions are needed.
        :return: Recommendations or new research directions based on the topic.
        """
        # Construct the query for GPT-o1
        query = f"Provide suggestions and improvements for research on {research_topic}. Recommend new directions or areas of focus."
        
        # Use the core GPT model to get suggestions
        return core_gpt_model(query)



# Example usage of the ResearchAgent
research_agent = ResearchAgent()

# Let's assume we are researching the topic of "fish ecosystems"
research_topic = "fish ecosystems"

# Perform the task and get the results
research_results = research_agent.perform_task(research_topic)

print(f"Research Results for '{research_topic}':\n{research_results}")

# Example usage of the TheoryTestingAgent
theory_testing_agent = TheoryTestingAgent()

# Let's assume we are testing a theory related to fish ecosystems
theory = "Fish population growth is directly influenced by the availability of phytoplankton."

# Perform the task and get the results
theory_results = theory_testing_agent.perform_task(theory)

print(f"Theory Testing Results for '{theory}':\n{theory_results}")

# Example usage of the SuggestionAgent
suggestion_agent = SuggestionAgent()

# Let's assume the research topic is "fish population control"
research_topic = "fish population control"

# Perform the task and get the suggestions
suggestions = suggestion_agent.perform_task(research_topic)

print(f"Suggestions for '{research_topic}':\n{suggestions}")
