import os
import google.generativeai as genai
import PIL.Image
import streamlit as st
import yaml
from PyPDF2 import PdfRead

#Configure your API Key
with open("config.yaml", "r") as f:
    config = yaml.full_load(f)

apikey = config['gemini']['api_key']

os.environ['GOOGLE_API_KEY'] = apikey
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

#Input the image
pic = PIL.Image.open('CPGRAMS.jpg')

#Select the model to be use in the app
model = genai.GenerativeModel('gemini-pro-vision')

#Initiative the chat
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = model.generate_content([question,pic])
    return response

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("DARPG Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("How can i help you: ", key="input")
submit = st.button("Submit")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("Answer is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
#st.subheader("The Chat History is")

#for role, text in st.session_state['chat_history']:
#    st.write(f"{role}: {text}")
#response = model.generate_content(["Explain what this picture conveys",pic])

#print(response.text)