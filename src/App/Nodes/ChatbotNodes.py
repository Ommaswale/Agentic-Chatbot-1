from langchain_core.prompts import ChatPromptTemplate
from src.App.State.States import ChatbotState
import streamlit as st
from langchain_groq import ChatGroq

class Chatbot:
    def __init__(self):
        model = st.session_state['selected_llm']
        self.llm = ChatGroq(model=model)

    def __call__(self, state: ChatbotState):
        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', """You are a helpful assistant that will answer the questions"""),
                ('placeholder', "{messages}")
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke({'messages': state['messages']})
        return {'messages': [response]}