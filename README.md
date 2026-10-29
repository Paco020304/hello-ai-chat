# hello-ai-chat

A simple command-line chatbot that keeps talking with an AI (DeepSeek, OpenAI-compatible API) and **remembers past conversation**, based on [lbc-team/hello_ai/multi_chat.py](https://github.com/lbc-team/hello_ai/blob/main/multi_chat.py).

## How memory works

- Every user message and AI reply is appended to a `messages` list, and the whole list is sent with each request, so the model sees the full context.
- History is saved to `chat_history.json` after each turn and reloaded on startup, so memory survives restarts.
- Only the most recent `CHAT_MAX_TURNS` (default 20) rounds are sent, to stay within the context window.

## Usage

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in DEEPSEEK_API_KEY
python multi_chat.py
```

Commands: `/history`, `/clear`, `/help`, `/exit`.

```
You: What's the highest mountain in the world?
AI: Mount Everest ...

You: What is the second?
AI: K2 ...
```
