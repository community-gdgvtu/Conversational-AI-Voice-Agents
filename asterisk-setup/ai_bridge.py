#!/usr/bin/env python3
import sys
import os
import requests
from google.cloud import speech
from google.cloud import texttospeech

# Point to the Asterisk-owned GCP key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/asterisk/gcp_key.json"

CLOUD_RUN_URL = "CLOUD_RUN_URL/generate-response"
USER_AUDIO_PATH = "/tmp/user_audio.wav"
AI_RESPONSE_PATH = "/tmp/ai_response.ulaw"
HANGUP_FLAG = "/tmp/hangup.flag"

def log_debug(message):
    sys.stderr.write(f"{message}\n")
    sys.stderr.flush()

def transcribe_audio():
    try:
        if not os.path.exists(USER_AUDIO_PATH) or os.path.getsize(USER_AUDIO_PATH) <= 44:
            return ""
        with open(USER_AUDIO_PATH, "rb") as f:
            content = f.read()
            
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="en-IN", # Optimized for Indian accents
            enable_automatic_punctuation=True
        )
        response = client.recognize(config=config, audio=audio)
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            log_debug(f"DEBUG: Caller said: {transcript}")
            return transcript
        return ""
    except Exception as e:
        log_debug(f"STT Error: {e}")
        return ""

def synthesize_speech(text):
    log_debug(f"DEBUG: AI saying: {text}")
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-H")
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MULAW, 
            sample_rate_hertz=8000
        )
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        with open(AI_RESPONSE_PATH, "wb") as out:
            out.write(response.audio_content)
        os.chmod(AI_RESPONSE_PATH, 0o777) # Ensure Asterisk can read it
    except Exception as e:
        log_debug(f"TTS Error: {e}")

def main():
    mode = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "chat"

    if mode == "intro":
        synthesize_speech("Hi, I am NOVA your personal AI! How can I help you?")
        sys.exit(0)

    user_text = transcribe_audio()
        
    if not user_text:
        ai_text = "I'm sorry, I didn't hear anything. Please speak clearly after the beep."
    else:
        # Smart Hangup Logic
        exit_phrases = ["bye", "goodbye", "hang up", "end call"]
        if any(phrase in user_text.lower() for phrase in exit_phrases):
            synthesize_speech("Goodbye! Thank you for calling.")
            os.system(f"touch {HANGUP_FLAG}") 
            sys.exit(0) 

        # Call AI
        try:
            r = requests.post(CLOUD_RUN_URL, json={"text": user_text}, timeout=10)
            ai_text = r.json().get("response", "Backend error.")
        except Exception:
            ai_text = "Connection timed out."
            
    synthesize_speech(ai_text)

if __name__ == "__main__":
    main()
