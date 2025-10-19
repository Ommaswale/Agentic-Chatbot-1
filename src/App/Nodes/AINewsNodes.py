import json
from langchain_groq import ChatGroq
from typing_extensions import List
from src.App.State.States import NewsDocument
from src.App.State.States import AINewsState
import streamlit as st
from tavily import TavilyClient

class FetchNews:
    def __init__(self):
        self.client = TavilyClient()
        
    def __call__(self, state: AINewsState) -> AINewsState:
        query = self.build_query(state['timeframe'])
        response = self.client.search(query, max_results=50)
        results = response.get('results', [])
        print(f"----------------------------FETCHED DOCUMENTS--------------------------")
        docs: List[NewsDocument] = []
        for r in results:
            docs.append({
                "title": r.get("title", "Untitled"),
                "content": r.get("content", ""),
                "date": r.get("published_date", "Unknown"),
                "url": r.get("url", "")
            })
        
        state['documents'] = docs
        return state

    @staticmethod
    def build_query(timeframe: str) -> str:
        tf_map = {
            "Daily": "past 24 hours",
            "Weekly": "past week",
            "Monthly": "past month",
            "Year": "past year"
        }
        print(f"----------------------{timeframe}------------------------")
        return f"Latest global news in politics, economy, finance, and technology from the {tf_map.get(timeframe, 'recent period')}"

class PerArticleSummarizer:
    def __init__(self):
        model = st.session_state['selected_llm']
        self.llm = ChatGroq(model=model)

    def __call__(self, state: AINewsState) -> AINewsState:
        print(f"----------------------ENTERED PERARTICLESUMMARIZER------------------------")
        summaries = []
        for doc in state['documents']:
            prompt = f"""
            Summarize this article in 2-3 sentences.
            Title: {doc['title']}
            Date: {doc['date']}
            URL: {doc['url']}
            Content: {doc['content']}
            """
            resp = self.llm.invoke(prompt)
            summaries.append(
                f"Title: {doc['title']}\nDate: {doc['date']}\nURL: {doc['url']}\nSummary: {resp.content}"
            )
        
        state['per_article_summaries'] = summaries
        return state

class Synthesizer:
    def __init__(self):
        model = st.session_state['selected_llm']
        self.llm = ChatGroq(model=model)

    def __call__(self, state: AINewsState) -> AINewsState:
        print(f"----------------------ENTERED SYNTHESIZER------------------------")
        joined = "\n\n".join(state['per_article_summaries'])
        prompt = f"""
        You are a news analyst. Here are {state['timeframe']} per-article summaries:

        {joined}

        Please synthesize them into a section wise summary containing points instead of paragraph with URL as source and Date:
        - Politics
        - Economy
        - Finance
        - Technology

        """
        resp = self.llm.invoke(prompt)
        print(f"----------------------GOT RESPONSE FROM SYNTHESIZER------------------------")
        state['summary'] = resp.content
        return state



# class SummarizeNews:
#     def __init__(self):
#         model = st.session_state['selected_llm']
#         self.llm = ChatGroq(model=model)
    
#     def __call__(self, state: AINewsState):
#         docs = state['documents']
#         docs_text = "\n\n".join(
#             f"Title: {doc['title']}\nDate: {doc['date']}\nURL: {doc['url']}\nContent: {doc['content']}"
#             for doc in docs
#         )

#         prompt = f"""
#         Summarize the following {state['timeframe']} global news articles.

#         ### Output format requirements:
#         - Return JSON list with keys: `category`, `title`, `url`, `summary`
#         - Categories: Politics, Economy, Finance, Technology
#         - Only include relevant categories.
#         - Do **not** add any text outside the JSON.

#         Articles:
#         {docs_text}
#         """

#         # Get model response
#         response = self.llm.invoke(prompt)

#         # Try parsing the JSON safely
#         try:
#             summaries = json.loads(response.content)
#         except json.JSONDecodeError:
#             summaries = []
#             st.warning("⚠️ Could not parse model response as JSON.")

#         # Group by category
#         grouped = {}
#         for item in summaries:
#             cat = item.get("category", "Uncategorized")
#             grouped.setdefault(cat, []).append(item)

#         # Generate Markdown output
#         markdown_output = []
#         category_emojis = {
#             "Politics": "🏛️",
#             "Economy": "🌍",
#             "Finance": "🏦",
#             "Technology": "💻",
#         }

#         for category in ["Politics", "Economy", "Finance", "Technology"]:
#             emoji = category_emojis.get(category, "")
#             markdown_output.append(f"### {emoji} {category}")
#             articles = grouped.get(category, [])
#             if not articles:
#                 markdown_output.append("No dedicated articles this period.\n")
#             else:
#                 for a in articles:
#                     markdown_output.append(
#                         f"- **{a['title']}**  \n"
#                         f"[Source link]({a['url']})  \n"
#                         f"{a['summary']}\n"
#                     )

#         formatted_summary = "\n".join(markdown_output)
#         state['summary'] = formatted_summary
#         return state