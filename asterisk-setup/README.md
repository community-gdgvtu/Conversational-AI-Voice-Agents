# Asterisk Setup

This directory contains the configuration files and scripts for the Asterisk server.

## Files

-   **`ai_bridge.py`**: This is an Asterisk Gateway Interface (AGI) script that acts as the bridge between Asterisk and the AI services. It handles:
    -   Recording the user's voice.
    -   Transcribing the audio using Google Cloud Speech-to-Text.
    -   Sending the transcribed text to the main AI backend.
    -   Receiving the AI's response.
    -   Synthesizing the response text into speech using Google Cloud Text-to-Speech.
    -   Playing the synthesized audio back to the user.

-   **`extensions.conf`**: This is the Asterisk dialplan. It defines how incoming calls are handled. In this project, it:
    -   Answers the call on extension `5000`.
    -   Plays a welcome message.
    -   Enters a loop to record the user's speech and execute the `ai_bridge.py` AGI script.
    -   Checks for a hangup signal from the AGI script to terminate the call.

-   **`pjsip.conf`**: This file configures the PJSIP channel driver for SIP connections. It defines:
    -   The transport settings (UDP).
    -   A SIP endpoint (e.g., `1001`) with authentication details.

## Setup

1.  **Copy Files:**
    -   Copy the contents of `pjsip.conf` and `extensions.conf` to your Asterisk configuration directory (usually `/etc/asterisk/`).
    -   Copy the `ai_bridge.py` script to a suitable location on your Asterisk server, for example, `/usr/local/bin/`. Make sure the script is executable (`chmod +x /usr/local/bin/ai_bridge.py`).

2.  **GCP Credentials:**
    -   Place your Google Cloud Platform service account key file at `/etc/asterisk/gcp_key.json`. The `ai_bridge.py` script is hardcoded to look for the key at this path.

3.  **Reload Asterisk:**
    -   After copying the files, reload the Asterisk configuration:
        ```bash
        sudo asterisk -rx "core reload"
        ```
