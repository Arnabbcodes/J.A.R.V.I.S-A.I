# J.A.R.V.I.S. -A.I  — Voice Assistant with Web HUD

A Python voice assistant with an Iron-Man-style browser interface. `main.py` is the original desktop assistant (mic input, text-to-speech, task management, AI chat via Groq). `server.py` exposes that same command set over HTTP so the `frontend/` HUD can talk to it from a browser. It can also work as your desktop assistant if you run the 'main.py' file in your terminal as well as you can control few operations from the localhost browser itself such as opening youtube, opening social media platforms, playing music etc.
You are requested to go through the code once inorder to make it work as your personal desktop/A.I assistant in your desktop/laptop.
## Structure

```
├── backend/
│   ├── main.py                      # original desktop assistant (mic + speakers)
│   ├── server.py                    # HTTP API mirroring main.py's commands
│   ├── openaiinfo.py                # Groq AI integration
│   ├── userconfiguration.py         # your credentials (not committed)
│   ├── userconfiguration.example.py # template — copy this to userconfiguration.py
│   ├── tasks.txt
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── .gitignore
```

## Features

- 🎙️ Voice input (browser mic or desktop microphone)
- 💬 Chat/command console
- 🟢 Live status — Listening / Thinking / Speaking
- ⚡ Animated reactor core
- 📊 System diagnostics panel
- 📱 Responsive desktop + mobile layout
- 🤖 AI chat fallback via Groq

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `userconfiguration.example.py` to `userconfiguration.py` and fill in your real Gmail and Groq credentials.

## Run

**Backend:**
```bash
cd backend
uvicorn server:app --reload --port 8000
```

**Frontend** (separate terminal):
```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in Chrome or Edge.

**Original desktop version** (mic/speakers, no browser):
```bash
cd backend
python main.py
```

## Notes

- `userconfiguration.py` is gitignored — never commit real credentials.
- Voice input requires Chrome or Edge (Web Speech API); typing works in any browser.
- Commands like `send whatsapp` and generic `open <app>` require a real desktop and only work when running `main.py` directly, not through `server.py`.
Made by ~Arnab Bhattacharjee :)<img width="1919" height="909" alt="Screenshot 2026-09-05 182100" src="https://github.com/user-attachments/assets/cd59a47d-5bfd-41da-bea2-5b314f82e756" />
