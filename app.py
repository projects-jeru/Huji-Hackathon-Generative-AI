import subprocess
import torch
import streamlit as st
from streamlit import session_state as state
import streamlit_ace as st_ace
import pipline
import subprocess

if "app" not in state:
    state.app = "model"
    state.out = None
    state.started = None
    state.user_profile = {"language": None, "level" : None, "user_name" : None, "subject": None, "params": [0,0,0,0,0,0]}
    state.user_live = False
    state.question = None
    state.user_code = None


example_question = "Here's a detailed Python question about for loops for a beginner level:\n Question: \n Write a program that calculates the sum of all the even numbers from 1 to a given positive integer, n. The program should use a for loop to iterate over the numbers and add up the even ones. Finally, it should print the total sum. \n Example: \n If the input value of n is 10, the program should calculate the sum of all even numbers from 1 to 10 (inclusive), which are 2, 4, 6, 8, and 10. The sum of these numbers is 30, so the program should output: \n Example code: \n The sum of all even numbers from 1 to 10 is 30. \n Your task is to write the Python code to solve this problem using a for loop. Good luck!"

header_row = st.empty()
middle_row = st.empty()

def __user_data(lang, lvl, subject):
    state.user_profile["language"] = lang
    state.user_profile["level"] = lvl
    state.user_profile["subject"] = subject

def __feedback_maker():
    state.started = "feedback"
    state.feedback_maker = pipline.feedback_maker(state.user_code,state.user_profile)

def __next_question():
    state.started = "question"
    state.question = pipline.next_question(state.question, state.user_code, state.user_profile)

def __run_code():
    state.out = subprocess.run(
                        ["python", "-c", state.user_code],
                        capture_output=True,
                        text=True,
                    ).stdout


#First Screen - Choose your name
if not state.user_live:
    with header_row.container():
        st.title("Welcome to Codi! \n Lets get to know you! 💬") 
    with middle_row.container():
    
        user_name = st.text_input("What's your name?")
        col1, col2, col3 = st.columns(3)
        with col1:
            chosen_lang = st.radio("Prefered pratice language:", ('Python', 'C++', 'JavaScript'))
            if chosen_lang == 'Python':
                st.write('You selected Python. 🎉')
            else:
                st.write("You didn\'t select Python.😥")
        
        with col2:
            user_lvl = st.slider("What's your mastery level?", 1, 10)
            st.write("My mastery level is:", user_lvl)
        
        with col3: 
            subject = st.multiselect("What subject do you wanna study?", ['If-Else', 'While loops', 'For loops', 'Funny stuff'])
        
        submit_button = st.button("Lets start! 🌟")
        if submit_button and chosen_lang == 'Python' and subject:
            if not subject:
                st.error("Woops! You haven't chosen a subject to study", icon="😮")
            else:
                state.started = "question"
                state.user_live = True
                __user_data(chosen_lang, user_lvl, subject)
                st.balloons()
                state.question = pipline.first_question(state.user_profile)
                st.experimental_rerun()
                

    
    print(state.user_profile)
    
#Third Screen - start Questions
 # todo - when do we know to start the questions

elif state.started == "question":
    with header_row.container():
            
            
    
        st.title("Answer the following question")
        #first_question = example_question
        st.write(state.question)
        state.user_code = st_ace.st_ace(language="python") 
        Submit, run = st.columns(2)
        st.text(state.out)
        Submit.button("Submit and get new question",on_click=__feedback_maker)
        run.button("run code",on_click=__run_code)
            

elif state.started == "feedback":
    with header_row.container():
        st.title("feedback question")
        #first_question = example_question
        st.write(state.feedback_maker)
        st.button("next question",on_click=__next_question) 