import os
from dotenv import load_dotenv
#
# load environment variables from .env file
load_dotenv()
#
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import google.generativeai as genai

# Configure with your API key (obtain from your Gemini account)
genai.configure(api_key=GOOGLE_API_KEY)

# Specify the model name (replace with the desired model)
model_name = "gemini-pro"  # Choose from available models

# Create a generative model object
model = genai.GenerativeModel(model_name)

# Prompt for text generation
prompt = "What is the meaning of life?"

# Generate text content
response = model.generate_content(prompt)

# Print the generated text
print(response.text)