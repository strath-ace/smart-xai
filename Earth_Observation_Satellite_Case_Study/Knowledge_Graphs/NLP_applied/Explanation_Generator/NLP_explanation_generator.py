# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Generates the script and gives the user the option if they are happy tp proceed or provide feedback to
# establish a dialog
# ===========================================================================================================



def NLP_explanation_generator(Results, client, Question, constraints):
    # Loading the solvers results.
    Results = Results.to_json()


    follow_up = ""
    satisfied = "n"
    message = ''

    while satisfied == "n":
        if follow_up == "":
            user_input = {
                "role": "user",
                "content": ''
            }
        else:
            user_input = follow_up

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": constraints + "\nThis is the question:\n" + Question},
                      {"role": "user", "content": "Here are the results from the code generated:\n" + Results},
                      {"role": "user", "content": 'Provide a detailed explanation'},
                      user_input
            ],

            temperature=1,
            max_tokens=1405,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # numpy.set_printoptions(threshold=sys.maxsize)
        print(response.choices[0].message.content)
        # satisfied = "y"
        satisfied = input('Are you satisfied? y to continue, n to add a message: ')

        # Function that cascades the responses and stores in thr form of string to estable a conversation (will use more tokens)
        if satisfied == "n":
            message_new = input('Provide a follow up message: ')
            message = response.choices[0].message.content + '\n'+ message_new + '.' + message
            follow_up = {"role": "user","content": ''+ str(message) +'' }

        else:
            follow_up = user_input


    return response.choices[0].message.content
    # return response['choices'][0]["message"]["content"]

if __name__ == "__main__":

    Results = ''
    client=''
    Question = 'how are you'
    constraints = 'there arent any constraints'

    NLP_explanation_generator(Results, client, Question, constraints)


