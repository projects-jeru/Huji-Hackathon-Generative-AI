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
feedback = None

prompt = "i am learning python give me exercise to practice coding"
def llm(context,system="You are a helpful assistant."):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": context},
        ]
    )
    return response['choices'][0]['message']['content']

# # save 
generate_question_template =lambda user: f"""Write a simple question in Python coding language:
The question should be in this topic:{user['subject']}
If the scale of a coding question's difficulty was from 1-10, this question would be in a difficulty of:{user['level']}
The question should be clear and simple.
The question should include a function name and expected output.
The question should include an example usage of the function.
Let's think step by step, and write the code
code: 
```python

"""


# subtopic_template = lambda questoin, answer:f"""Kim answered the question {questoin},
# her answer was {answer}.
# The list of topics that Kim does not seem to know:
# 1."""


next_question_template = lambda user:f"""Write a simple question in Python coding language:
The question should be in this topic:{user['subject']}
If the scale of a coding question's difficulty was from 1-10, this question would be in a difficulty of:{user['level']}
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
    match = re.findall(RATING_REGEX, feedback)[0]
    ints = re.findall(INT_REGEX, "\b\d+\b")
    
    print("feedback" , feedback)
    # for i in range():
    #     user_data['params'][i] = int(feedback[i])
    #     print(user_data)

    # analysis = llm(analysis_template(answer))
    # return analysis

def generate_next_question(user_data):
    cur_question = llm(next_question_template(user_data))
    return cur_question



# def subtopic_chain(questoin,answer):
#     return llm(subtopic_template(questoin,answer))
# def next_question_chain(topic,subtopic):
#     return llm(next_question_template(topic,subtopic))


def first_question(user_data:dict)->str:
    return generate_first_question(user_data)

def feedback_maker(answer, user_data)->str:
    return generate_feedback(answer, user_data)
    
def next_question(user_data:dict)->str:
    return generate_next_question(user_data)

# def next_question(questoin:str,answer:str,user_dict:dict)->str:
#     subtopic = subtopic_chain(questoin=questoin, answer=answer)
#     return next_question_chain(topic = user_dict["subject"],subtopic=subtopic)




def first_question(user_data:dict)->str:
    return generate_first_question(user_data)

def feedback_maker(answer, user_data)->str:
    return generate_feedback(answer, user_data)
    
def next_question(user_data:dict)->str:
    return generate_next_question(user_data)

# def next_question(questoin:str,answer:str,user_dict:dict)->str:
#     subtopic = subtopic_chain(questoin=questoin, answer=answer)
#     return next_question_chain(topic = user_dict["subject"],subtopic=subtopic)







if __name__ == "__main__":
    user_profile = {"language": "python", "level" : None, "user_name" : None, "subject": "dictionary", "weaknesses": None}
    q=generate_question(user_profile)
    print("Q: "+q+"\n")
    print(next_question(q,input("enter answer"),user_profile))


