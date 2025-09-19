import streamlit as st
from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import re

from key import openapi_key
import os
os.environ['OPENAI_API_KEY'] = openapi_key

llm = OpenAI(temperature=0.7)

st.title("Restaurant name and menu generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine",("American","Mexican","Chinese","Italian","Indian"))

def generate_restaurant_name_and_items(cuisine):
    name_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["cuisine"],
        template="Suggest a great restaurant name for {cuisine} food."
    ),
    output_key="restaurant_name"  
)

    food_items_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["cuisine", "restaurant_name"],
        template="List 5 signature dishes for {cuisine} cuisine at {restaurant_name}."
    ),
    output_key="menu_items"
)

    chain = SequentialChain(
    chains=[name_chain, food_items_chain],
    input_variables=["cuisine"],           
    output_variables=["restaurant_name", "menu_items"],
    
)

    response = chain({"cuisine": cuisine})
    return response

if cuisine:
    response = generate_restaurant_name_and_items(cuisine)

    st.header(response['restaurant_name'].strip())

    raw_items = response['menu_items'].strip()
    menu_items = re.split(r"\n+|\d+\.\s*", raw_items)
    menu_items = [item.strip(" -•") for item in menu_items if item.strip()]

    st.write("**Menu Items**")

    for item in menu_items:
        st.write("-",item)
