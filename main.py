import streamlit as st
import pprint
import google.generativeai as palm
palm.configure(api_key=st.secrets["api_key"])
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


temp = 0.7
outputSize = 1000

def PaLMgen(prompt, temp, outputSize):
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=temp,
        # The maximum length of the response
        max_output_tokens=outputSize,
    )
    return completion.result



st.title("Hello , Welcome to Email Generator")
content = st.text_area("Please type the content of your email here", height=100)
tone = st.selectbox("Please select the tone of your email", ("Formal", "Informal", "Casual", "Business", "Informative", "question", "neutral", "other"))

if tone == "other":
    tone = st.text_input("Please type the tone of your email here")
    
creativity = st.slider("Please select the creativity of your email", 0, 100, 70)/100
outputSize = st.slider("Please select the maximum length of your email", 0, 5000, 250)
suggestedSize = st.slider("Please select the suggested length of your email (0 will be regarded as you have no suggestion and the LLM will autopick)", 0, 5000, 0)

if st.button("Generate Email"):
    with st.spinner('Your email is being generated...'):
        if suggestedSize == 0:
            prompt = f"""
            You are an expert at writing emails
            You will write the meeting using this tone: {tone}
            The content of your email is:
            {content}
            """
            st.write(PaLMgen(prompt, creativity, outputSize))
            
        else:
            prompt = f"""
            You are an expert at writing emails
            You will write the meeting using this tone: {tone}
            The suggested length of the email is: {suggestedSize} words
            The content of your email is:
            {content}
            """
            st.write(PaLMgen(prompt, creativity, outputSize))
            
        
    st.success('Your email has been generated! 	:star2:')
    st.balloons()
