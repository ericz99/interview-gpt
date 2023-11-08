## InterviewGPT

> Your personal interview assistant companion

## Setup 

Setting up Development:

> Assuming you have Python 3.9+, and have installed poetry

- `git clone https://github.com/ericz99/interview-gpt.git <desired dest>`

- Run `poetry install` to install all dependency

- Initialize environment `poetry shell`

- Run main.py `cd interview-gpt/core && poetry run python main.py`

**API Key**

- .env file:
    - Create a copy of `.env.template` named `.env`
    - Add your OPENAI_API_KEY in .env

## Usage

After running the script, the program will start listening to system audio (eg: Speaker), and will record + create .wav file + transcript for you. After,
the AI will read your .wav to create a transcript then will help you answer question or response back about the transcript.

WIP...