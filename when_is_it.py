from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv() 

from datetime import date

import langchain
from langchain import LLMChain, PromptTemplate
from langchain.llms.cohere import Cohere
from langchain.llms.openai import OpenAI
from langchain.output_parsers import (OutputFixingParser, PydanticOutputParser,
                                      ResponseSchema, StructuredOutputParser)
from langchain.prompts import FewShotPromptTemplate


class Answer(BaseModel):
    answer_date: date = Field(description="The date that answers the question")
    
def get_llm_cohere():    
    llm = Cohere(max_tokens=10)
    return llm

def get_llm_openai():
    llm = OpenAI(max_tokens=10)
    return llm



def get_date_llm_chain():
    llm = get_llm_cohere()

    prefix = """You are a helpful AI assisant answering only the questions that you were asked. 
    The answers are concise and to the point. If you don't know, just say "I don't know".

    {input}
    """

    date_template = PromptTemplate(
        template=prefix,
        input_variables=["input"]
    )
        
    llm_chain = LLMChain(prompt=date_template, llm=llm, )
    return llm_chain

def get_a_date_str(question):
    llm_chain = get_date_llm_chain()

    reply_str = llm_chain.run(question)
    date_str = reply_str.split("\n")[0].strip()

    return date_str

def get_answer(question):
    date_str = get_a_date_str(question=question)
    try:
        answer = Answer(answer_date=date_str)
    except ValidationError as e:
        print(f"Input {date_str} is not in correct format. Error is {e} ")
        raise e

    return answer



