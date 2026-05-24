from channel.whatsapp.client import (
    start_whatsapp,
    list_chats,
    open_chat,
    get_messages
)


def main():
    page, context = start_whatsapp()

    # 1. list chats
    chats = list_chats(page)

    print("\nChats:")
    for c in chats[:5]:
        print(c)

    # 2. open first valid chat (skip Unknown)
    selected_chat = None
    for c in chats:
        if c.get("name") and c["name"] != "Unknown":
            selected_chat = c["name"]
            break

    if not selected_chat:
        print("❌ No valid chat found")
    else:
        print(f"\n👉 Opening chat: {selected_chat}")
        open_chat(page, selected_chat)

        # small wait for messages to load
        page.wait_for_timeout(2000)

        # 3. read messages
        msgs = get_messages(page)

        print("\nMessages:")
        for m in msgs:
            print(m)

    input("\nPress Enter to exit cleanly...")
    context.close()


if __name__ == "__main__":
    main()