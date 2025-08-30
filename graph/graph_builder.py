from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

from state.state import State
from nodes.basic_chatbot_node import BasicChatBotNode

class GraphBuilder:
    def __init__(self, model: ChatGroq):
        self.model = model
        self.graph_builder = StateGraph(State)
        self.basic_chatbot = None

    def setup_graph(self,usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        return self.graph_builder.compile()

    def basic_chatbot_build_graph(self):
        self.basic_chatbot = BasicChatBotNode(self.model)

        self.graph_builder.add_node("chatbot", self.basic_chatbot.process)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)