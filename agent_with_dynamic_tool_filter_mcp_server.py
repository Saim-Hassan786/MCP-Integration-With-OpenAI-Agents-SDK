import os
import asyncio
from dotenv import find_dotenv,load_dotenv
from agents import Agent,Runner,set_default_openai_api,set_tracing_disabled,set_default_openai_client
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttp,MCPServerStreamableHttpParams,ToolFilterContext

_:bool = load_dotenv(find_dotenv())
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

external_client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL")
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

async def dynamic_tool_filter(context:ToolFilterContext,tool)->bool:
    print(f"Tool Invoked : {tool.name} With ToolContext : {context}")
    if tool.name == "Mood_Tool":
        return True
    if tool.name == "Addition_Tool":
        return False
    return True
    
async def main():
    print("Setting Up The Connection And Client For Agent Loop")
    mcp_params = MCPServerStreamableHttpParams(
        url=MCP_SERVER_URL
    )
    async with MCPServerStreamableHttp(
        params=mcp_params,
        name="MCPServerClient",
        cache_tools_list=True,
        tool_filter=dynamic_tool_filter
    ) as mcp_client:
        print(f"MCP CLIENT ESTABLISHED NAMED {mcp_client.name}")
        agent = Agent(
            name = "Agent With MCP Server",
            instructions= "A helper Ai Assistant With MCP Server Tools",
            mcp_servers=[mcp_client],
            model="gemini-2.5-flash"
        )

        print(f"Agent Name {agent.name} Initialized With MCP Server {mcp_client.name}")
        print(f"Listing the tools Of MCP ")
        tools = await mcp_client.list_tools(run_context=object(),agent=object())
        print(f"Tools : {tools}")

        runner = await Runner.run(
            starting_agent=agent,
            input="Hello, My name is Sam and Mood is happy reply using the tool .",
        )

        print(f"Agent Response : {runner.final_output}")

        runner_1 = await Runner.run(
            starting_agent=agent,
            input="Hello, My name is Jacob and Mood is sad reply using the tool ."
        )

        print(f"Agent Response : {runner_1.final_output}")

        runner_2 = await Runner.run(
            starting_agent=agent,
            input="Add 10 into 100 from me using the tool"
        )
        print(f"Agent Response : {runner_2.final_output}")
    print(f"MCPServerStreamableHttp client '{mcp_client.name}' context exited.")

if __name__ == "__main__":
    asyncio.run(main()) 