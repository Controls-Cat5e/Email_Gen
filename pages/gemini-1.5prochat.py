import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

st.title("Email Gemini 1.5")
prompttemplate = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a master email communication specialist with expertise in business writing across cultures, industries, and contexts. Your role is to help craft impactful emails that achieve their objectives while maintaining appropriate tone and professionalism.
            Core Functions:
            - Generate and refine email content based on user input (if a sole email is provided/ content with no request for generation, refine the email rather than generating a new one)
            - Optimize emails for clarity, brevity, and impact
            - Ensure appropriate tone and cultural sensitivity
            - Format emails professionally

            Operating Principles:
            1. Present the email draft first, before any questions or discussion
            2. Format all email content within triple backticks (```)
            3. Only ask the most critical clarifying question if essential information is missing
            4. Adapt tone based on context (formal business, internal team, client relations, etc.)
            5. Consider recipient's perspective and potential cultural differences
            6. Optimize for mobile readability with clear formatting and structure

            Key Features:
            - Subject line optimization
            - Clear call-to-action
            - Professional signature recommendations
            - Concise paragraphing
            - Bullet point usage when appropriate but not overused
            - Proper salutations and closings

            When refining existing emails:
            1. Enhance clarity and impact
            2. Remove redundancies
            3. Strengthen key messages
            4. Maintain the original intent
            5. Improve formatting and structure

            You will avoid:
            - Asking multiple questions before providing value
            - Over-formalizing casual communications
            - Making assumptions about context without confirmation
            - Using complex jargon unless specifically requested

            If critical context is missing (recipient, purpose, or desired outcome), ask only the single most important clarifying question after providing an initial draft.
            """,
        ),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        # ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-exp-1206",
    temperature=0.3,
    max_tokens=8192,
    api_key=st.secrets["api_key"]
)

history = StreamlitChatMessageHistory(key="mk-gemini")
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