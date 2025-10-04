import os
import asyncio
from dotenv import find_dotenv,load_dotenv
from agents import Agent,Runner,set_default_openai_api,set_tracing_disabled,set_default_openai_client
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttp,MCPServerStreamableHttpParams

_:bool = load_dotenv(find_dotenv())
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

external_client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL")
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

async def main():
    print("Setting Up The Connection And Client For Agent Loop")
    mcp_params = MCPServerStreamableHttpParams(
        url=MCP_SERVER_URL
    )
    print(f"Connecting the MCP Server at URL {mcp_params.get('url')}")
    async with MCPServerStreamableHttp(
        params = mcp_params,
        name="MCPServerClient"
    ) as mcp_client:
        print(f"MCP CLIENT ESTABLISHED NAMED {mcp_client.name}")
        print(f"Calling the Server to get the list of prompts : {mcp_client.name}")
        prompts = await mcp_client.list_prompts()
        print(f"Prompts : {prompts}")
        print(f"\nNow Getting|Calling the Prompt")
        prompt = await mcp_client.get_prompt(
            name = "Code Review Prompt",
            arguments = {
                "focus":"in-depth code quality",
                "programming_language": "python"
            }
        )
        print(f"\nThe Result Prompt Form The MCP Server {prompt}")
        instructions_from_mcp = prompt.messages[0].content.text
        print(f"\nFinal Instructions Extracted {instructions_from_mcp}")

        agent = Agent(
            name = "Agent With MCP Server",
            instructions= instructions_from_mcp,
            mcp_servers=[mcp_client],
            model="gemini-2.5-flash"
        )

        print(f"Agent Name {agent.name} Initialized With MCP Server {mcp_client.name}")

        runner = await Runner.run(
            starting_agent=agent,
            input="Hi Can you tell me about python language.",
        )

        print(f"Agent Response : {runner.final_output}")

    print(f"MCPServerStreamableHttp client '{mcp_client.name}' context exited.")

if __name__ == "__main__":
    asyncio.run(main())    