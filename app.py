import subprocess
import torch
import streamlit as st
from streamlit import session_state as state
import streamlit_ace as st_ace
import pipline

if "app" not in state:
    state.app = "model"
    state.out = ""
    state.user_name = None
    state.language = None 
    state.level = None
    state.started = False
    state.user_profile = {"language": None, "level" : None, "user_name" : None, "subject": None, "weaknesses": None}


example_question = "Here's a detailed Python question about for loops for a beginner level:\n Question: \n Write a program that calculates the sum of all the even numbers from 1 to a given positive integer, n. The program should use a for loop to iterate over the numbers and add up the even ones. Finally, it should print the total sum. \n Example: \n If the input value of n is 10, the program should calculate the sum of all even numbers from 1 to 10 (inclusive), which are 2, 4, 6, 8, and 10. The sum of these numbers is 30, so the program should output: \n Example code: \n The sum of all even numbers from 1 to 10 is 30. \n Your task is to write the Python code to solve this problem using a for loop. Good luck!"

header_row = st.container()
middle_row = st.container()
bottom_row = st.container()

def __user_data(lang, lvl, subject):
    state.user_profile["language"] = lang
    state.user_profile["level"] = lvl
    state.user_profile["subject"] = subject


def __run_TTI():
    with bottom_row.empty():
        bottom_row.markdown(":green[Running pipline]")
        bottom_row.write(pipline.chain_TI(state.input_text)['text'])


def __run_CC():
    with bottom_row.empty():
        bottom_row.markdown(":green[Running pipline]")
        words = state.input_text.rstrip().split()
        if len(words) != 2:
            bottom_row.error("Please enter two terms")
        else:
            bottom_row.write(pipline.chain_CC({"term1": words[0], "term2": words[1]})['text'])

#First Screen - Choose your name
if state.user_profile["user_name"] == None:
    header_row.title("Welcome to _____! \n What's your name?") 
    user_name = header_row.text_input("")
    if user_name:
        header_row.write(f"Hi {user_name}, Nice to meet you.")
        continue_button = header_row.button("Lets get started")
        if continue_button:
            state.user_profile["user_name"] = user_name


#Second Screen - Choose your language, level, subject
elif state.user_profile["language"] == None:
    header_row.title("Lets get to know you! 💬")
    col1, col2, col3 = st.columns(3)
    with col1:
        chosen_lang = st.radio("Prefered pratice language:", ('Python', 'C++', 'JavaScript'))
        if chosen_lang == 'Python':
            st.write('You selected Python. 🎉')
        else:
            st.write("You didn\'t select Python.😥")
    
    with col2:
        user_lvl = st.slider("What's your mastery level?", 0, 10)
        st.write("My mastery level is:", user_lvl)
    
    with col3: 
        subject = st.multiselect("What subject do you wanna study?", ['If-Else', 'While loops', 'For loops', 'Funny stuff'])
    
    submit_button = st.button("Lets start! 🌟")
    if submit_button and chosen_lang == 'Python' and subject:
        state.started = True
        __user_data(chosen_lang, user_lvl, subject)
        st.empty()

    if not subject:
        st.error("Woops! You haven't chosen a subject to study", icon="😮")
    
    
    print(state.user_profile)
    
        
    
#Third Screen - start Questions
 # todo - when do we know to start the questions

if state.started:
    st.balloons()
    header_row.title("Answer the following question")
    first_question = example_question
    #first_question = pipline.generate_question(state.user_profile)
    middle_row.write(first_question)
    user_code = st_ace("Write your code here") 
    middle_row.code(user_code, state.user_profile["language"])
    submit_code = st.button("Submit your code")
    run_code = st.button("Run your code")
    if run_code:
        exec(user_code)
    if submit_code:
        pipline.next_question(first_question, str(user_code), state.user_profile)

    
    
    
# else:
#     bottom_row.header("Output")
#     header_row.text_area("enter text", key="input_text")
#     tti_button , cc_button = header_row.columns(2)
#     tti_button.button("What are you trying to imply?", on_click=__run_TTI)
#     cc_button.button("What is the connection between the two terms?", on_click=__run_CC)
