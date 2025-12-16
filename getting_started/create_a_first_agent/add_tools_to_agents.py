from strands import Agent, tool
from strands_tools import calculator

@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"

agent = Agent(
    model='anthropic.claude-3-5-sonnet-20241022-v2:0',
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather.")

response = agent("What is the weather today?")

print(response)

#In Strands you can do it using the tool method of your agent followed by the tool name.
# You can invoke the tool directly like so:

# Calculate derivative
agent.tool.calculator(expression="sin(x)", mode="derive", wrt="x", order=2)