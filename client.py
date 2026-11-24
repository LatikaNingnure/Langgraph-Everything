from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio

from dotenv import load_dotenv
load_dotenv

import asyncio 

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args": ["MCPDEMOLANGCHAIN\\mathserver.py"],
                "transport":"stdio",
            },
            "weather":{
                "url": "http://127.0.0.1:8001/mcp",
                "transport":"stramablr_http",   
            }

        }
    )

    import os


    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen/qwen3.8-27b")
    agent=create_react_agent(
        model, tools
    )

    math_response = await agent.invoke(
        {"messages":[{"role":"user", "content": "What's (3+5)*12?"}]}
    )
    print("Math response", math_response['messages'][-1].content)

asyncio.run(main())    
