from playwright.sync_api import sync_playwright
import os
import time

USER_DATA_DIR = "channel/session/user_data"


# 🚀 Start WhatsApp (persistent session)
def start_whatsapp():
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    p = sync_playwright().start()

    context = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        channel="chrome",
        args=["--start-maximized"]
    )

    page = context.pages[0] if context.pages else context.new_page()

    if "web.whatsapp.com" not in page.url:
        page.goto("https://web.whatsapp.com")

    print("👉 Scan QR if first time")

    page.wait_for_selector("div[role='grid']", timeout=0)

    print("✅ WhatsApp ready")

    return page, context


# 📋 List chats
def list_chats(page, limit=20):
    chats = page.query_selector_all("div[data-testid='cell-frame-container']")

    results = []

    for chat in chats[:limit]:
        try:
            name_el = chat.query_selector("span[title]")
            name = name_el.get_attribute("title") if name_el else "Unknown"

            results.append({
                "name": name
            })
        except:
            pass

    return results


# 📂 Open chat by name
def open_chat(page, name):
    chats = page.query_selector_all("div[data-testid='cell-frame-container']")

    for chat in chats:
        try:
            name_el = chat.query_selector("span[title]")
            chat_name = name_el.get_attribute("title") if name_el else ""

            if chat_name == name:
                chat.click()
                print(f"✅ Opened chat: {name}")
                return
        except:
            pass

    raise Exception(f"Chat '{name}' not found")


# 💬 Get messages from opened chat
def get_messages(page, limit=20):
    messages = page.query_selector_all("div.message-in, div.message-out")

    results = []

    for msg in messages[-limit:]:
        try:
            # detect sender
            cls = msg.get_attribute("class") or ""
            sender = "me" if "message-out" in cls else "other"

            # 🔥 correct text selector
            text_el = msg.query_selector("span[data-testid='msg-text']")

            if text_el:
                text = text_el.inner_text().strip()
            else:
                text = ""

            results.append({
                "sender": sender,
                "text": text
            })

        except Exception as e:
            pass

    return results


# 🚀 Send message directly
def send_message(page, phone, message):
    url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    page.goto(url)

    page.wait_for_selector("div[contenteditable='true']")

    page.keyboard.press("Enter")

    print(f"✅ Sent to {phone}")