import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyDwG6IB5YIGXdOy1xb7l71eEk8EAjJHPRw"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("List the top 5 generative AI models")

print(response.text)
