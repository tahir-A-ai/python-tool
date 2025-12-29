import google.generativeai as genai
import os
from dotenv import load_dotenv  

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") 
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_response(self, context: str, user_query: str) -> str:
        """
        Constructs the prompt and gets the answer from Gemini.
        """
        
        # The System Prompt (Instructions for the AI)
        prompt = f"""
        You are an expert Senior Software Engineer assisting a developer.
        
        CONTEXT (Code Snippets from the project):
        {context}
        
        USER QUESTION:
        {user_query}
        
        INSTRUCTIONS:
        1. Answer the question based ONLY on the context provided.
        2. If the context doesn't contain the answer, say "I couldn't find relevant code for that in this repository."
        3. Keep the answer concise and technical.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}"