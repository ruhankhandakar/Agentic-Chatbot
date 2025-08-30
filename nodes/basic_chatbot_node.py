from langchain_groq import ChatGroq

from state.state import State

class BasicChatBotNode:
    def __init__(self, llm_model: ChatGroq):
        self.llm = llm_model

    def process(self, state: State) -> dict:
        return {"messages": self.llm.invoke(state["messages"])}
