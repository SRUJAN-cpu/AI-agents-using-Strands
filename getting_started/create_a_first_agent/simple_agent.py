from strands import Agent

# Initialize your agent
agent = Agent(
    model='anthropic.claude-3-5-sonnet-20241022-v2:0',
    system_prompt="You are a helpful assistant that provides concise responses.",
)

# Send a message to the agent
response = agent("Hello! What can you do?")
print(response)