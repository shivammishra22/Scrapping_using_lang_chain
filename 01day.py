import os
import requests
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

load_dotenv()

llm=ChatGroq(model_name="Gemma2-9b-It", api_key="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")

# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

ed = Website("https://edwarddonner.com")
print(ed.title)
print(ed.text,'\n','-----------------------------------------------------')

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

# A function that writes a User Prompt that asks for summaries of websites:

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# print(user_prompt_for(ed))

# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Try this out, and then try for a few more websites

print("\n",'*********************************************',"\n",messages_for(ed))


# And now: call the OpenAI API. You will get very familiar with this!



llm = ChatGroq(model_name="Gemma2-9b-It", api_key="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")

def summarize(url):
    website = Website(url)
    messages = messages_for(website)
    
    response = llm.invoke(messages)
    
    return response

print('\n','++++++++++++++++++++++++++++++++++++++','\n',summarize("https://edition.cnn.com/"))


