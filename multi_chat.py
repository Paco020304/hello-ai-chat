import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
)
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
HISTORY_FILE = os.environ.get("CHAT_HISTORY_FILE", "chat_history.json")
MAX_TURNS = int(os.environ.get("CHAT_MAX_TURNS", "20"))
SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful assistant."}

HELP = """Commands:
  /history  show conversation history
  /clear    clear memory
  /help     show this help
  /exit     quit (history is saved automatically)"""


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return [SYSTEM_PROMPT]


def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def trimmed(messages):
    """Keep the system prompt plus the most recent MAX_TURNS user/assistant pairs."""
    system, rest = messages[:1], messages[1:]
    return system + rest[-MAX_TURNS * 2:]


def chat(messages, user_input):
    messages.append({"role": "user", "content": user_input})
    stream = client.chat.completions.create(
        model=MODEL, messages=trimmed(messages), stream=True
    )
    reply = []
    print("AI: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            reply.append(text)
            print(text, end="", flush=True)
    print("\n")
    messages.append({"role": "assistant", "content": "".join(reply)})


def main():
    messages = load_history()
    print(f"Multi-turn chat with {MODEL}. Loaded {len(messages) - 1} past messages.")
    print(HELP + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/help":
            print(HELP + "\n")
            continue
        if user_input == "/clear":
            messages = [SYSTEM_PROMPT]
            save_history(messages)
            print("Memory cleared.\n")
            continue
        if user_input == "/history":
            for m in messages[1:]:
                print(f"[{m['role']}] {m['content']}")
            print()
            continue

        try:
            chat(messages, user_input)
        except Exception as e:
            messages.pop()
            print(f"\n[Error] {e}\n")
            continue
        save_history(messages)

    save_history(messages)
    print("Bye! History saved to", HISTORY_FILE)


if __name__ == "__main__":
    main()
