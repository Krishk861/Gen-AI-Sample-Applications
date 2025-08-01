import os
from dotenv import load_dotenv

from langchain_community.llms import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="True"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

## Prompt templater
prompt=ChatPromptTemplate.from_messages(
    [
        {"system","You are a helpful Assistant.Please respond to the question asked."}
        ("user","Question{question}")
    ]
)

## Steamlit framework
st.title("Langchain Demo with llama2")
input_text=st.text_input("What question you want to ask?")

###Ollama llam2 model
llm=ollama("gemma:2b")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))