from strands import Agent, tool
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import RatelimitException, DuckDuckGoSearchException
import logging

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)

# Define a websearch tool
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    """Search the web to get updated information.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return.
    Returns:
        List of dictionaries with search results.
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    except DuckDuckGoSearchException as d:
        return f"DuckDuckGoSearchException: {d}"
    except Exception as e:
        return f"Exception: {e}"

# Create a recipe assistant agent
recipe_agent = Agent(
    model='anthropic.claude-3-5-sonnet-20241022-v2:0',
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to look up cooking information.""",
    tools=[websearch], # Import the websearch tool we created above
)

response = recipe_agent("Suggest a recipe with chicken and broccoli.")

print(f"Metrics : {response.metrics}") # Optional, but recommended.