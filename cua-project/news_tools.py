import time
from playwright.sync_api import sync_playwright
import ollama
from agent_framework import tool

_last_summary_block = ""

@tool
def fetch_and_summarize_news() -> str:
    """Opens BBC News in browser, extracts top 3 articles, summarizes with Ollama. Returns status only."""
    global _last_summary_block
    articles = []
    pw = None
    browser = None

    try:
        print("  [1/5] Launching browser...", flush=True)
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()

        print("  [2/5] Opening BBC News...", flush=True)
        page.goto("https://www.bbc.com/news", wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)

        print("  [3/5] Extracting headlines...", flush=True)
        page.screenshot(path="debug_bbc.png")
        print("  [3/5] Screenshot saved: debug_bbc.png", flush=True)

        selectors = ['h2 a[href]', 'h3 a[href]', '[data-testid*="title"] a', 'a[data-testid*="title"]', '.gs-c-promo-heading a', 'article a[href]']
        links = []
        for sel in selectors:
            links = page.query_selector_all(sel)
            print(f"  [3/5] Selector '{sel}': {len(links)} matches", flush=True)
            if links:
                break

        if not links:
            links = page.query_selector_all('a')
            print(f"  [3/5] Fallback all a: {len(links)} matches", flush=True)

        print(f"  [3/5] Found {len(links)} headline links", flush=True)

        seen = set()
        for link in links:
            href = link.get_attribute("href")
            title = link.inner_text().strip()
            if not href or not title or len(title) < 10 or title in seen:
                continue
            seen.add(title)
            url = "https://www.bbc.com" + href if href.startswith("/") else href
            articles.append({"title": title, "url": url})
            if len(articles) >= 5:
                break

        print(f"  [3/5] Collected {len(articles)} unique headlines", flush=True)

        if not articles:
            _last_summary_block = ""
            return "FAILED: no articles found on BBC News"

        blocks = []
        for i, art in enumerate(articles[:3]):
            print(f"  [4/5] Opening article {i+1}: {art['title'][:50]}...", flush=True)
            try:
                art_page = browser.new_page()
                art_page.goto(art["url"], wait_until="domcontentloaded", timeout=15000)
                time.sleep(2)
                body = art_page.inner_text("body")[:2000]
                art_page.close()
                print(f"  [4/5] Got {len(body)} chars, summarizing...", flush=True)
            except Exception as e:
                print(f"  [4/5] Failed to load article: {e}", flush=True)
                body = art["title"]

            try:
                summary = ollama.chat(
                    model="qwen2.5:7b",
                    messages=[{"role": "user", "content": f"Summarize this news in 2-3 sentences:\n\n{body}"}]
                )["message"]["content"].strip()
                print(f"  [4/5] Summary: {summary[:80]}...", flush=True)
            except Exception as e:
                print(f"  [4/5] Ollama error: {e}", flush=True)
                summary = "Summary not available."

            blocks.append(f"HEADLINE: {art['title']}\nSOURCE: {art['url']}\nSUMMARY: {summary}")

        _last_summary_block = ("\n\n" + "=" * 50 + "\n\n").join(blocks)
        print(f"  [5/5] Done. {len(blocks)} articles summarized.", flush=True)
        return f"SUCCESS: {len(blocks)} articles summarized"

    except Exception as e:
        return f"FAILED: {e}"

    finally:
        try:
            if browser:
                browser.close()
            if pw:
                pw.stop()
        except Exception:
            pass

def get_last_summary() -> str:
    return _last_summary_block
