# CUA - Notepad Automation Agent

A Python automation agent that controls Windows Notepad using an agent framework with Ollama (LLaMA 3.2) integration.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) running locally with `llama3.2:3b` model
- Windows OS (uses `pywinauto` for UI automation)

## Installation

```bash
pip install agent-framework pywinauto pyperclip
```

## Usage

```bash
python agent.py
```

The agent will launch Notepad, type a message, save it as `test.txt`, and close Notepad.

## Tools

- `open_notepad()` - Launch Notepad
- `type_text(text)` - Type text into Notepad
- `save_file(filename)` - Save the file
- `close_notepad()` - Close Notepad
