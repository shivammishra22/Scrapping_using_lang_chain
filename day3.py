import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

openai = OpenAI()
MODEL = 'gpt-3.5-turbo'

system_message = "You are a helpful assistant"

# It's now just 1 line of code to prepare the input to OpenAI!

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response
gr.ChatInterface(fn=chat, type="messages").launch()