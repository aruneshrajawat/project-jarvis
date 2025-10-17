#import requests

# Gemini Pro API key
GEMINI_API_KEY = "AIzaSyCb52Oq6d3gwnlX_nm_ZPIauoraY5uojnQ"
GEMINI_API_URL =  "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-turbo:generateText"

# Prompt to send
prompt = "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. User: what is coding?"

# Request headers and body
headers = {
    "Authorization": f"Bearer {GEMINI_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "prompt": prompt,
    "maxOutputTokens": 300
}

# Call Gemini Pro REST API
try:
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    print(result['candidates'][0]['output'])
except Exception as e:
    print(f"Error: {e}")
