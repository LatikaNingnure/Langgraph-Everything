from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from IPython.display import Image, display
import os

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGCHAIN_PROJECT"]="TestProject"

from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

llm=ChatGroq(model="qwen/qwen3.8-27b")
llm

class State(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

def make_tool_graph():
    ## Graph with tool call
    

    @tool
    def add(a:float, b:float):
        """Add to number"""
        return a+b

    tools=[add]
    tool_node =ToolNode([add])

    llm_with_tool=llm.bind_tools([add])

    def call_llm_model(state:State):
        return {"messages":[llm_with_tool.invoke(state['messages'])]}  

    ## Gharph
    builder=StateGraph(State)
    builder.add_node("call_llm_model",call_llm_model)
    builder.add_node("tools", ToolNode(tools))

    ## Add edges
    builder.add_edge(START, "call_llm_model")
    builder.add_conditional_edges("call_llm_model", tools_condition)
    builder.add_edge("tools", "call_llm_model")

    #compile the graph
    graph=builder.compile()

    return graph

tool_agent=make_tool_graph()

