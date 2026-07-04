import asyncio
from agent_framework import ChatAgent
from agent_framework.ollama import OllamaChatClient
from news_tools import fetch_and_summarize_news
from notepad_bridge import write_summary_to_notepad_and_save

agent = ChatAgent(
    chat_client=OllamaChatClient(model="qwen2.5:7b"),
    name="news_to_notepad_agent",
    instructions=(
        "You have exactly 2 tools. Call each ONCE, never retry any tool.\n"
        "1. Call fetch_and_summarize_news() FIRST.\n"
        "2. If it returns SUCCESS, call write_summary_to_notepad_and_save() SECOND.\n"
        "3. If it returns FAILED, output the error and STOP. Do NOT call any tool again.\n"
        "4. After write_summary_to_notepad_and_save returns SUCCESS, output 'Done.'\n"
        "NEVER call fetch_and_summarize_news more than once. NEVER retry failed tools."
    ),
    tools=[fetch_and_summarize_news, write_summary_to_notepad_and_save],
)

result = asyncio.run(agent.run("Get recent news, summarize it, and save it to Notepad."))
print(result)
