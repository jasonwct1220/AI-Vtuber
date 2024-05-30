import openai
import keys

#Import the prompt from the text file
def prompt(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

#Create openai client instance
from openai import OpenAI
client = OpenAI(
    api_key=keys.OPENAI_API_KEY
) 
#openai.api_base = 'https://api.openai.com/v1/chat'

#Get the responses from gpt 3.5 turbo model
def gpt(messages):
    output = client.chat.completions.create(
        model='ft:gpt-3.5-turbo-1106:personal:model-1:9GpBYIaD',
        messages=messages,
        temperature=0.9,
        max_tokens=256,
        frequency_penalty=2,
        presence_penalty=2
        )
    reply = output.choices[0].message.content
    return reply

#Get the responses from gpt 4 model
def gpt4(messages):
    output = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=0.9,
        max_tokens=256,
        frequency_penalty=2,
        presence_penalty=2
        )
    reply = output.choices[0].message.content
    return reply
