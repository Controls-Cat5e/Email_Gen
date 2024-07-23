import streamlit as st
from meta_ai_api import MetaAI
st.set_page_config(page_title="Prototype-TextGen")
# palm.configure(api_key=st.secrets["api_key"])




def metaGen(prompt):
    ai = MetaAI()
    response = ai.prompt(message=prompt)
    return response['message']



st.title("Hello , Welcome to Meta Text Generator!")
option = st.radio("Please select the type of your text", ("Email", "Message"))
content = st.text_area("Please type the content of your email here", height=100)
tone = st.selectbox("Please select the tone of your email", ("Professional email short","Formal", "Informal", "Casual", "Business", "Informative", "question", "neutral", "other"))

if tone == "other":
    tone = st.text_input("Please type the tone of your email here")
    
# creativity = st.slider("Please select the creativity of your email", 0, 100, 33)/100
# outputSize = st.slider("Please select the maximum length of your email", 0, 1024, 250)
# suggestedSize = st.slider("Please select the suggested length of your email (0 will be regarded as you have no suggestion and the LLM will autopick)", 0, 1024, 0)

if st.button("Generate Email"):
    if option == "Email":
        with st.spinner('Your email is being generated...'):
            prompt = f"""
            You are an expert at writing emails
            You will write the email using this tone: {tone}
            The content of your email is:
            {content}
            you will perform grammar refinements, fix typos and follow the tone above
            """
            st.write(metaGen(prompt))
                

                
            
        st.success('Your email has been generated! 	:star2:')
        st.balloons()

    elif option == "Message":
        with st.spinner('Your message is being generated...'):
            prompt = f"""
            You are an expert at writing SMS/Messages
            You will write the message using this tone: {tone}
            The content of your message is:
            {content}
            you will perform grammar refinements, fix typos and follow the tone above
            """
            st.write(metaGen(prompt))
                
                
            
        st.success('Your message has been generated! 	:star2:')
        st.balloons()