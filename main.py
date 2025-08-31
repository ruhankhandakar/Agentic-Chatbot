import streamlit as st
from dotenv import load_dotenv

from ui.streamlit_ui.loadui import LoadStreamlitUI
from ui.streamlit_ui.display_result import DisplayResultStreamlit
from LLMS.groqllm import GroqLLM
from graph.graph_builder import GraphBuilder

load_dotenv()

def load_langgraph_agentic_ai_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: failed to load user input from the UI")
        return
    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM Model could not be initialized")
                return
            
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No usecase selected")
                return
            
            graph_builder = GraphBuilder(model=model)

            graph = graph_builder.setup_graph(usecase)
            DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()

        except Exception as e:
            st.error(f"Error: {e}")
            raise


if __name__ == "__main__":
    load_langgraph_agentic_ai_app()
