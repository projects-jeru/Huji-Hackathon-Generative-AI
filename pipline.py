import langchain as lc
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.prompts import load_prompt
import wikipedia
import os
import streamlit as st
import re

import openai

RATING_REGEX = r"\[( ?\'(?P<DIGITS>[0-9]|10)\'?,? ?){6}\]"
INT_REGEX = r"\b\d+\b"

openai.api_key = "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"
cur_question = None
cur_answer = None
chat_answer = None
feedback = None

system_prompt = "You are an engine that generates customized programming questions, you try to understand what the person needs to learn and accordingly write the questions"
def llm(context,system=system_prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": context},
        ]
    )
    return response['choices'][0]['message']['content']


generate_question_template =lambda user: f"""
Write a simple question in Python coding language:
The question should be in this topic:{user['subject']}
If the scale of a coding question's difficulty was from 1-10, this question would be in a difficulty of:{user['level']}
The question should be clear and simple.
The question should include a function name.
The question should include 3 different expected outputs of the function.
Do not include code example.
Let's think step by step
code: 
```python

"""

generate_possible_answer =lambda question: f"""Please return only the coding solution for this question and nothing else: {question}"""

next_question_template = lambda user:f"""Write a simple question in Python coding language:
The question should be in this subject:{user['subject']}
We know that the user has this rating on his level (from 1-10, 1 being the worst and 10 being the best) in these topics:
He is {user['params'][0]} in Readability and Formatting(Code Style and Conventions),
He is {user['params'][1]} in Logic and Structure,
He is {user['params'][2]} in Input Handling,
He is {user['params'][3]} in Efficiency,
He is {user['params'][4]} in Modularity,
He is {user['params'][5]} in Error Handling.
The question should be clear and simple.
The question should include a function name and expected output.
The question should include an example result of using the function.
Do not include code example.
Let's think step by step, and write the code
code: 
```python

"""

feedback_template = lambda answer:f"""A user was give this question:
question = '''
{cur_question}
'''
Analyse this answer for the question above based on the topics of:
 Readability and Formatting(Code Style and Conventions) , 
 Logic and Structure, Input Handling, Efficiency, Modularity, Error Handling. 
 Then give it a rating of 1-10 (1 being the worst and 10 being the best) and 
 return the output in a format of a list that looks like this [*rating*,*rating*,*rating*,*rating*,*rating*,*rating*] 
 in the respective order. please return only that list without saying anything else:
{answer}
"""

analysis_template = lambda answer:f"""A user was give this question:
question = '''
{cur_question}
'''
Analyse this answer for the question above based on the topics of:
 Readability and Formatting(Code Style and Conventions) , 
 Logic and Structure, Input Handling, Efficiency, Modularity, Error Handling. 
 Then give it a rating of 1-10 (1 being the worst and 10 being the best):
{answer}
"""

def generate_first_question(user_data):
    cur_question = llm(generate_question_template(user_data))
    return cur_question

def generate_feedback(answer, user_data):
    feedback = llm(feedback_template(answer))
    # match = re.findall(RATING_REGEX, feedback)
    ints = re.findall(INT_REGEX, feedback)
    
    for i in range(6):
        user_data['params'][i] = int(ints[i])

    analysis = llm(analysis_template(answer))
    print(user_data)
    return analysis

def build_possible_answer(question):
    chat_answer = llm(generate_possible_answer(question))
    return chat_answer

def generate_next_question(user_data):
    cur_question = llm(next_question_template(user_data))
    return cur_question



def first_question(user_data:dict)->str:
    return generate_first_question(user_data)

def feedback_maker(answer, user_data)->str:
    return generate_feedback(answer, user_data)
    
def next_question(user_data:dict)->str:
    return generate_next_question(user_data)



def first_question(user_data:dict)->str:
    return generate_first_question(user_data)

def feedback_maker(answer, user_data)->str:
    return generate_feedback(answer, user_data)
    
def next_question(user_data:dict)->str:
    return generate_next_question(user_data)




if __name__ == "__main__":
    user_profile = {"language": None, "level" : None, "user_name" : None, "subject": None, "params": [0,0,0,0,0,0]}
    


