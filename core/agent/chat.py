from dataclasses import dataclass, field
from ai.factory import AIFactory
from prompt.message import Message

@dataclass
class ChatAgent():
    ai = AIFactory().create('openai', 'gpt-3.5-turbo-0613')
    messages: list[Message] = field(default_factory=list)
    message_window_size: int = 50

    async def ask(self, message):
        system_prompt = Message(
            '''
                You are content writer, that will help me write stuff.
            ''',
            role="system",
            name=None
        )

        _messages = [system_prompt, message]
        
        if len(self.messages) >= self.message_window_size:
            # remove last message
            self.messages.pop()
        
        # save messages
        self.messages.append(_messages)

        # generate message
        res = await self.ai.generate(_messages)
        print(res)