from dataclasses import dataclass
from loguru import logger
import re

from interview_gpt.core.prompt.message import Message
from .chat import ChatAgent


@dataclass
class AssistantAgent(ChatAgent):
    async def fix_transcript(self, result):
        # create new messages to be consumed
        message = Message(
            f"""
            Please fix this transcript, but try not to change any wording:

            {result}
            """,
            role="user",
            name=None,
        )

        # ask agent
        resp = await self.ask(message)

        if resp is not None:
            content = resp.choices[0].message.content

            # update transcript, for more readible content
            with open("transcription.txt", "w") as f:
                f.write(content)

    async def is_question(self, data):
        # create new messages to be consumed
        message = Message(
            f"""
            Based on this text can you confirm if its a question?:

            Text: {data}

            Please only return response as an valid Python JSON object and nothing else.

            Example Response: {{ is_question: true }}
            """,
            role="user",
            name=None,
        )

        # ask agent
        resp = await self.ask(message)

        if resp is not None:
            content = resp.choices[0].message.content
            matches = re.search(r'"is_question":\s*(\w+)', content)

            if matches:
                is_quest = matches.group(1)  # Extracting the value of "is_question"
                result = {"is_question": is_quest}
                return result

        return None

    async def answer(self, data):
        message = Message(
            f"""
                Given the following question, please answer to the best of your ability:

                Question: {data}
            """,
            role="user",
            name=None,
        )

        # ask agent
        resp = await self.ask(message)

        if resp is not None:
            content = resp.choices[0].message.content
            logger.success(content)
            return content
