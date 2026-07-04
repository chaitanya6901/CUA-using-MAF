import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from common.tools import launch_app, set_text, trigger_save, fill_save_dialog, close_window
from news_tools import get_last_summary
from agent_framework import tool

@tool
def write_summary_to_notepad_and_save() -> str:
    """Opens Notepad, pastes stored summary, saves as news_summary.txt, closes. Single tool, real window_title threaded through every call -- fixes the missing-argument crash from the prior version."""
    text = get_last_summary()
    if not text:
        return "ERROR: no summary available. Call fetch_and_summarize_news first."
    try:
        window_title = launch_app()
        set_text(window_title, text)
        trigger_save(window_title)
        fill_save_dialog("news_summary.txt")
        close_window()
        return "SUCCESS: saved as news_summary.txt and closed Notepad"
    except Exception as e:
        return f"ERROR: {e}"
