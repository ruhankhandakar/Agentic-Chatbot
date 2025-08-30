import streamlit as st
from ui.streamlit_ui.loadui import LoadStreamlitUI

def load_langgraph_agentic_ai_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: failed to load user input from the UI")
        return
    
    user_message = st.chat_input("Enter your message")


if __name__ == "__main__":
    load_langgraph_agentic_ai_app()
