import openai
import streamlit as st
import os

openai.api_key = st.text_input("Enter OpenAI API Key")

if "default" not in st.session_state:
    st.session_state["default"] = "User:\n\n"

st.title('System: You are a helpful assistant.')
    
prompts = st.text_area(
    "Input prompt", value=st.session_state["default"], height=500
)

models = ['gpt-3.5-turbo', 'text-davinci-003', 'gpt-4']
model = st.sidebar.selectbox("Select Model", models)

with st.sidebar:
    if ((model == 'gpt-3.5-turbo') or (model == 'text-davinci-003')):
        max_ = 4096
    else:
        max_ = 8192
    st.subheader("Advanced Settings")
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    
    max_tokens = st.slider("Max Tokens", min_value=64, max_value=max_, value=1024, step=64)
    top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=1.0, step=0.1)
    frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    n = st.slider("n", min_value=1, max_value=5, value=1, step=1)
    
    # Add best_of option for text-davinci-003
    if model == 'text-davinci-003':
        best_of = st.slider("Best Of", min_value=1, max_value=5, value=1, step=1)

if st.button('Submit'):
    prompts = 'System: You are a helpful assistant:\n\n'+prompts+'\n\nAssistant:\n\n'
    
    if model == 'text-davinci-003':
        response = openai.Completion.create(
        engine=model,
        prompt=prompts,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=n,
        best_of=best_of
    )
        response_output = response['choices'][0]['text']
    else:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompts}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=n
        )
        response_output = response['choices'][0]['message']['content']

    print(response)
    
    st.session_state["default"] = prompts.lstrip('System: You are a helpful assistant:\n\n') + response_output + '\n\nUser:\n\n'
    st.experimental_rerun()

if st.button('Reset'):
    st.session_state["default"] = ""
    st.experimental_rerun()