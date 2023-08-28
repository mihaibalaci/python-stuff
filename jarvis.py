# simple program that uses chatgpt text and transforms it into speech

import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import openai
# please do not store the key in the script, use an .env file or similar to call it 
openai.api_key = OPENAI_API_KEY

# convert text to speech
# I inilially used FeiQ lib but is dramatically slow :)
def SpeakText(command):

    # initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    # loop in case of errors
    while(1):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
            
                # prepare recogniser to receive imput
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print ("I'm listening")
                
                # now listens for user's imput
                audio = r.listen(source2) 

                # Use google (or Alexa if you want) to recognize audio
                MyText = r.recognize_google(audio)
                return MyText
        
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")

# now, this will send messages to chatgpt and get the responses - magic :)
def sent_to_chatGPT(messages, model="gpt-3.5-turbo"):
    
    response = openai.Completion.create(
        engine=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
# this is ugly i know but I need this in order to make sure chatgpt remembers the previous conversation and adds context - apprend the dictioanry on line 69
    messages = response.choices[0].messages.content
    messages.append(response.choices[0].messages)
    return messages

messages = []
while(1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = sent_to_chatGPT(messages)
    SpeakText(response)

    print(response)
