import os
import logging
from fastapi import FastAPI, Request
from datetime import datetime
import pytz
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# --- CONFIGURATION ---
# Replace with your actual Gemini API Key from Google AI Studio
GEMINI_API_KEY = "REPLACE_ME"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- THE NEW SYSTEM PROMPT ---
def get_system_prompt():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p")
    
    return f"""You are 'Nova', a highly intelligent and friendly personal AI assistant. 
The current time is {current_time}.

CORE RULES FOR VOICE CONVERSATION:
1. CONCISENESS: Your responses are being read aloud over a phone line. Keep answers to 1 or 2 short, punchy sentences maximum.
2. NO FORMATTING: Do not use bullet points, bold text, asterisks, or emojis. Use only natural, spoken punctuation.
3. TONE: Be helpful, clever, and energetic. 
4. CONVERSATIONAL: Speak as if you are on a live phone call with a human.
"""

@app.post("/generate-response")
async def generate_response(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        full_prompt = f"{get_system_prompt()}\n\nThe user says: '{user_text}'. Respond now:"
        
        response = model.generate_content(full_prompt)
        return {"response": response.text.strip()}
        
    except Exception as e:
        logging.error(f"Gemini API Error: {str(e)}")
        return {"response": "I encountered a processing error on the backend."}
