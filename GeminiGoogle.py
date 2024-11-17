import streamlit as st
import pprint
import google.generativeai as gemini
st.set_page_config(page_title="Email Gen-V1.0", page_icon=":email:",initial_sidebar_state="expanded")
st.sidebar.title("Email Gen-V1.0")
st.sidebar.success("Please select version above ")

gemini.configure(api_key=st.secrets["api_key"])
models = [m for m in gemini.list_models() if 'generateText' in m.supported_generation_methods]
model = gemini.GenerativeModel('gemini-exp-1114')


temp = 0.7
outputSize = 1000

def geminiGen(prompt, temp, outputSize):
    completion = model.generate_content(
        prompt,
        generation_config=gemini.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        max_output_tokens=outputSize,
        temperature=temp)
    )
    if outputFont == "TextDefault":
        st.markdown(completion.text)
    elif outputFont == "Raw":
        st.code(completion.text)
        
    elif outputFont == "Custom":
        for line in completion.text.splitlines():
            st.markdown(f'<p style="font-family:Courier New;font-size: 16px;">{line}</p>', unsafe_allow_html=True)



st.title("Hello , Welcome to Email Generator V1.0! Now Powered by Gemini.")
option = st.radio("Please select the type of your text", ("Email", "Message"))
content = st.text_area("Please type the content of your email here", height=100)
tone = st.selectbox("Please select the tone of your email", ("Professional email short","Formal", "Informal", "Casual", "Business", "Informative", "question", "neutral", "other"))

if tone == "other":
    tone = st.text_input("Please type the tone of your email here")
    
creativity = st.slider("Please select the creativity of your email", 0, 100, 33)/100
outputSize = st.slider("Please select the maximum length of your email", 0, 2048, 1024)
suggestedSize = st.slider("Please select the suggested length of your email (0 will be regarded as you have no suggestion and the LLM will autopick)", 0, 1024, 0)
outputFont = st.radio("Please select the font of your email (note: custom might be unsafe)",("TextDefault","Raw","Custom") )

if st.button("Generate Email"):
    if option == "Email":
        with st.spinner('Your email is being generated...'):
            if suggestedSize == 0:
                prompt = f"""
                You are an expert at writing emails
                You will write the email using this tone: {tone}
                The content of your email is:
                {content}
                you will perform grammar refinements, fix typos and follow the tone above, return only the email with no other accompanying text
                """
                geminiGen(prompt, creativity, outputSize)

                
            else:
                prompt = f"""
                You are an expert at writing emails
                You will write the email using this tone: {tone}
                The suggested length of the email is: {suggestedSize} words
                The content of your email is:
                {content}
                you will perform grammar refinements, fix typos and follow the tone above, return only the email with no other accompanying text
                """
                geminiGen(prompt, creativity, outputSize)
                
            
        st.success('Your email has been generated! 	:star2:')
        st.snow()

    elif option == "Message":
        with st.spinner('Your message is being generated...'):
            if suggestedSize == 0:
                prompt = f"""
                You are an expert at writing SMS/Messages
                You will write the message using this tone: {tone}
                The content of your message is:
                {content}
                you will perform grammar refinements, fix typos and follow the tone above, return only the message with no other accompanying text
                """
                geminiGen(prompt, creativity, outputSize)
                
            else:
                prompt = f"""
                You are an expert at writing SMS and Messages
                You will write the message using this tone: {tone}
                The suggested length of the message is: {suggestedSize} words
                The content of your message is:
                {content}
                you will perform grammar refinements, fix typos and follow the tone above, return only the message with no other accompanying text
                """
                geminiGen(prompt, creativity, outputSize)
                
            
        st.success('Your message has been generated! 	:star2:')
        st.snow()
