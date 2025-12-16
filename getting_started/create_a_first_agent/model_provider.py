# Amazon Bedrock providing the model ID string directly :
from strands import Agent

agent = Agent(model="us.anthropic.claude-3-7-sonnet-20250219-v1:0")
print(agent.model.config)


# For more control over the model configuration, you can create a BedrockModel provider instance:
import boto3
from strands import Agent
from strands.models import BedrockModel

# Create a BedrockModel
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name='us-west-2',
    temperature=0.3,
)

agent = Agent(model=bedrock_model)