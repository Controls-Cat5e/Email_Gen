import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

st.title("Email Gen-Llama 90B V1.0")
prompttemplate = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert at writing emails, please assist the user in writing the best emails possible and ask clarifying questions if needed before assuming information. 
            """,
        ),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        # ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatGroq(
    model="llama-3.2-90b-text-preview",
    temperature=0.3,
    max_tokens=8192,
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