from src.App.UI.config import Config
import streamlit as st

class LoadUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_ui(self):

        st.set_page_config(
            page_title=self.config.get_page_title(),
            layout='wide'
        )

        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecases = self.config.get_usecases()

            self.user_controls['SELECTED_USECASE'] = st.selectbox('Select usecase', usecases)
            self.user_controls['SELECTED_LLM'] = st.selectbox('Select LLM', llm_options)

            if self.user_controls['SELECTED_LLM'] != '--select llm--':
                if st.session_state.selected_llm == None:
                    st.session_state.selected_llm = self.user_controls['SELECTED_LLM']
                self.user_controls['GROQ_API_KEY'] = st.text_input('GROQ_API_KEY', type='password')

            if self.user_controls['SELECTED_USECASE'] == 'Chatbot':
                if st.session_state.selected_usecase == None:
                    st.session_state.selected_usecase = 'Chatbot'
                if st.button("Load Chatbot", use_container_width=True):
                    if self.user_controls['GROQ_API_KEY'] == '':
                        st.error("Please enter GROQ API key")
                    if self.user_controls['SELECTED_LLM'] == '--select llm--':
                        st.error("Please select LLM")
                    self.ResetStates()
                    st.session_state.LoadChatbot = True

            if self.user_controls['SELECTED_USECASE'] =='AI News':
                st.session_state.selected_usecase = 'AI News'
                self.user_controls['TAVILY_API_KEY'] = st.text_input('TAVILY_API_KEY', type='password')

                st.subheader("AI News Explorer")

                with st.sidebar:
                    self.user_controls['TIMEFRAME'] = st.selectbox("Select time frame", ["Daily", "Weekly", "Monthly", "Year"],
                    index=0
                    )
                
                if st.button("Fetch Latest News", use_container_width=True):
                    if self.user_controls['TAVILY_API_KEY'] == '':
                        st.error("Please enter tavily API key")
                    if self.user_controls['GROQ_API_KEY'] == '':
                        st.error("Please enter API key")
                    if self.user_controls['SELECTED_LLM'] == '--select llm--':
                        st.error("Please select LLM")
                    self.ResetStates()
                    st.session_state.LoadAINews = True
        
        return self.user_controls
    
    @staticmethod
    def ResetStates():
        st.session_state.LoadChatbot = False
        st.session_state.LoadAINews = False
        st.session_state.messages = []