# CUA - Computer Use Agent

A Python automation project that controls Windows Notepad using AI agents with Ollama integration.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) running locally
- Windows OS (uses `pywinauto` for UI automation)
- Playwright (for web scraping in news agent)

## Installation

```bash
pip install agent-framework pywinauto pyperclip playwright
playwright install chromium
```

## Project Structure

```
CUA/
├── agent.py              # Basic Notepad automation agent (llama3.2:3b)
├── tools.py              # Notepad UI automation tools
└── cua-project/
    ├── agent_news.py     # News scraping + Notepad agent (qwen2.5:7b)
    ├── news_tools.py     # BBC News scraping and summarization
    ├── notepad_bridge.py # Bridge between news tools and Notepad
    └── common/
        └── tools.py      # Shared Notepad automation utilities
```

## Usage

### Basic Agent
```bash
python agent.py
```
Launches Notepad, types a message, saves as `test.txt`, and closes.

### News Agent
```bash
python cua-project/agent_news.py
```
Scrapes top 3 BBC News articles, summarizes them with Ollama, and saves to `news_summary.txt` in Notepad.

## Tools

### Basic Agent (`tools.py`)
- `open_notepad()` - Launch Notepad
- `type_text(text)` - Type text into Notepad
- `save_file(filename)` - Save the file
- `close_notepad()` - Close Notepad

### News Agent (`cua-project/`)
- `fetch_and_summarize_news()` - Scrape and summarize BBC News
- `write_summary_to_notepad_and_save()` - Save summary to Notepad
