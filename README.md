## InterviewGPT

WIP 

> Your personal interview assistant companion

## Setup 

Setting up Development:

> Assuming you have Python 3.9+, and have installed poetry

- `git clone https://github.com/ericz99/interview-gpt.git <desired dest>`

- Run `poetry install` to install all dependency

- Initialize environment `poetry shell`

- How to run?
    - You can run with web / server
        - Navigate both `/backend/interview_gpt/server` and `/web`
            - On backend run `uvicorn main:app --reload`
            - On web run `pnpm run dev`

    - Or just run the core feature
        - Navigate both `/backend/interview_gpt/core`
            - Run `poetry run python main.py`

**API Key**

- .env file:
    - Create a copy of `.env.template` named `.env`
    - Add your OPENAI_API_KEY in .env

## Development

- This is currently project not optimized for performance as of now. 
- Working on writing a simple api to create new instance of recorders, and new session
- trying to add VAD (Voice activity detection) instead of relying on RMS
- currently this can only spin up one instance of recorder, and it uses socketio to send data from backend to client
- sometime theres like a delay when speaking to the mic, then couple second later it process the audio data

tldr: not slow nor fast, but works good and transcription is on point. Needs optimized using VAD (Voice activity detection)

## Usage

After running the script, the program will start listening to system audio (eg: Speaker), and will record + create .wav file + transcript for you. After,
the AI will read your .wav to create a transcript then will help you answer question or response back about the transcript.

![pic](/assets/pic1.png)

