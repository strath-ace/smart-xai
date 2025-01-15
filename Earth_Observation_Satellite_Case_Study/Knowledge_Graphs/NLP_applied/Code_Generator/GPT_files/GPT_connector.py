import openai
import os
def GPT_connector():

    openai.api_key = os.environ["OPENAI_API_KEY"]
    key = openai.api_key
    return key
