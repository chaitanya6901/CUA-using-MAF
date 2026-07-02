import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from tools import open_notepad, type_text, save_file, close_notepad

agent = Agent(
    client=OllamaChatClient(model="llama3.2:3b"),
    name="notepad_agent",
    instructions="You have tools to control Notepad. Use function calls — never output text describing them.",
    tools=[open_notepad, type_text, save_file, close_notepad],
)

task = (
    "Execute these 4 steps as function calls. Do not output text. Do not skip steps.\n"
    "1. open_notepad()\n"
    "2. type_text(text='hi chaitanya how are you')\n"
    "3. save_file(filename='test.txt')\n"
    "4. close_notepad()\n"
    "After step 4, say 'Done.'"
)
result = asyncio.run(agent.run(task))
print(result.text if hasattr(result, "text") else str(result))
