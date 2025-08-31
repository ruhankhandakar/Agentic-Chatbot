from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langgraph.prebuilt import tools_condition

from state.state import State
from nodes.basic_chatbot_node import BasicChatBotNode
from nodes.chatbot_with_tool_node import ChatBotWithToolNode
from nodes.ai_news_node import AiNewsNode
from tools.search_tool import get_tools, create_tool_node

class GraphBuilder:
    def __init__(self, model: ChatGroq):
        self.model = model
        self.graph_builder = StateGraph(State)
        self.basic_chatbot = None

    def setup_graph(self,usecase: str):
        if usecase == "Basic Chatbot":
            self._basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self._chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            self._ai_news_build_graph()

        return self.graph_builder.compile()

    def _basic_chatbot_build_graph(self):
        self.basic_chatbot = BasicChatBotNode(self.model)

        self.graph_builder.add_node("chatbot", self.basic_chatbot.process)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def _chatbot_with_tools_build_graph(self):
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define the chatbot node
        chatbot_with_node = ChatBotWithToolNode(self.model)
        chatbot_node = chatbot_with_node.create_chatbot(tools)

        # Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Add Edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot") # END will be handled by tool

    def _ai_news_build_graph(self):
        ai_news_node = AiNewsNode(self.model)

        # Nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        # Edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)
