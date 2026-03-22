# Voice-Based AI Campus Event Assistant

This project is a voice-based AI assistant for the Visvesvaraya Technological University (VTU) campus event. It uses Asterisk for telephony, Google Cloud Speech-to-Text and Text-to-Speech, and Google's Gemini Pro for conversational AI.

## Project Structure

- `main.py`: A FastAPI application that serves the Gemini Pro model's responses.
- `Dockerfile`: To containerize the FastAPI application.
- `requirements.txt`: Python dependencies for the FastAPI app.
- `asterisk-setup/`: Contains the Asterisk configuration files and the AGI script.

## Setup and Usage

### Prerequisites

- A running Asterisk server.
- Google Cloud Platform project with Speech-to-Text and Text-to-Speech APIs enabled.
- A service account key for GCP with the necessary permissions.
- A Gemini API key.

### 1. Configure Asterisk

The `asterisk-setup` directory contains the necessary configuration files for Asterisk. Refer to the `README.md` in that directory for more details.

### 2. Configure the AI Backend

1.  **Update `main.py`:**
    -   Replace `"change this and add your api key here"` with your Gemini API key.

2.  **Update `asterisk-setup/ai_bridge.py`:**
    -   Replace `"YOUR_CLOUD_RUN_URL/generate-response"` with the URL of your deployed FastAPI application.
    -   Place your GCP service account key at `/etc/asterisk/gcp_key.json` on your Asterisk server.

3.  **Update `asterisk-setup/pjsip.conf`:**
    -   Replace `YOUR_VM_EXTERNAL_IP` with the external IP address of your Asterisk server.
    -   Set a secure password for the SIP endpoint.

### 3. Run the AI Backend

The AI backend is a FastAPI application that can be run using Docker.

```bash
# Build the Docker image
docker build -t voice-backend .

# Run the Docker container
docker run -d -p 8080:8080 --name voice-backend voice-backend
```

The application will be available at `http://localhost:8080`.

## How it Works

1.  A user dials into the Asterisk server.
2.  The `extensions.conf` dialplan answers the call and initiates the `ai_bridge.py` AGI script.
3.  The `ai_bridge.py` script records the user's speech, sends it to Google Cloud Speech-to-Text for transcription.
4.  The transcribed text is sent to the FastAPI backend (`main.py`).
5.  The FastAPI backend uses the Gemini model to generate a response.
6.  The response text is synthesized into speech by Google Cloud Text-to-Speech via the `ai_bridge.py` script.
7.  The synthesized audio is played back to the user.
8.  The loop continues until the user hangs up or says a goodbye phrase.
