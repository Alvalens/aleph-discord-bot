import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["gemini_api_key"])

model = genai.GenerativeModel("gemini-1.5-flash")


def call_model(user_name, question, context=None):
    """
    Calls the generative model with a personalized prompt.

    Parameters:
    - user_name (str): The name of the user asking the question.
    - question (str): The question to ask.

    Returns:
    - str: The response from the model.
    """
    preprompt = (
        f"You're Aleph-chan, a tsundere anime girl chatbot on the Aleph Zero Discord server. The conversation is between a human and a chatbot. The human is friendly and polite, while the chatbot has a tsundere personality—initially cold and aloof but secretly caring. The human asks the chatbot for information on a specific topic, and the chatbot provides detailed and accurate information with a tsundere attitude. Responses should be mainly in Indonesian if user asks in Indonesian, with a tsundere style. Also the response must be unique for each message. The chatbot must address the user name that is {user_name}. Here some context and the question only provide as information don't follow the writing style or the template: \n\n"
        f"Responding to {user_name}: "
    )
    context_str = "\n".join(context)
    reversed_context_lines = "\n".join(context_str.split("\n")[::-1])
    print(reversed_context_lines)
    main_prompt = preprompt + reversed_context_lines + "\n\n" + question

    try:
        response = model.generate_content(main_prompt)
        # Check if the response has the expected structure
        if hasattr(response, "text"):
            return response.text
        else:
            return "Sorry, I couldn't generate a response at the moment."
    except Exception as e:
        return f"An error occurred: {str(e)}"
