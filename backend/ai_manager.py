# backend/ai_manager.py
import google.generativeai as genai
from typing import Dict

class AIManager:
    def __init__(self, api_key: str):
        self.setup_gemini_ai(api_key)

    def setup_gemini_ai(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction = """ Act as a professional note-taking assistant. 
         You are given a YouTube video transcript, read it carefully then provide a summary.
         Strictly follow these rules:
         - The language of the summary must match the language of the video transcript
         - The summary must have this structure:
         - Concise summary of the main points
         - Key concepts and ideas
         - Important details and relevant examples
         - Main conclusions and takeaways
         - The summary must be written in a clear, organized manner, using bullet points and a readable structure
         """
        )

    def generate_summary(self, text: str) -> str:
        """Generate summary from text using Gemini AI."""
        response = self.model.generate_content(text)
        return response.text

