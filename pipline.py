import langchain as lc
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.prompts import load_prompt
import wikipedia
import os

llm = OpenAI()
# save templates to a file
try_imply_template = """Question:
 The user wrote me the following text, what is he trying to imply to me?
 {user_input}

Answer: Let's think step by step."""
# An example prompt with multiple input variables
TI_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=try_imply_template,
)


connection_between_terms_template = PromptTemplate(
    template="""Question:
 What is the connection between {term1} and {term2}?
 Answer: Let's think step by step.""",
    input_variables=["term1", "term2"],
)


chain_TI = LLMChain(prompt=TI_prompt, llm=llm)
chain_CC = LLMChain(prompt=connection_between_terms_template, llm=llm)


if __name__ == "__main__":
    print(chain_TI.run("I am happy"))
    print(chain_CC.run(["I am sad", "I am happy"]))