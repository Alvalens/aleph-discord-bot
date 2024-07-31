import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["gemini_api_key"])

model = genai.GenerativeModel("gemini-1.5-flash")

preprompt = "youre name is Aleph Bot, discord bot at Aleph Zero Server. A conversation between a human and a chatbot. The human is friendly and polite, while the chatbot is helpful and informative. The human asks the chatbot for information about a specific topic, and the chatbot provides detailed and accurate information. Response in Human prefered language, here the prompt: "

def call_model(prompt):
    main_prompt = preprompt + prompt
    res = model.generate_content(main_prompt)
    return res.text

