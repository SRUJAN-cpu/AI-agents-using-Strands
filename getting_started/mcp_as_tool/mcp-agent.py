import threading
import time
from datetime import timedelta

from mcp import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.server import FastMCP
from strands import Agent
from strands.tools.mcp import MCPClient

# Connect to an MCP server using stdio transport
stdio_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Create an agent with MCP tools
with stdio_mcp_client:
    # Get the tools from the MCP server
    tools = stdio_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        tools=tools)

    response = agent("What is Amazon Bedrock pricing model. Be concise.")

# Create an MCP server
mcp = FastMCP("Calculator Server")

# Define a tool

@mcp.tool(description="Calculator tool which performs calculations")
def calculator(x: int, y: int) -> int:
    return x + y


@mcp.tool(description="This is a long running tool")
def long_running_tool(name: str) -> str:
    time.sleep(25)
    return f"Hello {name}"


def main():
    mcp.run(transport="streamable-http", mount_path="mcp")

    # Let's now start a thread with the streamable-http server

thread = threading.Thread(target=main)
thread.start()

def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp")


streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

with streamable_http_mcp_client:
    tools = streamable_http_mcp_client.list_tools_sync()

    agent = Agent(
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        tools=tools)

    response = str(agent("What is 2 + 2?"))

    # tools are typically invoked by the agent based on user requests, you can also call MCP tools directly. This can be useful for workflow scenarios where you orchestrate multiple tools together.

query = {"x": 10, "y": 20}

with streamable_http_mcp_client:
    # direct tool invocation
    result = streamable_http_mcp_client.call_tool_sync(
        tool_use_id="tool-123", name="calculator", arguments=query
    )

    # Process the result
    print(f"Calculation result: {result['content'][0]['text']}")

    
with streamable_http_mcp_client:
    try:
        result = streamable_http_mcp_client.call_tool_sync(
            tool_use_id="tool-123",
            name="long_running_tool",
            arguments={"name": "Amazon"},
            read_timeout_seconds=timedelta(seconds=30),
        )

        if result["status"] == "error":
            print(f"Tool execution failed: {result['content'][0]['text']}")
        else:
            print(f"Tool execution succeeded: {result['content'][0]['text']}")
    except Exception as e:
        print(f"Tool call timed out or failed: {str(e)}")

        # Connect to an MCP server using stdio transport
aws_docs_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Connect to an MCP server using stdio transport
cdk_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command="uvx", args=["awslabs.cdk-mcp-server@latest"])
    )
)

# Create an agent with MCP tools
with aws_docs_mcp_client, cdk_mcp_client:
    # Get the tools from the MCP server
    tools = aws_docs_mcp_client.list_tools_sync() + cdk_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        tools=tools)

    response = agent(
        "What is Amazon Bedrock pricing model. Be concise. Also what are the best practices related to CDK?"
    )