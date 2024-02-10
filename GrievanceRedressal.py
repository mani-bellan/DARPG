import os
import yaml
import google.generativeai as genai
import base64
import pandas as pd

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI 
from langchain_openai import OpenAI
import streamlit as st

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from st_aggrid import AgGrid, GridOptionsBuilder

def initialize_ai_env():
    with open("config/config.yaml", "r") as f:
        config = yaml.full_load(f)
        apikey = config['gemini']['api_key']
        os.environ['GOOGLE_API_KEY'] = apikey
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

class grievanceRedressal:
    def __init__(self,st_obj,inp_query,department):
        self.st_1=st_obj
        self.inp_query=''
        self.department=''
    
    def add_bg_from_local(self,image_file):

        with open(image_file, "rb") as image_file:
            
           encoded_string = base64.b64encode(image_file.read())
           st.markdown(f"""<style>.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});background-size: cover}}</style>""",unsafe_allow_html=True)

    def initialize_ui_sidebar(self):
        with self.st_1.sidebar:    

           self.st_1.sidebar.image("resources/DARPG_Logo.jpg", use_column_width=True)
           "**Welcome to DARPG Chatbot**"
           self.st_1.text_area(label="**Instructions**",value="1. This chatbot can answer your questions related Public Grievance\n2. If you know the department, select it from the dropdown and ask questions related to the department\n3. If you do not know, leave the department as All and you can ask any general queries about Grievance redressal process", height=130)
           self.st_1.text_area(label="**Note**",value="The list of ministry/department is provided and when selected will help you with the categories and subcategories of complaints you can raise under the respective ministry/department.\nThis is for informatonal purpose to help you select the righ category/subcategory", height=135)
    
    def initialize_ui_categories(self):
        df = pd.read_csv('data/Complaint_Category.csv')
        print(df.columns)
        required_df = df[["Category","ParentCategory","OrgCode"]].sort_values(by=['Category'])
        print(required_df.columns)
        required_df_1=required_df[required_df['ParentCategory'].isna()].sort_values(by=['Category'])

        # Create the primary dropdown for Category and selected value is assigned to var
        selected_category = self.st_1.selectbox("Select Department/Ministry for your Queries", required_df_1['Category'].unique())
        
        # Filter the dataframe based on the selected category
        filtered_df = required_df[required_df['ParentCategory'] == selected_category]
        selected_org_code=filtered_df["OrgCode"].unique()[0]
        #print(selected_org_code)
        self.department=selected_category
        selected_sub_category=self.st_1.selectbox("Complaint categories under "+self.department, filtered_df['Category'].unique())
        #print(selected_sub_category)
        sub_category_df=required_df[(required_df['ParentCategory']==selected_sub_category) &(required_df["Category"]!=selected_sub_category) & (required_df["OrgCode"]==selected_org_code)]
        sub_category_df=sub_category_df[["Category","ParentCategory"]]
        
        # Create a dictionary for dependent dropdown options
        dependent_dropdown_options = {'options': sub_category_df['Category'].unique().tolist(),'default': 'Others'  }
    
    
        grid_options = GridOptionsBuilder.from_dataframe(sub_category_df).build()
        AgGrid(sub_category_df, gridOptions=grid_options, data_editor=dependent_dropdown_options, height=150,fit_columns_on_grid_load=True )

    def get_input_query(self):
        user_question = self.st_1.text_input("**How can I help you today?**")
        
        self.inp_query=user_question

    def initialize_ui(self):
        self.st_1.set_page_config("DARPG Chatbot")
        self.st_1.header("Dept of Adminstrative Reforms & Public Grievances Chatbot")
        self.add_bg_from_local('resources/flag.png') 
        self.initialize_ui_categories()
        self.initialize_ui_sidebar()
    def return_out(self):   

        if self.department !='All':
            prompt = PromptTemplate(input_variables=["concept"], template="Answer to the ask {concept} from "+self.department+" Department")
        else:
            prompt = PromptTemplate(input_variables=["concept"], template="Answer the {concept} from all DARPG Department")
     
    
        llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)
        chain = LLMChain(llm=llm, prompt=prompt)
    
        output = chain.invoke(self.inp_query)
        return output["text"]

    def process(self):
        if self.st_1.button("Retreive Information"):

            with self.st_1.spinner("Retrieving Information..."):
               self.st_1.write(self.return_out())
    

        
        

def main():
    initialize_ai_env()
    grievanceRedressal_obj=grievanceRedressal(st,'','')
    grievanceRedressal_obj.initialize_ui()
    grievanceRedressal_obj.get_input_query()
    grievanceRedressal_obj.process()
    


if __name__=="__main__":
    main()
    
        