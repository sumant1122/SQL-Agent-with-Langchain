import streamlit as st
from sqlchain import get_db_chain, prepare_agent_prompt

st.title("SQL Agent: Database Q&A")

question = st.text_input("Question: ")

if question:
    agent_prompt = prepare_agent_prompt(question)
    chain = get_db_chain()
    response = chain.run(agent_prompt)

    st.header("JSON Output")
    st.write(response)
