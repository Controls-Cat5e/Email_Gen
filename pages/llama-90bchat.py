import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

st.title("Email Gen-Llama 70B V1.0")
prompttemplate = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert in writing clear, professional, and effective emails. Your task is to assist the user in creating high-quality emails. Before assuming any information, ask specific clarifying questions to ensure you fully understand the user's goals, context, and desired tone. Focus on maximizing clarity, maintaining an appropriate tone, and achieving the email's purpose. Keep your responses of emails/templates at a suitable length and always guide the user step-by-step if needed.
            """,
        ),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        # ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.3,
    max_tokens=8000,
    api_key=st.secrets["groq_key"]
)

history = StreamlitChatMessageHistory(key="mk-llama-90b")
text = st.chat_input(placeholder="Type your message here...")
if len(history.messages) == 0:
    history.add_ai_message("Welcome to the Email Gen-Llama 90B V1.0! How can I help you today?")
    
for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)
    
if prompt :=text:
    with st.chat_message("user"):
        st.write(prompt)
        history.add_user_message(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        formatted_prompt = prompttemplate.format_messages(input=prompt, history=history.messages)
        response = st.write_stream(llm.stream(formatted_prompt))
        history.add_ai_message(response)     