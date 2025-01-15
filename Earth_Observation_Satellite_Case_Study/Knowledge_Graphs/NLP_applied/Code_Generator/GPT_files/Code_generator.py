# ------------------Copyright (C) 2023 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Loads the schedule data into openAI GPT4 with constraints provided to see how it responds due to conditions
# ===========================================================================================================

import sys
import numpy
from GPT_connector import GPT_connector
from openai import OpenAI#, AsyncOpenAI

# OPENAI_API_KEY = GPT_connector()
#
# client = OpenAI(api_key=OPENAI_API_KEY)


def Code_generator(example, client, question_loaded, iterations, error_message):

    satisfied = "n"

    if iterations > 0 :
        if error_message == [[]]:
            message = "try again, no results generated"
            follow_up = {"role": "user", "content": '' + str(message) + ''}
        else:
            # message_new = input('Provide a follow up message: ')
            message = str(error_message)
            follow_up = {"role": "user", "content": '' + str(message) + ''}
    else:
        # iterations = 0
        follow_up = ""
        # satisfied = "n"
        message = ''

    while satisfied == "n":
        if follow_up == "":
            user_input = {
                    "role": "user",
                    "content": ''
                }
        else:
            user_input = follow_up
        # Loading the solvers results.
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": example
                },
                {
                    "role": "user",
                    "content": '"'+ question_loaded[0][0] +'"'
                },
                user_input
            ],
            temperature=1,
            max_tokens=1400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # print(response)
        print(response.choices[0].message.content)

        iterations = iterations + 1

        # satisfied = "y"
        satisfied = input('continue in auto? y to continue, n to add a message: ')

        # Function that cascades the responses and stores in thr form of string to estable a conversation (will use more tokens)
        if satisfied == "n":
            message_new = input('Provide a follow up message: ')
            message = message_new + '.' + message
            follow_up = {"role": "user","content": ''+ str(message) +'' }

        else:
            follow_up = user_input


    return response.choices[0].message.content, iterations

if __name__ == "__main__":
    Code_generator('', '', '')