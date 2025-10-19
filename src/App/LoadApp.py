import os
import streamlit as st
from src.App.UI.streamlit.LoadUI import LoadUI
from src.App.Graph.GraphBuilder import GraphBuilder
from src.App.UI.streamlit.DisplayResults import DisplayResult

class LoadApp:
    def load_app(self):

        # Initialize session state keys if they don't exist
        if "LoadChatbot" not in st.session_state:
            st.session_state.LoadChatbot = False
        if "LoadAINews" not in st.session_state:
            st.session_state.LoadAINews = False
        if "graph" not in st.session_state:
            st.session_state.graph = None
        if "user_message" not in st.session_state:
            st.session_state.user_message = None
        if "selected_llm" not in st.session_state:
            st.session_state.selected_llm = None
        if "selected_usecase" not in st.session_state:
            st.session_state.selected_usecase = None
        if "messages" not in st.session_state:
            st.session_state.messages = []

        ui = LoadUI()
        user_controls = ui.load_ui()
        user_message = None

        # Now update to the new selection
        st.session_state.selected_usecase = user_controls['SELECTED_USECASE']
        st.session_state.selected_llm = user_controls['SELECTED_LLM']

        # Always rebuild graph if needed
        if (
            st.session_state.graph is None
            or st.session_state.selected_usecase != user_controls['SELECTED_USECASE']
        ):
            st.session_state.graph = GraphBuilder().build_graph()

        if st.session_state.LoadChatbot or st.session_state.LoadAINews:
            os.environ['GROQ_API_KEY'] = user_controls['GROQ_API_KEY']

            if st.session_state.LoadChatbot:
                user_message = st.chat_input("Enter your message: ")

            if st.session_state.LoadAINews:
                os.environ['TAVILY_API_KEY'] = user_controls['TAVILY_API_KEY']
                user_message = user_controls['TIMEFRAME']

            st.session_state.user_message = user_message

        if user_message:
            if st.session_state.graph is None:
                st.error("Please load the chatbot before giving input")
                return
            try:
                DisplayResult().display_result()
            except Exception as e:
                st.error(f"Exception: {e}")