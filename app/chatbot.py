import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self):
        # Get Ollama URL from environment variable
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/")  # Fallback to default URL

    def get_response(self, text: str) -> str:
        # Request payload for the Llama model
        payload = {
            "model": "llama3.1",  # Specify the Llama 3.1 model
            "input": text,  # The user's message
        }
        
        # Send request to Ollama server
        response = requests.post(self.ollama_url, json=payload)
        
        # If the response is successful, extract and return the generated message
        if response.status_code == 200:
            return response.json().get("text", "No response from model.")
        else:
            return f"Error: {response.status_code} - {response.text}"