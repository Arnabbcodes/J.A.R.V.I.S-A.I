import datetime
import random
import smtplib
import webbrowser

import wikipedia
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plyer import notification
from pydantic import BaseModel

import openaiinfo as ai
import userconfiguration

app = FastAPI(title="J.A.R.V.I.S. Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Same in-memory chat history main.py keeps as `jarvis_chat` inside main_process
jarvis_chat = []

SONG_URLS = {
    1: "https://youtu.be/kv_5z2ROptE?si=VPnixaYJjH8UbYvc",
    2: "https://youtu.be/SxTYjptEzZs?si=WNA0-yGmE4JXCLWJ",
    3: "https://youtu.be/otyKssvCZxw?si=hzaADrG6XR04Ikjy",
    4: "https://youtu.be/AgX2II9si7w?si=hKQ2bKk5QsFcRyVR",
    5: "https://youtu.be/i52TYO13Nyg?si=RnO4Mfjy7JZk3J1F",
}


class CommandRequest(BaseModel):
    text: str


class CommandResponse(BaseModel):
    reply: str
    action: str = "none"       
    url: str | None = None     
    exit: bool = False         


def handle_command(raw_request: str) -> CommandResponse:
    """
    Mirrors main.py's main_process() while-loop body, one call per command
    instead of one iteration of an infinite loop. Same phrases, same order,
    same branch bodies as main.py.
    """
    global jarvis_chat

    request = raw_request.lower()

    if "hello" in request:
        return CommandResponse(reply="Hello sir, I am JARVIS", action="speak")

    elif "jarvis" in request and len(request.strip()) <= 8:
    
        return CommandResponse(reply="Yes sir, I am here", action="speak")

    elif "how are you" in request:
        return CommandResponse(reply="I am fine sir, what about you?", action="speak")

    elif "good" in request:
        return CommandResponse(reply="That's good to hear sir", action="speak")

    elif "bad" in request:
        return CommandResponse(
            reply="I am sorry to hear that sir, I hope you will be fine soon",
            action="speak",
        )

    elif "exit" in request:
        return CommandResponse(reply="Goodbye sir, have a nice day", action="speak", exit=True)

    elif "thank you" in request:
        return CommandResponse(reply="You are welcome sir", action="speak")

    elif "play music" in request:
        songs = random.randint(1, 5)
        url = SONG_URLS[songs]
        return CommandResponse(
            reply=f"Playing song {songs} sir",
            action="open_url",
            url=url,
        )

    elif "open youtube" in request:
        return CommandResponse(reply="Opening youtube sir", action="open_url", url="https://www.youtube.com/")

    elif "open google" in request:
        return CommandResponse(reply="Opening google sir", action="open_url", url="https://www.google.com/")

    elif "open facebook" in request:
        return CommandResponse(reply="Opening facebook sir", action="open_url", url="https://www.facebook.com/")

    elif "open instagram" in request:
        return CommandResponse(reply="Opening instagram sir", action="open_url", url="https://www.instagram.com/")

    elif "open twitter" in request:
        return CommandResponse(reply="Opening twitter sir", action="open_url", url="https://www.twitter.com/")

    elif "say time" in request:
        now_time = datetime.datetime.now()
        return CommandResponse(reply=f"The current time is {now_time.hour}:{now_time.minute}", action="speak")

    elif "say date" in request:
        now_time = datetime.datetime.now()
        return CommandResponse(
            reply=f"The current date is {now_time.day}/{now_time.month}/{now_time.year}",
            action="speak",
        )

    elif "new task" in request:
        task = request.replace("new task", "").strip()
        if task != "":
            with open("tasks.txt", "a") as f:
                f.write(task + "\n")
            return CommandResponse(reply="Adding task sir " + task, action="speak")
        return CommandResponse(reply="Please tell me the task sir", action="speak")

    elif "say task" in request:
        try:
            with open("tasks.txt", "r") as f:
                contents = f.read()
        except FileNotFoundError:
            contents = "(no tasks yet)"
        return CommandResponse(reply="Here are your tasks sir: " + contents, action="speak")

    elif "show work" in request:
        try:
            with open("tasks.txt", "r") as f:
                tasks = f.read()
        except FileNotFoundError:
            tasks = "(no tasks yet)"
        try:
            notification.notify(
                title="J.A.R.V.I.S\nToday's tasks are: ",
                message=tasks,
            )
        except Exception:
            pass
        return CommandResponse(reply="You will be notified sir", action="speak")

    elif "delete task" in request:
        task = request.replace("delete task", "").strip()
        if task != "":
            try:
                with open("tasks.txt", "r") as f:
                    lines = f.readlines()
                with open("tasks.txt", "w") as f:
                    for line in lines:
                        if line.strip() != task:
                            f.write(line)
            except FileNotFoundError:
                pass
            return CommandResponse(reply="Deleting task sir " + task, action="speak")
        return CommandResponse(reply="Please tell me which task to delete sir", action="speak")

    elif "wikipedia" in request:
        query = request.replace("jarvis", "").replace("search wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            return CommandResponse(reply="Here is what I found on Wikipedia: " + result, action="speak")
        except Exception:
            return CommandResponse(
                reply="Sorry sir, I could not find that on Wikipedia",
                action="speak",
            )

    elif "search in google" in request:
        query = request.replace("jarvis", "").replace("search in google", "").strip()
        url = "https://www.google.com/search?q=" + query
        return CommandResponse(reply=f"Searching Google for {query} sir", action="open_url", url=url)

    elif "send whatsapp" in request:
        import pywhatkit as pwt

        msg = request.replace("jarvis", "").replace("send whatsapp", "").strip()
        pwt.sendwhatmsg("+91 ", msg, 15, 5, 40)
        return CommandResponse(reply="WhatsApp message scheduled sir", action="speak")

    elif "send email" in request:
        import pywhatkit as pwt

        msg = request.replace("jarvis", "").replace("send email", "").strip()
        pwt.send_email(
            userconfiguration.gmail_user,
            password=userconfiguration.gmail_password,
            subject="Subject",
            message=msg,
            email_receiver="recipient@example.com",
        )
        return CommandResponse(reply="Email sent successfully sir.", action="speak")

    elif "send email using smtp" in request:
        smgmail = smtplib.SMTP("smtp.gmail.com", 587)
        smgmail.starttls()
        smgmail.login(userconfiguration.gmail_user, userconfiguration.gmail_password)
        message = """
This is the subject of the email
This is the body of the email
this is the end of the email
"""
        smgmail.sendmail(userconfiguration.gmail_user, "recipient@example.com", message)
        smgmail.quit()
        return CommandResponse(reply="Email sent successfully sir.", action="speak")

    elif "clear chat" in request:
        jarvis_chat = []
        return CommandResponse(reply="Chat Cleared", action="speak")

    elif "ask ai" in request:
        # main.py bug fixed: `response` was referenced before assignment
        query = request.replace("jarvis", "").replace("ask ai", "").strip()
        jarvis_chat = [{"role": "user", "content": query}]
        try:
            response = ai.send_request(jarvis_chat)
        except Exception as e:
            return CommandResponse(
                reply=f"Sorry sir, I could not reach the AI service ({e}).",
                action="speak",
            )
        return CommandResponse(reply=response, action="speak")

    elif request.strip().startswith("open") and "open youtube" not in request \
            and "open google" not in request and "open facebook" not in request \
            and "open instagram" not in request and "open twitter" not in request:
        return CommandResponse(
            reply="Sorry sir, opening desktop applications only works when "
            "JARVIS runs on your own machine (main.py), not on a web server.",
            action="desktop_only",
        )

    else:
        cleaned = request.replace("jarvis", "").strip()
        jarvis_chat.append({"role": "user", "content": cleaned})
        try:
            response = ai.send_request(jarvis_chat)
        except Exception as e:
            return CommandResponse(
                reply=f"Sorry sir, I could not reach the AI service ({e}).",
                action="speak",
            )
        jarvis_chat.append({"role": "assistant", "content": response})
        return CommandResponse(reply=response, action="speak")


@app.get("/api/health")
def health():
    return {"status": "online", "system": "J.A.R.V.I.S."}


@app.post("/api/command", response_model=CommandResponse)
def process_command(payload: CommandRequest):
    return handle_command(payload.text)
