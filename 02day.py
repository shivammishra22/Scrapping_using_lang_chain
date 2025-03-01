import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from IPython.display import Markdown, display, update_display


load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GEMINI_API_KEY')
deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')

genai.configure()

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
# if anthropic_api_key:
#     print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
# else:
#     print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

# Optionally if you wish to try DeekSeek, you can also use the OpenAI client library
if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API\n")

openai = OpenAI()

system_message = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
  ]

# GPT-3.5-Turbo

# completion = openai.chat.completions.create(model='gpt-3.5-turbo', messages=prompts)
# print(completion.choices[0].message.content)



gemini = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    system_instruction=system_message
)
response = gemini.generate_content(user_prompt)
# print("Hi I am GEMINI-----",response.text)


# Let's make a conversation between GPT-4o-mini and Claude-3-haiku
# We're using cheap versions of models so the costs will be minimal

gpt_model = 'gpt-3.5-turbo'
gemini_model = 'gemini-2.0-flash-exp'

gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

gemini_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

gpt_messages = ["Hi there"]
gemini_messages = ["Hi"]

def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, gemini in zip(gpt_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": gemini})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

print(call_gpt())

def call_gemini():
    messages = [{"role": "user", "parts": [{"text": gemini_system}]}]  # System message formatted correctly

    for gpt, gemini_message in zip(gpt_messages, gemini_messages):
        messages.append({"role": "user", "parts": [{"text": gpt}]})  # Corrected key from 'content' to 'parts'
        messages.append({"role": "model", "parts": [{"text": gemini_message}]})  # Gemini uses 'model' instead of 'assistant'

    # Add the final user message
    messages.append({"role": "user", "parts": [{"text": gpt_messages[-1]}]})

    # Call Gemini model
    model = genai.GenerativeModel(gemini_model)
    response = model.generate_content(messages)

    return response.text 

# print(call_gemini())

# print(call_gpt())

gpt_messages = ["Hi there"]
gemini_messages = ["Hi"]

print(f"GPT:\n{gpt_messages[0]}\n")
print(f"gemni:\n{gemini_messages[0]}\n")

for i in range(5):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)
    
    gemini_next = call_gemini()
    print(f"gemini:\n{gemini_next}\n")
    gemini_messages.append(gemini_next)
