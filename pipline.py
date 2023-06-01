import langchain as lc
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.prompts import load_prompt
import wikipedia
import os
import streamlit as st

import openai

openai.api_key = "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"

prompt = "i am learning python give me exercise to practice if-else"
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
generate_question_template =lambda topic: f"""Write a simple question in Python:
The question should be in this topic:{topic}
The question should be clear and simple, without any difficulties
Let's think step by step, and write the code
code: 
```python

"""


subtopic_template = lambda questoin, answer:f"""Kim answered the question {questoin},
her answer was {answer}.
The list of topics that Kim does not seem to know:
1."""


next_question_template = lambda topic, subtopics:f"""Write a short code question that deals with this topic:{topic}
and refers to these sub-topics:{subtopics}
The question should be clear and simple, without any difficulties
Let's think step by step, and write the code
code: 
```python"""

def generate_question_chain(topic):
    return llm(generate_question_template(topic))
def subtopic_chain(questoin,answer):
    return llm(subtopic_template(questoin,answer))
def next_question_chain(topic,subtopic):
    return llm(next_question_template(topic,subtopic))


def generate_question(user_data:dict)->str:
    return generate_question_chain(topic=user_data["subject"])
    


def next_question(questoin:str,answer:str,user_dict:dict)->str:
    subtopic = subtopic_chain(questoin=questoin, answer=answer)
    return next_question_chain(topic = user_dict["subject"],subtopic=subtopic)







if __name__ == "__main__":
    user_profile = {"language": "python", "level" : None, "user_name" : None, "subject": "dictionary", "weaknesses": None}
    q=generate_question(user_profile)
    print("Q: "+q+"\n")
    print(next_question(q,input("enter answer"),user_profile))


