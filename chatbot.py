# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 22:41:18 2019

@author: Late Night Coding
"""

#import necessary libraries
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pyttsx3

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

#Reading in the data
with open('DATA.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()
    
#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# chatbot voice !
def speak(message):
    engine= pyttsx3.init()
    engine.say('{}'.format(message))
    engine.runAndWait()

# greetings Keyword matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey")
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

#Generating answer
def response(user_input):
    Delphi_response=''
    sent_tokens.append(user_input)
    
    word_vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(sent_tokens)  
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    idx=similar_vector_values.argsort()[0][-2]
    
    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]
   
    if(vector_matched==0):
        Delphi_response=Delphi_response+"I am sorry! I don't understand you."
        return Delphi_response
    else:
        Delphi_response = Delphi_response+sent_tokens[idx]
        return Delphi_response



continue_dialogue=True
print('\n\n')
print("==========Delphi==========")
print("You can speak to me by typing in English.")
print('Enter "Bye" to quit')
print('='*26)
print("Hello. I am Delphi, how can i help you?")
speak("Hello. I am Delphi, how can i help you?")


while(continue_dialogue==True):
    user_input = input()
    user_input=user_input.lower()
    if(user_input!='bye'):
        if(user_input=='thanks' or user_input=='thank you' ):
            print("Delphi: You are welcome..")
            speak(" You are welcome")
            
        else:
            if(greeting(user_input)!=None):
                tmp=greeting(user_input)
                print("Delphi: "+tmp)
                speak(tmp)
            else:
                print("Delphi: ",end="")
                temp=response(user_input)
                print(temp)  
                speak(temp)
                sent_tokens.remove(user_input)
                

    else:
        continue_dialogue=False
        print("Delphi: Goodbye.")
        speak("goodbye")
        print("and Don't forget to subscribe to this awesome channel")
        speak("and Don't forget to subscribe to this awesome channel")



        