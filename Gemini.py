import os
import google.generativeai as genai
import yaml

with open("config.yaml", "r") as f:
    config = yaml.full_load(f)

apikey = config['gemini']['api_key']

os.environ['GOOGLE_API_KEY'] = apikey
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("List the top 5 generative AI models")

print(response.text)