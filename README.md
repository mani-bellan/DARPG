# DARPG Chatbot

This project is to develop an AI-driven Chatbot which is Ministry Specific to help the Citizens to resolve their common queries related to filing a Grievance in the CPGRAMS portal (https://pgportal.gov.in) and expedite smooth submission of grievances.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* Generate your API Key : I have the details in my blog : https://medium.com/@mani.bellan/introduction-to-gemini-ai-fe16b1bbedfe
* Update the key in the config.yaml file within config folder. 
* Note - This is assigned per user and should not be shared publicly.


### Installing

Create a python virtual environment and post it is activated, install the libraries. Tested on python 3.10 onwards
Run the below commands for this
```python
git clone https://github.com/mani-bellan/DARPG
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

* Once the libraries are installed, test the code by running it on the terminal
 ```python
streamlit run GrievanceRedressal.py
```
* You can pick some sample questions to be asked from ChatQueries.txt

## Built Using
[![Built Using](https://skillicons.dev/icons?i=python,vscode&perline=3)](https://skillicons.dev)
[![Built Using](https://raw.githubusercontent.com/rlew631/rlew631/b09a7af3f30f8b5a5428dbeb07b9021622018685/red_streamlit.svg)](https://streamlit.io/)


## Resources Used
* CategoryCode_Mapping_V2.xlsx provided by NDSAP as a part of DARPG Hackathon 2024.
* Gemini LLM Model

## Authors

* **Manikandan Bellan** - *Team Lead*  - [Mani Bellan](https://github.com/mani-bellan/)
* **Anita Agrawal**  - *Developer*
* **Agni Srinivasan** *Devops and Documentation* - [Agni](https://github.com/agnisrini/agnisrini)

## Acknowledgments

* https://github.com/krishnaik06 for his video on building chatbot on PDFs using Gemini AI

