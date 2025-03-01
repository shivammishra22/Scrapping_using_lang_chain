#Gradio Day!
import day_01

import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import gradio as gr

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Connect to OpenAI, Anthropic and Google; comment out the Claude or Google lines if you're not using them

openai = OpenAI()


genai.configure()

# A generic system message - no more snarky adversarial AIs!

system_message = "You are a helpful assistant"

# Let's wrap a call to GPT-4o-mini in a simple function

def message_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    completion = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
    )
    return completion.choices[0].message.content

# This can reveal the "training cut off", or the most recent date in the training data

# print(message_gpt("What is today's date?"))


def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()
shout("hello")

# gr.Interface(fn=shout, inputs="textbox", outputs="textbox",allow_flagging='never').launch(share=True)

# Inputs and Outputs

# view = gr.Interface(
#     fn=message_gpt,
#     inputs=[gr.Textbox(label="Your message:", lines=6)],
#     outputs=[gr.Textbox(label="Response:", lines=8)],
#     flagging_mode="never"
# )
# view.launch()

system_message = "You are a helpful assistant that responds in markdown"

# view = gr.Interface(
#     fn=message_gpt,
#     inputs=[gr.Textbox(label="Your message:")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()


def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

# view = gr.Interface(
#     fn=stream_gpt,
#     inputs=[gr.Textbox(label="Your message:")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()


def stream_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    response = model.generate_content(prompt, stream=True)

    accumulated_response = ""
    for chunk in response:
        accumulated_response += chunk.text or ""
        yield accumulated_response

# view = gr.Interface(
#     fn=stream_gemini,
#     inputs=[gr.Textbox(label="Your message:")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()


def stream_model(prompt, model):
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

# view = gr.Interface(
#     fn=stream_model,
#     inputs=[gr.Textbox(label="Your message:"), gr.Dropdown(["GPT", "gemini"], label="Select model", value="GPT")],
#     outputs=[gr.Markdown(label="Response:")],
#     flagging_mode="never"
# )
# view.launch()
#------------------------------------------------------------------------------------------
# With massive thanks to Bill G. who noticed that a prior version of this had a bug! Now fixed.

system_message = "You are an assistant that analyzes the contents of a company website landing page \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown."

def stream_brochure(company_name, url, model):
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += day_01.Website(url).get_contents()
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

view = gr.Interface(
    fn=stream_brochure,
    inputs=[
        gr.Textbox(label="Company name:"),
        gr.Textbox(label="Landing page URL including http:// or https://"),
        gr.Dropdown(["GPT", "gemini"], label="Select model")],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)
view.launch()

