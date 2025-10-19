from langchain_core.messages import BaseMessage
from typing import TypedDict
from typing_extensions import Annotated, List
from langgraph.graph.message import add_messages

class ChatbotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

class NewsDocument(TypedDict):
    title: str
    content: str
    date: str
    url: str

class AINewsState(TypedDict):
    timeframe: str
    documents: List[NewsDocument]
    per_article_summaries: List[str]
    summary: str