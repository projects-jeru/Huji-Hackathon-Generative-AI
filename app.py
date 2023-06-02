import streamlit as st
from streamlit import session_state as state
import streamlit_ace as st_ace
import pipline
import subprocess
from PIL import Image
def get_key():
    if st.secrets["api_key"]:
        return st.secrets["api_key"]
    else:
        return st.input_text("enter key")
image = Image.open('HackEnv/pics/Codi.png')

if "app" not in state:
    state.app = "model"
    state.out = None
    state.started = None
    state.user_profile = {"language": None, "level" : None, "user_name" : None, "subject": None, "params": [0,0,0,0,0,0]}
    state.user_live = False
    state.question = None
    state.user_code = None
    state.chat_answer = None


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
    state.question = pipline.next_question(state.user_profile)
    state.chat_answer = pipline.build_possible_answer(state.question)

def __run_code():
    state.out = subprocess.run(
                        ["python", "-c", state.user_code],
                        capture_output=True,
                        text=True,
                    ).stdout


# Home Screen

if not state.user_live:
    with header_row.container():
        st.title("Hi, I'm Codi! 👋 \n Before you begin your quest to success let's start by getting to know you!")
        st.image(image)
    with middle_row.container():
    
        user_name = st.text_input("What's your name? 💬")
        col1, col2, col3 = st.columns(3)
        with col1:
            chosen_lang = st.radio("Prefered pratice language: 💻", ('Python', 'C++', 'JavaScript'))
            if chosen_lang == 'Python':
                st.write("You've selected Python. 🎉")
            else:
                st.write("You didn't select Python.😥")
        
        with col2:
            user_lvl = st.slider("What's your mastery level? 🏗️", 1, 10)
            st.write("My mastery level is:", user_lvl)
        
        with col3: 
            subject = st.multiselect("What subject do you wanna study? 📚", ['If-Else', 'While loops', 'For loops', 'String manipulation', 'Recursion', 'Backtracking'])
        
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
                state.chat_answer = pipline.build_possible_answer(state.question)
                st.experimental_rerun()
                

    
    print(state.user_profile)
    
# Questions Prompt Screen

elif state.started == "question":
    with header_row.container():
            
        st.title("Answer the following question ✍️")
        st.write(state.question)
        state.user_code = st_ace.st_ace(language="python", auto_update=True) 
        Submit, run = st.columns(2)
        st.text(state.out)
        Submit.button("Submit Answer 📫",on_click=__feedback_maker)
        run.button("Run Code ▶️",on_click=__run_code)
            

# Feedback Screen
elif state.started == "feedback":
    with header_row.container():
        
        st.title("How did you do? 🤔")
        st.write(state.feedback_maker)

        st.title("Here is a possible answer 📖")
        st.code(state.chat_answer, language="python")

        st.button("Next Question",on_click=__next_question) 
        
