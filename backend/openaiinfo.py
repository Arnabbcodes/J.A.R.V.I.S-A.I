#open ai astra api was not available so i used groq api for this purpose. you can use any other api for this purpose.
from groq import Groq
import userconfiguration

client = Groq(api_key=userconfiguration.JARVIS_API_KEY)
#def send_request(query):
 #   completion = client.chat.completions.create(
  #      model="openai/gpt-oss-120b",
   #     messages=[
    #    {
     #       "role": "user",
      #      "content": query
       # }
        #],
    #)

    #return completion.choices[0].message.content
def send_request(query):
    completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=query
        )
    
    return completion.choices[0].message.content
    

