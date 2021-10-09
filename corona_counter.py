'''
Created on 7 Oct 2021

@author: Oleg Ovroutsky
'''
import speech_recognition as sr

recognizer = sr.Recognizer()
audio_file_ = sr.AudioFile("homo_2.wav")

with sr.Microphone() as source:
    audio_file = recognizer.listen(source)
    text = recognizer.recognize_google(audio_file, language="en-US", show_all=True)
    print(text)
    