import subprocess
import torch
import streamlit as st
from streamlit import session_state as state
import streamlit_ace
import pipline

if "app" not in state:
    state.app = "model"
    state.out = ""
in_area = st.container()
out_area = st.container()
in_area.title("Demo using langchain and streamlit") 
out_area.header("Output")



def __run_TTI():
    with out_area.empty():
        out_area.markdown(":green[Running pipline]")
        out_area.write(pipline.chain_TI(state.input_text)['text'])


def __run_CC():
    with out_area.empty():
        out_area.markdown(":green[Running pipline]")
        words = state.input_text.rstrip().split()
        if len(words) != 2:
            out_area.error("Please enter two terms")
        else:
            out_area.write(pipline.chain_CC({"term1": words[0], "term2": words[1]})['text'])


in_area.text_area("enter text", key="input_text")
tti_button , cc_button = in_area.columns(2)
tti_button.button("What are you trying to imply?", on_click=__run_TTI)
cc_button.button("What is the connection between the two terms?", on_click=__run_CC)
with st.expander("code", expanded=False):
    st.code("""
    import pipline

if "app" not in state:
    state.app = "model"
    state.out = ""
in_area = st.container()
out_area = st.container()
in_area.title("Demo using langchain and streamlit") 
out_area.header("Output")



def __run_TTI():
    with out_area.empty():
        out_area.markdown(":green[Running pipline]")
        out_area.write(pipline.chain_TI(state.input_text)['text'])


def __run_CC():
    with out_area.empty():
        out_area.markdown(":green[Running pipline]")
        words = state.input_text.rstrip().split()
        if len(words) != 2:
            out_area.error("Please enter two terms")
        else:
            out_area.write(pipline.chain_CC({"term1": words[0], "term2": words[1]})['text'])


in_area.text_area("enter text", key="input_text")
tti_button , cc_button = in_area.columns(2)
tti_button.button("What are you trying to imply?", on_click=__run_TTI)
cc_button.button("What is the connection between the two terms?", on_click=__run_CC)

    """,language="python")