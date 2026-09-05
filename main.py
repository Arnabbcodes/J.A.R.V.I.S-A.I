import pyttsx3#for audio output
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification#for notification
import pyautogui#to open computer applications
import wikipedia#to search in wikipedia
import pywhatkit as pwt
import userconfiguration
import smtplib 
import openaiinfo as ai
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    content=" "
    while(content==" "):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            content=r.recognize_google(audio,language='en-in')
            print("Sir, you just said " + content)
        except Exception as e:
            print("Please try again sir, I did not understand that.....")
    return content
def main_process():
    jarvis_chat=[]
    while True:
     request=command().lower()
     print(request)
     if 'hello' in request:
         speak("Hello sir, I am JARVIS")
     elif 'jarvis' in request:
         speak("Yes sir, I am here")  
     elif 'how are you' in request:
         speak("I am fine sir, what about you?")
     elif 'good' in request:
         speak("That's good to hear sir")
     elif 'bad' in request:
         speak("I am sorry to hear that sir, I hope you will be fine soon")
     elif 'exit' in request:
         speak("Goodbye sir, have a nice day")
         break
     elif 'thank you' in request:
         speak("You are welcome sir")
     elif 'play music' in request:
            speak("Playing music sir")
            songs=random.randint(1,5)
            if songs==1:
                speak("Playing song 1")
                webbrowser.open("https://youtu.be/kv_5z2ROptE?si=VPnixaYJjH8UbYvc")
            elif songs==2:
                speak("Playing song 2")
                webbrowser.open("https://youtu.be/SxTYjptEzZs?si=WNA0-yGmE4JXCLWJ")
            elif songs==3:
                speak("Playing song 3")
                webbrowser.open("https://youtu.be/otyKssvCZxw?si=hzaADrG6XR04Ikjy")#add songs
            elif songs==4:
                speak("Playing song 4")
                webbrowser.open("https://youtu.be/AgX2II9si7w?si=hKQ2bKk5QsFcRyVR") 
            elif songs==5:
                speak("Playing song 5")
                webbrowser.open("https://youtu.be/i52TYO13Nyg?si=RnO4Mfjy7JZk3J1F")
     elif 'open youtube' in request:
                speak("Opening youtube sir")
                webbrowser.open("https://www.youtube.com/")
     elif 'open google' in request:
                speak("Opening google sir")
                webbrowser.open("https://www.google.com/")
     elif 'open facebook' in request:
                speak("Opening facebook sir")
                webbrowser.open("https://www.facebook.com/")
     elif 'open instagram' in request:
                  speak("Opening instagram sir")
                  webbrowser.open("https://www.instagram.com/")   
     elif 'open twitter' in request:
                  speak("Opening twitter sir")
                  webbrowser.open("https://www.twitter.com/")                             
     elif "say time" in request:
                now_time=datetime.datetime.now()
                speak(f"The current time is {now_time.hour}:{now_time.minute}")
     elif "say date" in request:
                     now_time=datetime.datetime.now()
                     speak(f"The current date is {now_time.day}/{now_time.month}/{now_time.year}")   
     elif "new task" in request:
          task=request.replace("new task","")
          task=task.strip()
          if task !="":
               speak("Adding task sir"+task)
               with open("tasks.txt","a") as f:
                    f.write(task+"\n") 
     elif "say task" in request:
          speak("Looking at your tasks sir")
          with open("tasks.txt","r") as f:  
               speak("Here are your tasks sir: " + f.read()) 
     elif "show work" in request:
          speak("You will be notified sir")
          with open("tasks.txt","r") as f:
             tasks=f.read()
          notification.notify(
             title="J.A.R.V.I.S\nToday's tasks are: ",
             message=tasks,
            )
     elif "open" in request:
          query=request.replace("open","")
          pyautogui.press("super")
          pyautogui.typewrite(query)
          pyautogui.sleep(2)
          pyautogui.press("enter")
     elif "delete task" in request:
          task=request.replace("delete task","")
          task=task.strip()
          if task !="":
               speak("Deleting task sir"+task)
               with open("tasks.txt","r") as f:
                    lines=f.readlines()
               with open("tasks.txt","w") as f:
                    for line in lines:
                         if line.strip()!=task:
                              f.write(line)
     elif "wikipedia" in request:
          request=request.replace("jarvis","")
          request=request.replace("search wikipedia","")
          result=wikipedia.summary(request, sentences=2)
          print(result)
          speak("Here is what I found on Wikipedia:",result)
     elif "search in google" in request:
           request=request.replace("jarvis","")
           request=request.replace("search in google","")
           webbrowser.open("https://www.google.com/search?q="+request)     
     elif "send whatsapp" in request:
            request=request.replace("jarvis","")
            request=request.replace("send whatsapp","")
            pwt.sendwhatmsg("+91 ",request,15,5,40)
            # you can add your number in the above line to send message to yourself 
            # and make sure to change the time(the delay)i.e 40 in the above example in the above line to 1 minute ahead of the current time to send the message successfully 
            # and add all the contacts of your device if you wish to send message to them :) 
     elif "send email" in request:
                 request=request.replace("jarvis","")
                 request=request.replace("send email","")
                 pwt.send_email(userconfiguration.gmail_user, password=userconfiguration.gmail_password, subject="Subject", message=request, email_receiver="recipient@example.com")
                 speak("Email sent successfully sir.")
                 print("Email sent successfully sir.")
     elif "send email using SMTP" in request:
                    smgmail=smtplib.SMTP('smtp.gmail.com', 587)
                    smgmail.starttls()
                    smgmail.login(userconfiguration.gmail_user, userconfiguration.gmail_password)
                    message="""
                      This is the subject of the email
                        This is the body of the email
                        this is the end of the email
                        """
                    smgmail.sendmail(userconfiguration.gmail_user, "recipient@example.com",message)
                    speak("Email sent successfully sir.")
                    print("Email sent successfully sir.")
     elif "ask ai" in request:
            jarvis_chat=[]
            request=request.replace("jarvis","")
            request=request.replace("ask ai","")
            jarvis_chat.append({"role":"user","content":response})
            response=ai.send_request(jarvis_chat)
            print(response)
            speak(response)        
     elif "clear chat" in request:
           jarvis_chat=[]
           speak("Chat Cleared")
           print("Chat Cleared")
                     
     else:
           request=request.replace("jarvis","")
           jarvis_chat.append({"role":"user","content":request})

           response=ai.send_request(jarvis_chat)
           jarvis_chat.append({"role":"assistant","content":response})

           speak(response)

     
#speak("Hello sir, I am JARVIS")
main_process()


