from src.App.Nodes.ChatbotNodes import Chatbot
from src.App.Nodes.AINewsNodes import FetchNews, PerArticleSummarizer, Synthesizer
import streamlit as st
from langgraph.graph import StateGraph, START, END
from src.App.State.States import AINewsState, ChatbotState

class GraphBuilder:
    def build_graph(self):
        if st.session_state['selected_usecase'] == 'AI News':
            graph = self.ai_news_graph()
            return graph
        
        if st.session_state['selected_usecase'] == 'Chatbot':
            graph = self.chatbot_graph()
            return graph
        
    @staticmethod
    def ai_news_graph():
        fetch_news = FetchNews()
        per_article_summarizer = PerArticleSummarizer()
        synthesizer = Synthesizer()

        graph = StateGraph(AINewsState)

        graph.add_node("fetch_news", fetch_news)
        graph.add_node("per_article_summarizer", per_article_summarizer)
        graph.add_node("synthesizer", synthesizer)

        graph.add_edge(START, "fetch_news")
        graph.add_edge("fetch_news", "per_article_summarizer")
        graph.add_edge("per_article_summarizer", "synthesizer")
        graph.add_edge("synthesizer", END)

        app = graph.compile()
        return app
    
    @staticmethod
    def chatbot_graph():
        chatbot = Chatbot()

        graph = StateGraph(ChatbotState)
        graph.add_node('chatbot', chatbot)
        graph.add_edge(START, 'chatbot')
        graph.add_edge('chatbot', END)

        app = graph.compile()
        return app