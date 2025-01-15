# ------------------Copyright (C) 2023 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Connects to the Assistant of GPT and creates and thread and run for conversations
# ===========================================================================================================
from time import sleep, ctime


def thread_run_generator(client, user_input, assistant_id, thread_id, run_id):
    if thread_id == "":
        # create thread
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread_id = thread_id


    # Add a message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )
    print("message: ", message)




    if run_id =="":
        # create run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            # instructions="Please answer the questions"
        )
        print('run create', run)
        run_id =  run.id
    else:
        run_id =  run_id

    #
    # To retrieve list
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        # run_id="run_6J221SJkELA2Jm1rxUgqSXvf"
        run_id=run_id
    )
    print("run steps", run_steps)

    # To retrieve results
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    # print("run", run)

    counter = 0
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print(f"[{ctime()}]: Working... {run.status}")
        if counter % 10 == 0:
            print(f"\t\t{run}")
        counter += 1
        sleep(5)



    return thread_id, run




