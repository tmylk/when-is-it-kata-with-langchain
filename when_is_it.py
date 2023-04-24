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

    examples = [ 
        {'question': "When is your birthday?",
          'answer': "2020-02-24"},
         {'question': "What is your favourite date?",
          'answer': "1999-03-14"},
        {'question': "What is your friend's favourite date?",
          'answer': "1991-01-01"},
        {'question': "When is Labour Day in 1990?",
          'answer': "1990-05-01"},



          ]

    example_prompt = PromptTemplate(input_variables=["question", "answer"], template="""Question: {question} Answer: {answer}  \n""")

    prefix = """You are a helpful AI assisant answering only the questions that you were asked. 
    The answers are concise and to the point. If you don't know, just say "I don't know".

    The correct date format is YYYY-MM-DD., e.g. 2020-02-24.

    """

    date_template = FewShotPromptTemplate(
    prefix=prefix,
    examples=examples, 
    example_prompt=example_prompt,
    suffix="Question: {input} Answer:", 
    input_variables=["input"]
    )
    
    
    #new_parser = OutputFixingParser.from_llm(llm=llm, parser=None)
    # prompt_template = PromptTemplate(template=date_template,
    #                                 input_variables=["question"],
    #                                 partial_variables={"format_instructions": output_parser.get_format_instructions()},
    #                                 output_parser=output_parser)
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



