import subprocess
import torch
import streamlit as st
from streamlit import session_state as state
import streamlit_ace
import pipline

if "app" not in state:
    state.app = "model"
    state.out = ""
    state.user_name = None
    state.language = None 
    state.grade = None
    state.started = False
    state.user_profile = dict()


header_row = st.container()
middle_row = st.container()
bottom_row = st.container()

def __change_lang(lang):
    state.language = lang
    print(state.language)

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
if state.user_name == None:
    header_row.title("Welcome to _____! \n What's your name?") 
    user_name = header_row.text_input("")
    if user_name:
        header_row.write(f"Hi {user_name}, Nice to meet you.")
        continue_button = header_row.button("Lets get started")
        if continue_button:
            state.user_name = user_name


#Second Screen - Choose your language, level, subject
elif state.language == None:
    chosen_lang = None
    header_row.title("What language would you like to practice? 💬")
    chosen_lang = middle_row.radio(" ", ('Python', 'C++', 'JavaScript'))
    user_lvl = bottom_row.radio(" ", ('Newbie', 'Good', 'Really Good'))
    subject = bottom_row.text_input("\n What sub-subject do you wanna study?")

    if chosen_lang == 'Python':
        middle_row.write('You selected Python. 🎉')
        bottom_row.button("Submit", on_click=__change_lang('Python'))
    else:
        middle_row.write("You didn\'t select Python.😥")
        
    

    
#Third Screen - Choose your Level
elif state.grade == None:
    print('hey we made it to third step!')
    self_grade_button_area , test_grade_button_area = header_row.columns(2)



    
    
#Fourth Screen
# elif not state.started:
    
    
# else:
#     bottom_row.header("Output")
#     header_row.text_area("enter text", key="input_text")
#     tti_button , cc_button = header_row.columns(2)
#     tti_button.button("What are you trying to imply?", on_click=__run_TTI)
#     cc_button.button("What is the connection between the two terms?", on_click=__run_CC)
