import time
import streamlit as st
import pandas as pd 
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib
from joblib import dump,load
from PIL import Image 
import numpy as np
import pandas as pd
import JSON
import requests
import sqlite3

#data=pd.read_csv('bbc.csv',)
# API key :
#@st.cache(allow_output_mutation=True)
@st.cache_resource()
def GenerateVideo(img_link,voice_id,text):
    api_url = "https://api.d-id.com/talks/"
    payload = {
    "script": {
        "type": "text",
        "input": text,
        "subtitles": "false",
        "provider": {
            "type": "microsoft",
            "voice_id": voice_id
        },
        "ssml": "false"
    },
    "config": {
        "fluent": "false",
        "pad_audio": "0.0",
        
    }
        
        ,"source_url": img_link

        }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic eWVjb2IyNzQyNUBlbGl4aXJzZC5jb20:u8lHSBPtZLDU-EHZ4mOWZ"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    id=response.json()['id']
    url = api_url+id
    headers = {
    "accept": "application/json",
    "authorization": "Basic eWVjb2IyNzQyNUBlbGl4aXJzZC5jb20:u8lHSBPtZLDU-EHZ4mOWZ"
    }
    web=None
 
    while web==None:
       
        time.sleep(0.5)
        response = requests.get(url, headers=headers)
        try:
            web = response.json()['result_url']
        except Exception as e:
         print(e)
         print("Sorry that's not valid")
    return web


def SelectImage(choice):
    if choice == 'Davis':
        voice_id="en-US-JasonNeural"
        img_link="https://clips-presenters.d-id.com/jack/Pt27VkP3hW/fbQicImV2J/image.png"
    
    if choice == 'Ashley':
        voice_id="en-US-AshleyNeural"
        img_link="https://clips-presenters.d-id.com/amy/sEIU0O2gBy/VrHMAOUSgO/image.png"
    
    if choice == 'Jason':
        voice_id="en-US-DavisNeural"
        img_link="https://clips-presenters.d-id.com/rian/lZC6MmWfC1/mXra4jY38i/image.png"
    
    return img_link,voice_id
    
    
@st.cache_resource()
def Category(data):
    model=load('ML.joblib')
    vectorizer=load('Vectorizer.joblib')
    x=vectorizer.transform(data)
    nparray=model.predict(vectorizer.transform(data))
    array=(nparray)
    index=int(array)
    return index
    
def Data(text,Category,Video_url):
    conn= sqlite3.connect(r"C:\Users\abdsh\OneDrive\Desktop\programing projects\NewsAnimate.db")
    cursor=conn.cursor()  
    cursor.execute("INSERT INTO NA (news_text, Category, Video_url) VALUES (?, ?, ?)",(text, Category, Video_url))
    conn.commit()
    conn.close()
    st.write("your Data has been saved")
    
def main():
    Categories=['business','entertainment', 'politics', 'sport', 'tech']
    col1,col2=st.columns(2)
    script=col1.text_area("Type news:",height=20)
    text=[script]
    Selected=col2.selectbox("Select an image",('Davis','Ashley','Jason'))
    img_link,voice_id=SelectImage(Selected)
    index=Category(text)
    section=Categories[index]
    d=col2.selectbox("Change the Category if it's wrong",('business','entertainment', 'politics', 'sport', 'tech'))
    check=col2.checkbox('Are you sure you want to change it?')
    if check:
        section=d
    st.write('Your Category is: ',section) 
    bt=col1.button("Click here to save the data")
    button=st.button("Generate Video",type='primary')
    if button :
        Video_url=GenerateVideo(img_link,voice_id,script)
        st.video(Video_url)
    
    if bt:
        Data(script,section,Video_url)
        st.write(script,section,Video_url)
    
    
    
if __name__=="__main__":
    main()