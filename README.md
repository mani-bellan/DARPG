# DARPG Chatbot

This project is to develop an AI-driven Chatbot which is Ministry Specific to help the Citizens to resolve their common queries related to filing a Grievance in the CPGRAMS portal (https://pgportal.gov.in) and expedite smooth submission of grievances.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* Generte your API Key : 
        * I have explained the process on my blog : https://medium.com/@mani.bellan/introduction-to-gemini-ai-fe16b1bbedfe

* Update the key in the config.yaml file


### Installing

* Create a python virtual environment and post it is activated, install the libraries. Run the below commands for this
        * python3 -m venv .venv
        * source .venv/bin/activate
        * pip install -r requirements.txt

## Running the tests

* Once the libraries are installed, test the code by running it on the terminal
        * streamlit run GrievanceRedressal.py

* You can pick some sample questions to be asked from ChatQueries.txt

## Built Using
[![Built Using](https://skillicons.dev/icons?i=python,vscode&perline=3)](https://skillicons.dev)

## Authors

* **Manikandan Bellan** - *Initial work* - [Mani Bellan](https://github.com/mani-bellan/)
* **Anita Agrawal**  
* **Agni Srinivasan** 

## Acknowledgments

* https://github.com/krishnaik06 for his video on building chatbot on PDFs using Gemini AI

