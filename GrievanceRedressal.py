import os
import yaml
import google.generativeai as genai
import base64
import pandas as pd
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI 
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from st_aggrid import AgGrid, GridOptionsBuilder

def initialize_ai_env():
    with open("config/config.yaml", "r") as f:
        config = yaml.full_load(f)
        apikey = config['gemini']['api_key']
        os.environ['GOOGLE_API_KEY'] = apikey
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

class grievanceRedressal:
    llm_resp=''
    chat_history=''
    inp_query=''
    department=''
    def __init__(self,st_obj):
        self.st_obj=st_obj
    
    def add_bg_from_local(self,image_file):

        with open(image_file, "rb") as image_file:
            
           encoded_string = base64.b64encode(image_file.read())
           st.markdown(f"""<style>.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});background-size: cover}}</style>""",unsafe_allow_html=True)

    def initialize_ui_sidebar(self):
        with self.st_obj.sidebar:    

           self.st_obj.sidebar.image("resources/DARPG_Logo.jpg", use_column_width=True)
           "**Welcome to DARPG Chatbot**"
           self.st_obj.text_area(label="**Instructions**",value="1. This chatbot can answer your questions related Public Grievances \n2. If you know the department, select it from the dropdown and ask questions related to the department\n3. If you do not know, leave the department as it is and you can ask any general queries about Grievance redressal process", height=130)
           self.st_obj.text_area(label="**Note**",value="The list of ministry/department is provided and when selected will help you with the categories and subcategories of complaints you can raise under the respective ministry/department.\nThis is for informational purpose to help you select the righ category/subcategory", height=135)
    
    def initialize_ui_categories(self):
        df = pd.read_csv('data/Complaint_Category.csv')
        #print(df.columns)
        required_df = df[["Category","ParentCategory","OrgCode"]].sort_values(by=['Category'])
        new_row=["All",np.nan,"ALL"]
        required_df.loc[len(required_df)]=new_row
        new_row1=["All","All","ALL"]
        required_df.loc[len(required_df)]=new_row1
        required_df_1=required_df[required_df['ParentCategory'].isna()].sort_values(by=['Category'])
        #print(required_df_1)

        # Create the primary dropdown for Category and selected value is assigned to var
        selected_category = self.st_obj.selectbox("Select Department/Ministry for your Queries", required_df_1['Category'].unique())
        
        # Filter the dataframe based on the selected category
        filtered_df = required_df[required_df['ParentCategory'] == selected_category]
        selected_org_code=filtered_df["OrgCode"].unique()[0]
        #print(selected_org_code)
        self.department=selected_category
        selected_sub_category=self.st_obj.selectbox("Complaint categories under "+self.department, filtered_df['Category'].unique())
        #print(selected_sub_category)
        sub_category_df=required_df[(required_df['ParentCategory']==selected_sub_category) &(required_df["Category"]!=selected_sub_category) & (required_df["OrgCode"]==selected_org_code)]
        sub_category_df=sub_category_df[["Category","ParentCategory"]]
        
        if self.department !='All':
            # Create a dictionary for dependent dropdown options
            dependent_dropdown_options = {'options': sub_category_df['Category'].unique().tolist(),'default': 'Others'  }
            grid_options = GridOptionsBuilder.from_dataframe(sub_category_df).build()
            AgGrid(sub_category_df, gridOptions=grid_options, data_editor=dependent_dropdown_options, height=150,fit_columns_on_grid_load=True )

    def get_input_query(self):
        user_question = self.st_obj.text_input("**How can I help you today?**")
        
        self.inp_query=user_question

    def initialize_ui(self):
        self.st_obj.set_page_config("DARPG Chatbot")
        self.st_obj.header("Dept of Adminstrative Reforms & Public Grievances Chatbot")
        self.add_bg_from_local('resources/flag.png') 
        self.initialize_ui_categories()
        self.initialize_ui_sidebar()
    def return_out(self):   

        if self.department !='All':
            prompt = PromptTemplate(input_variables=["concept"], template="Answer to the ask {concept} from "+self.department+" Department")
        else:
            prompt = PromptTemplate(input_variables=["concept"], template="Answer the {concept} from all DARPG Departments")
     
    
        llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)
        chain = LLMChain(llm=llm, prompt=prompt)

        #concatenate history
        self.chat_history +="**You asked :**"
        self.chat_history +=self.inp_query
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        st.session_state['chat_history'].append(("**You asked**", self.inp_query))


        #output = chain.invoke(self.inp_query)
        print(self.chat_history)
        output = chain.invoke(self.chat_history)
        
        #capture response in history text
        self.chat_history +="**Bot answered:**"
        self.chat_history +=output["text"]
        print(self.chat_history)

        return output["text"]

    def process(self):
        if self.st_obj.button("Retreive Information"):

            with self.st_obj.spinner("Retrieving Information..."):
                llm_resp = self.return_out()
                self.st_obj.session_state['chat_history'].append(("**Bot asnwered**", llm_resp))
                self.st_obj.write(llm_resp)

                self.st_obj.subheader("The Chat History is")
                for role, text in st.session_state['chat_history']:
                    self.st_obj.write(f"{role}: {text}") 
        

def main():
    initialize_ai_env()
    grievanceRedressal_obj=grievanceRedressal(st)
    grievanceRedressal_obj.initialize_ui()
    grievanceRedressal_obj.get_input_query()
    grievanceRedressal_obj.process()
    


if __name__=="__main__":
    main()