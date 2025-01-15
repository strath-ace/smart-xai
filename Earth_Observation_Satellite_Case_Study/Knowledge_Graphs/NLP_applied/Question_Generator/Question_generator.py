# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Main File to generate questions with feedback based on the categories selected from the menu
# ===========================================================================================================

from GPT_connector import GPT_connector
from openai import OpenAI#, AsyncOpenAI

OPENAI_API_KEY = GPT_connector()

client = OpenAI(api_key=OPENAI_API_KEY)

# thread_id = "thread_0PKzXbE8rSggsSxKkH3KV3Kh"
# assistant_id = "<Put ID here>"


def question_generator(file_name, thread_id, run_id, thread_run_generator,assistant_id, num):
    satisfactory = "n"
    # Receives the input from the prompt for the category
    follow_up = input('Enter additional message if it is not the first run, leave blank or enter information to continue: ')
    while satisfactory == "n":
        if follow_up == "":
            user_input = open(file_name + ".txt", "r")
            user_input = user_input.read()
            user_input = user_input + "Can you make "+ str(num) + " question/s similar to the example questions using the file attached? Only provide the questions nothing more"
            print(user_input)
        else:
            user_input = user_input

        # thread Id and Run ID are created for assistant api dialog
        thread_id, run = thread_run_generator(client, user_input, assistant_id, thread_id, run_id)


        input('\nPress anything to continue')

        # time.sleep(10)  # Makes Python wait for 5 seconds
        # -------------------------to retrieve results

        run_steps = client.beta.threads.runs.steps.list(
            thread_id=thread_id,
            # run_id ="run_6J221SJkELA2Jm1rxUgqSXvf"
            run_id=run.id
        )
        print(run_steps)



        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        print(run)

        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages)

        print("message: ", messages.data[0].content[0].text.value)

        satisfactory = input('\nIs this satisfactory? y/n: ')

        if satisfactory == "n":
            follow_up = input('Provide a follow up message: ')
        else:
            follow_up = user_input


    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    # print(messages)
    # print(messages.data[0].content[0].text.value)

    return messages.data[0].content[0].text.value

