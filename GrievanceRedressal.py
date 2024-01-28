import streamlit as st
import os
import yaml
import google.generativeai as genai
import base64
import pandas as pd

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


#Configure your API Key
with open("config.yaml", "r") as f:
    config = yaml.full_load(f)

apikey = config['gemini']['api_key']

os.environ['GOOGLE_API_KEY'] = apikey
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Generate text from PDF Files
def get_pdf_text():
    text=""
    for pdf in os.listdir("./data"):
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

# Generate texts chunks from the text created out of PDF Files
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Use Facebook AI Similarity Search(FAISS) and create a local vector store called faiss_index
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Geneerate the lang chain 
def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


# Get the user question as the input and generae the response
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    #print(response)
    st.write("Reply: ", response["output_text"])

# Add background image to the page
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


def main():

    st.set_page_config("Chat PDF")
    st.header("Dept of Adminstrative Reforms & Public Grievances Chatbot")

    user_question = st.text_input("How can I help you today?")

    add_bg_from_local('flag.png') 

    with st.sidebar:    
        st.sidebar.image("DARPG_Logo.jpg", use_column_width=True)
        "Welcome to DARPG Chatbot"
        # Build df.
        df = pd.read_csv('Departments.csv')
        st.selectbox(label='**Select Department**', options=df.Departments,on_change=None,args=None, kwargs=None, placeholder="Choose an option",)
        st.text_area(label="Instructions",value="If you have specific question about the departmet,use the name of the department in the query box along with the question\nEg. Give me contacts of Central Board of Direct Taxes (Income Tax)", height=150)

    if user_question:
        user_input(user_question)

    if st.button("Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text()
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            st.success("Done")


if __name__ == "__main__":
    main()