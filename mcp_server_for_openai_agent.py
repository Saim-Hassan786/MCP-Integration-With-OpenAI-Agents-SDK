from mcp.server.fastmcp import FastMCP
from typing import Literal

mcp = FastMCP(
    name = "MCP SERVER FOR AI AGENT",
    stateless_http = True,
    json_response= True
)

@mcp.tool(
    name="Addition_Tool",
    description= "A greeting tool that greets the User",
    title= "ADDER"
)
async def addition(a:int,b:int):
    return f"Hi there, This is the result of Addition {a+b} 😀 From MCP SERVER FOR AI AGENT"

@mcp.tool(
    name="Mood_Tool",
    description= "A Mood tool that replies according to User Mood",
    title= "Mood"
)
async def mood_user(name:str,mood: Literal["Happy","Sad"]):
    if mood == "Happy":
        return f"I am glad to hear to your mood is {mood}, Have a nice day 😃"
    else:
        return f"Dont Worry, if your mood is {mood}, Better Days Are coming 🎇🎆✨"

@mcp.prompt(
    name = "Code Review Prompt",
    title = "Code Reviewer",
    description="A code reviewer Prompt that works best for code check instructions"  
)
async def code_review_prompt(
    focus: Literal["general code quality","medium code quality","in-depth code quality"],
    programming_language : Literal["python","javascript"]
    ):
      prompt = f"""You are a senior {programming_language} code review specialist. Your role is to provide comprehensive code analysis with focus on {focus}.

INSTRUCTIONS:
- Analyze code for quality, security, performance, and best practices
- Provide specific, actionable feedback with examples
- Identify potential bugs, vulnerabilities, and optimization opportunities
- Suggest improvements with code examples when applicable
- Be constructive and educational in your feedback
- Focus particularly on {focus} aspects

RESPONSE FORMAT:
1. Overall Assessment
2. Specific Issues Found
3. Security Considerations
4. Performance Notes
5. Recommended Improvements
6. Best Practices Suggestions

Use the available tools to check current time if you need timestamps for your analysis."""
      return prompt

    
mcp_app = mcp.streamable_http_app()