from langchain_groq import ChatGroq

from state.state import State

class ChatBotWithToolNode:
    def __init__(self, llm_model: ChatGroq):
        self.llm = llm_model
    
    def create_chatbot(self, tools):
        """Returns a chatbot node function
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """ChatBot logic for processing the input state and returning a response
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node