'''
Created on 9 Mar 2020
asdfsfsdfsdfdsffsd
@author: Oleg Ovroutsky
'''
import _thread as thread, queue, time
import threading
import speech_recognition as sr
import mysql.connector
import os
import sys
aaaa =2313
#Counter for number of times the word is recognized
counter = 0

#Make a connection to MySql data base
db = mysql.connector.connect(host = "localhost", user = "root", passwd = "oleg1990",auth_plugin="mysql_native_password")
mc = db.cursor()
#Check if connected to data base
if db.is_connected():
    print("ok")
    
#Function to activate the microphone and send the recording to the queue    
def recorder(dataQueue):
    r = sr.Recognizer()
    while True:
        print("recording...")
        with sr.Microphone(device_index=0) as source:
            print("Adjusting noise")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Saved to audio var")
            audio = r.listen(source, phrase_time_limit=10)
        dataQueue.put(audio)
        
#Function to pull the recording from the queue and send it to recogtion speech to text
#if the recording contains one of the words in wordlist than send the data to MySql table
def recognizer(db,dataQueue,safeprint):
    wordList = ["Corona","corona","korona","Korona"]
    mc = db.cursor()
    r = sr.Recognizer()
    global counter
    while True:
        time.sleep(4)
        try:
            data = dataQueue.get()
        except queue.Empty:
            pass
        except Exception as ex:
            with safeprint:
                print(ex)
        try:
            text = r.recognize_google(data, language="en-US", show_all=True)
            for x in list(text.values())[0]:
                if any([word in str(list(x.values())[0]).lower() for word in wordList]):
                    counter += 1
                    print(counter)
                    with open('corona_{}.wav'.format(counter), mode='bx') as f:
                        f.write(data.get_wav_data())
                    sql = "INSERT INTO test.corona_counter_1 (id, path) VALUES (%s, %s)"
                    val = (counter, os.path.dirname(os.path.abspath(sys.argv[0])))
                    mc.execute(sql, val)
                    db.commit()
                    break
        except Exception as ex:
            with safeprint:
                print(ex)
#The main function that runs the program                
def main(db):
    
    safeprint = thread.allocate_lock()
    
    dataQueue = queue.Queue()
    thread1 = threading.Thread(target=recorder,group=None,args = ([dataQueue]))
    thread2 = threading.Thread(target=recognizer,group=None,args = ([db,dataQueue,safeprint]))
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main(db)   
    
    
    