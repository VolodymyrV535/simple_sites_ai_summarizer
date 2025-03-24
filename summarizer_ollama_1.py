# imports
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


# Constants
MODEL = "llama3.2"

# A class to represent a Webpage
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
        
        
# initialize openai object
openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')


############################################## constants ########################################################################################
# site to summarize
URL = "https://edwarddonner.com"

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."
SYSTEM_PROMPT = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


############################################## functions definitions ##############################################################################
# A function that writes a User Prompt that asks for summaries of websites:
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# See how this function creates exactly the format above
def messages_for(website):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt_for(website)}
    ]


# call the OpenAI API.
def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = MODEL,
        messages = messages_for(website)
    )
    return response.choices[0].message.content


# A function to display summary in markdown format
def display_summary(url):
    summary = summarize(url)
    print(summary)
    
    
###################################################### main program #############################################################
display_summary(URL)
