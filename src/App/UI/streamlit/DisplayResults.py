from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

class DisplayResult:
    def display_result(self):
        graph = st.session_state.graph
        user_message = st.session_state.user_message
        st.session_state['messages'].append(HumanMessage(content=user_message))

        if st.session_state.selected_usecase == 'Chatbot':
            with st.spinner("Thinking..."):
                try:
                    # Pass full conversation to the graph
                    result = graph.invoke({"messages": st.session_state["messages"]})

                    # Extract AI response
                    if isinstance(result, dict) and "messages" in result:
                        ai_response = result["messages"][-1].content
                    elif isinstance(result, dict) and "output" in result:
                        ai_response = result["output"]
                    else:
                        ai_response = str(result)

                    # Append AI's message
                    st.session_state["messages"].append(AIMessage(content=ai_response))

                except Exception as e:
                    st.error(f"Exception: {e}")

            st.markdown("### 💬 Chat")
            for msg in st.session_state["messages"]:
                if isinstance(msg, HumanMessage):
                    st.markdown(f"🧑 **You:** {msg.content}")
                elif isinstance(msg, AIMessage):
                    st.markdown(f"🤖 **AI:** {msg.content}")

        if st.session_state.selected_usecase == 'AI News':
            with st.spinner("Fetching and summarizing news..."):
                try:
                    result = graph.invoke({'timeframe': user_message})

                    if isinstance(result, dict) and "summary" in result:
                        st.markdown(result["summary"], unsafe_allow_html=True)
                    else:
                        st.markdown(str(result))
                except Exception as e:
                    st.error(f"Exception: {e}")
