# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# The main file that calls all functions to generate a solution through the menu
# ===========================================================================================================


from Google_sheets.sheet_code_generator import sheet_code_generator
from Explanation_Generator.extract_google_sheets import extract_question, extract_info, locate_number_google_sheets
from Explanation_Generator.NLP_explanation_generator import NLP_explanation_generator
from Google_sheets.Sheet_updates import get_values, update_values, append_values
from Code_Generator.GPT_files.Code_generator import Code_generator
from Code_Generator.TypeDB_executor import TypeDB_executor
from Question_Generator.Question_generator import question_generator
from Question_Generator.GPT_files.thread_run_generator import thread_run_generator
from Scoring.Scoring import bert_score, cosine_score
from Scoring.bell_chart import bell_chart
from google.oauth2.credentials import Credentials
from GPT_connector import GPT_connector
from openai import OpenAI  # , AsyncOpenAI
from googleapiclient.discovery import build
import time
import pandas as pd
import string

# Load openAI API key
OPENAI_API_KEY = GPT_connector()

client = OpenAI(api_key=OPENAI_API_KEY)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)

spreadsheet_id =  input("<Enter Google sheet ID here>:  ")
service = build("sheets", "v4", credentials=creds)

nonalpha = string.digits + string.punctuation + string.whitespace


def main():
    # Select the correct worksheet in Google Sheets

    worksheet = int(input(
        'Enter worksheet name \n0. Sheet1 \n1. Swap_actions \n2. Single_substitution \n3. Verification  \n4. Forward_Backward: '))

    if worksheet == 1:
        worksheet_name = "Swap_actions"
    elif worksheet == 2:
        worksheet_name = "Single_Substitution"
    elif worksheet == 3:
        worksheet_name = "Verification"
    elif worksheet == 4:
        worksheet_name = "Forward_Backward"
    elif worksheet == 0:
        worksheet_name = "Sheet1"
    else:
        worksheet_name = "Please Enter a worksheet number"

    # Select the respective worksheet
    range1 = worksheet_name + "!"

    query_required = input("Would you like GPT generate queries y/n: ")
    # query_required ="n"

    if query_required == "y":
        query_num = int(input("How many questions would you like to create?: "))
        # Used for question creation only
        assistant_id = input('Enter Assistant ID for creating questions, can be retrieved from OPenAI playground IS REQUIRED: ')
        thread_id = input(
            'Enter thread ID, to proceed with the dialog, otherwise leave blank if unknown or the first time continue: ')
        run_id = input('Enter run ID, leave blank if unknown or enter ID to continue: ')

        worksheet_dir = "Question_Generator/GPT_files/Prompt_files/"
        worksheet_file = worksheet_dir + worksheet_name

        # Load the question created by GPT here
        question_generated = question_generator(worksheet_file, thread_id, run_id, thread_run_generator, assistant_id,
                                                query_num)

        # Range is always required for data retrieval/entry
        lines = question_generated.split('\n')
        print(len(lines), lines)
        # separate the numbers into lines for each cell
        for i in range(0, len(lines)):
            if lines[i] != '':

                print(lines[i].lstrip(nonalpha))

                list_lines = lines[i].lstrip(nonalpha)

                # Get the data length from the worksheet
                data_len, _ = get_values(spreadsheet_id, range1 + "A1:C200", creds)
                if data_len == 0:
                    column_headings = [
                        ['Question number', 'thread_ID', 'Algorithm', 'Human Explantion', 'Explanations',
                         'Human Assessment 1 Correctness',
                         'Human Assessment 1 Validation', 'Human Assessment 2 Correctness',
                         'Human Assessment 2 Validation', 'Average Correctness', 'Average Validation',
                         'Bert Score - Precision', 'Bert Score - Recall', 'Bert Score - f1', 'Final Score',
                         'Word Count Human', 'Word Count GPT', 'Average_Cosine_similarity for questions', '',
                         'Iterations1', '', '', 'Cos_Swap', 'Cos_Single_Sub', 'Cos_Verification',
                         'Cos_Forward_Backward'], [1]]

                    # Creates the column headings for the next sheet
                    append_values(spreadsheet_id, range1 + "A" + str(data_len + 1),
                                  "USER_ENTERED",
                                  ["A"], column_headings, creds
                                  )
                    # Continue to add data to the next set of cells based on location of last entry
                    update_values(spreadsheet_id, range1 + "B" + str(data_len + 2),
                                  "USER_ENTERED",
                                  ["B"], list_lines, creds
                                  )

                    # Place column heading on results page
                    column_headings2 = [0, 'Questions', 'Results']
                    # Creates the column headings for the next sheet
                    append_values(spreadsheet_id, worksheet_name + '_Table_results!' + "A" + str(data_len + 1),
                                  "USER_ENTERED",
                                  ["A"], column_headings2, creds
                                  )



                else:

                    append_values(spreadsheet_id, range1 + "A" + str(data_len + 1),
                                  "USER_ENTERED",
                                  ["A"], [[data_len, list_lines]], creds
                                  )

                print(data_len)
    repeat = "y"
    # repeat = input("Have all the questions been generated? (y/n): ")
    rep = 0
    # int(input("What is the maximum number of questions?: ")) + 1
    max_num = 21
    while repeat == "y" and rep <= max_num:
        # code_required ="n"
        code_required = input("Would you like GPT generate a code y/n: ")
        # Create the code
        question_number = ''
        if code_required == "y":
            # Get the data length (current position) and all data entered from the worksheet in Column C for new data entry
            data_lenc, row_data = get_values(spreadsheet_id, range1 + "C1:C2000", creds)

            cell_num = data_lenc + 1
            print(cell_num)

            # Get the question from the worksheet from Column B using position of x (use next cell of x to locate the next question)
            data_lenb, question_loaded = get_values(spreadsheet_id, range1 + "B" + str(data_lenc), creds)

            # Locate file with example prompt
            example = open("Code_Generator/GPT_files/Prompt_files/for_all_conditions.txt", "r")
            example = example.read()

            message = ''
            iterations = 0
            # checks if there are errors in the code and reruns automatically, may need supervision for verification and forward_backward
            # Also does 2 additional runs per code, can be bypassed as this is an optional step
            Rerun = 'uncertain'
            while Rerun == 'uncertain':
                # Option for code rerun for 2 or 3 to record code iterations. It checks if the code is executable and proceeds
                Rerun = input(
                    "Is this a code re-run? Meaning, is this for generation code the 2nd or the first time?: y/n: ")

                if Rerun == "y":
                    if question_number != '':
                        question_number = question_number
                    else:

                        question_number = int(input("Enter the question number: "))

                    sheet_name = 'Code_rerun_'
                    # load the question generated by extracting it from original sheet
                    cell_num, question_loaded = extract_info(spreadsheet_id, sheet_name + range1, str(question_number),
                                                             "B", service)

                    print(cell_num, question_loaded)
                    # number_number_version = 2
                    # checks if this the 2nd or 3rd time the codes are being run and store the results in the respective cells
                    number_number_version = int(input("what number rerun is this 2 or 3?: "))
                    if number_number_version == 2:

                        col_code_store = "C"
                        col_iter_store = "E"
                        Rerun = 'proceed'

                    elif number_number_version == 3:

                        col_code_store = "D"
                        col_iter_store = "F"
                        Rerun = 'proceed'
                    else:
                        print("error, version not entered ")
                        Rerun = 'uncertain'
                else:
                    sheet_name = ''
                    col_code_store = "C"
                    col_iter_store = "T"
                    Rerun = 'proceed'

            data_results = 'Error'
            while 'Error' in str(data_results) or 'error' in str(data_results) or data_results == [[]]:

                # Generate the code using GPT here
                code_generated, iterations = Code_generator(example, client, question_loaded, iterations, message)
                # Execute the code to create a Knowledge graph and store the results
                data_results = TypeDB_executor(str(code_generated))
                message = data_results

            else:
                data_results = ''

                # Store the code
                sheet_code_generator(worksheet_name, spreadsheet_id, str(cell_num), update_values, append_values,
                                     [code_generated, iterations], question_loaded, data_results, str(question_number),
                                     get_values, creds, sheet_name + range1, col_code_store, col_iter_store)

        # OPTIONAL - Code RE-RUN
        # USed for storing the results
        # Execute the code to create a Knowledge graph and store the results
        # execute_code_required = "n"
        execute_code_required = input("Do you want to execute the code? y/n: ")

        if execute_code_required == "y":
            question_number = int(input("What question would you like to get: "))

            # load the code generated
            cell_num, code_generated = extract_info(spreadsheet_id, range1, str(question_number), "C", service)

            # Test the code and get results
            data_results = TypeDB_executor(code_generated[0][0])

            # Copy the question number and question across from the original sheet before the answers are loaded
            cell_num, question_loaded, _ = extract_question(spreadsheet_id, range1, str(question_number), service)

            # Store the results here
            sheet_code_generator(worksheet_name, spreadsheet_id, str(cell_num), update_values, append_values,
                                 code_generated, question_loaded, data_results, str(question_number),
                                 get_values, creds, _, _, _)

            print("code..done")

        # Request explanations
        explanation_required = input("Explanation required from Knowledge Graph? y/n: ")
        # explanation_required = "n"
        # Generate the script using the results from the Knowledge graph
        if explanation_required == "y":

            question_number = int(input("What question would you like to get: "))

            # Sheet containing results
            table_worksheet = worksheet_name + "_Table_results!"

            # Load constraint prompt -------------------
            constraints = open("Explanation_Generator/GPT_files/Prompt_files/NLP_script_generation_prompt.txt",
                               "r")
            constraints = constraints.read()

            explanation_example = open(
                "Explanation_Generator/GPT_files/Prompt_files/" + worksheet_name + "_example.txt",
                "r")
            explanation_example = explanation_example.read()

            human_input_req = input("Is a human input required for the LLM response? y/n: ")
            # human_input_req = "n"
            if human_input_req == "y":
                constraints = constraints + explanation_example
                updated_sheet_name = 'human_'
            else:
                constraints = constraints
                updated_sheet_name = ''

            # locate table results/Extract googlesheets in the form of pandas data
            cell_num, question, tabulated_kg_results = extract_question(spreadsheet_id, table_worksheet,
                                                                        str(question_number), service)

            explanation = NLP_explanation_generator(tabulated_kg_results, client, question[0][0], constraints)

            sheet, values, cell_num2, cell_num3 = locate_number_google_sheets(spreadsheet_id,
                                                                              updated_sheet_name + range1 + "A1:A3000",
                                                                              str(question_number), service)

            # Add explainations/Results to the next set of cells (column E) of original sheet based on location of last entry
            update_values(spreadsheet_id, updated_sheet_name + range1 + "E" + str(cell_num2),
                          "USER_ENTERED",
                          ["B"], explanation, creds
                          )

        # Request if scoring is required
        scoring_required = input("Is bert score required? y/n: ")
        # scoring_required = "n"

        # Generate the score
        if scoring_required == "y":
            if rep != 0:
                question_number = rep
            else:

                question_number = int(input("What question would you like to get: "))
            # question_number = int(input("What question would you like to get: "))
            # human_input_req = input("Is a human input required for the LLM response? y/n: ")

            human_input_req = "n"
            if human_input_req == "y":
                updated_sheet_name = 'human_'
            else:
                updated_sheet_name = ''

            # load the explanations generated
            cell_num, explanations_generated = extract_info(spreadsheet_id, updated_sheet_name + range1,
                                                            str(question_number), "E", service)

            # load the reference explanations
            _, refs = extract_info(spreadsheet_id, updated_sheet_name + range1, str(question_number), "D", service)

            precision, recall, f1 = bert_score(explanations_generated[0], refs[0])

            scored_results = precision, recall, f1

            for i in range(0, len(scored_results)):
                if i == 0:
                    column = "L"
                    print(column, i, scored_results[i][0])
                    score = scored_results[i][0]
                elif i == 1:
                    column = "M"
                    print(column, i, scored_results[i][0])
                    score = scored_results[i][0]
                else:
                    column = "N"
                    print(column, i, scored_results[i][0])
                    score = scored_results[i][0]

                # Add Scored Results to the next set of cells (column F) of original sheet based on location of last entry
                update_values(spreadsheet_id, updated_sheet_name + range1 + column + str(cell_num),
                              "USER_ENTERED",
                              [column], score, creds)

        # cos_score_required = input("Is cosine similarity score required? y/n: ")
        cos_score_required = "n"

        # Generate the cosine similarity
        if cos_score_required == "y":
            question_number = int(input("What question would you like answered: "))
            # question2 = []
            sol = []
            # cell_num, question1, _ = extract_question(spreadsheet_id, range1,
            #                                                                     str(question_number))
            cross_category_comparison = input("Whould you like a cross category comparison done? y/n: ")
            column_input_update = 'R'
            updated_sheet_name = worksheet_name
            if cross_category_comparison == "y":
                cross_cat = int(input(
                    'Enter worksheet name to cross compare with  \n1. Swap_actions \n2. Single_substitution \n3. Verification  \n4. Forward_Backward: '))

                if cross_cat == 1:
                    updated_sheet_name = "Swap_actions"
                    column_input_update = 'W'
                elif cross_cat == 2:
                    updated_sheet_name = "Single_Substitution"
                    column_input_update = 'X'
                elif cross_cat == 3:
                    updated_sheet_name = "Verification"
                    column_input_update = 'Y'
                elif cross_cat == 4:
                    updated_sheet_name = "Forward_Backward"
                    column_input_update = 'Z'
                else:
                    updated_sheet_name = "Please Enter a worksheet number"
                    column_input_update = 'R'
            elif cross_category_comparison == "n":
                updated_sheet_name = worksheet_name

            for z in range(question_number, max_num + 1):
                cell_num, question1, _ = extract_question(spreadsheet_id, range1,
                                                          str(z), service)

                if updated_sheet_name == worksheet_name:

                    for i in range(1, max_num):
                        if i != z:
                            # locate table results/Extract googlesheets in the form of pandas data
                            _, question2 = extract_info(spreadsheet_id, updated_sheet_name + '!', str(i), "B", service)
                            # question2.append(question)
                            print(i, question2[0])
                            sol.append(float(cosine_score(question1[0], question2[0])))
                else:
                    for i in range(1, max_num):
                        # if i != z:
                        # locate table results/Extract googlesheets in the form of pandas data
                        _, question2 = extract_info(spreadsheet_id, updated_sheet_name + '!', str(i), "B", service)
                        # question2.append(question)
                        print(i, question2[0])
                        sol.append(float(cosine_score(question1[0], question2[0])))

                if z >= question_number:
                    # Remove square brackets from list and input as function to spreadsheet
                    function = "=Average(" + str(sol)[1:-1] + ")"

                    # Add Scored Results to the next set of cells (column R) of original sheet based on location of last entry
                    update_values(spreadsheet_id, range1 + column_input_update + str(cell_num),
                                  "USER_ENTERED",
                                  [column_input_update], function, creds)
                time.sleep(60)

        # Request if graphs are required
        graph_required = "y"
        # graph_required = input("Are graphs required? y/n: ")
        # Generate the cosine similarity
        if graph_required == "y":
            # compare_question = input("  Cosine comparison of questions plot required? y/n: ")
            compare_question = "n"
            cols = ["Swap_actions", "Single_Substitution", "Verification", "Forward_Backward"]
            # human_input_req = input("  Human prompt? y/n: ")
            human_input_req = "y"
            if human_input_req == "y":
                updated_sheet_name = 'human_'
            else:
                updated_sheet_name = ''

            plot_data2 = []
            if compare_question == "y":

                for t in cols:
                    plot_data = []
                    for i in range(1, max_num):
                        # print(t,i)
                        # locate table results/Extract googlesheets in the form of pandas data
                        _, cosine_plot_data = extract_info(spreadsheet_id, updated_sheet_name + t + "!", str(i), "R",
                                                           service)
                        plot_data.append(float(cosine_plot_data[0][0]))

                    # plot_data.insert(0, t)
                    plot_data2.append(plot_data)
                    print(plot_data2)
                    time.sleep(60)
                fig_subtitle = "Cosine Similarity"
                plot_label = 'Cosine Similarity'
                fig_name = "Q_Cosine_Similarity.png"
                plot_data2 = pd.DataFrame(plot_data2).transpose()
                plot_data2.columns = cols
                print(plot_data2)
                bell_chart(plot_data2, plot_label, fig_name, fig_subtitle)

            # If the LLM human comparison is required
            LLM_Human = "y"
            # LLM_Human = input("  Comparison of questions with human vs llm required? y/n: ")

            if LLM_Human == 'y':
                for t in cols:
                    Human_data = []
                    LLM_data_with_human = []
                    LLM_data_without_human = []
                    plot_data2 = []
                    for i in range(1, max_num):
                        print(t, i)
                        col1 = "P"  # Human
                        col2 = "Q"  # LLM
                        # locate table results/Extract googlesheets in the form of pandas data (limit on retrieving data)
                        _, Human_plot_data = extract_info(spreadsheet_id, t + "!",
                                                          str(i), col1, service)
                        print(i, Human_plot_data[0][0])
                        Human_data.append(float(Human_plot_data[0][0]))

                        _, LLM_plot_data_without = extract_info(spreadsheet_id, t + "!",
                                                                str(i), col2, service)
                        LLM_data_without_human.append(float(LLM_plot_data_without[0][0]))

                        if human_input_req == "y":
                            _, LLM_plot_data_with = extract_info(spreadsheet_id, updated_sheet_name + t + "!",
                                                                 str(i), col2, service)
                            LLM_data_with_human.append(float(LLM_plot_data_with[0][0]))

                        # due to limit of data read for every 60s, a delay is placed here after every 5 datapoints => 15 data points in total
                        if i % 5 == 0:
                            print("pause", Human_data)
                            time.sleep(60)

                    plot_data2.append(Human_data)

                    plot_data2.append(LLM_data_without_human)

                    if len(LLM_data_with_human) >= 1:
                        plot_data2.append(LLM_data_with_human)
                        fig_subtitle = "Human vs LLM word count with and without human examples " + t
                        plot_label = "word count"
                        fig_name = "Human_vs_LLM_" + t + ".png"
                        plot_data2 = pd.DataFrame(plot_data2).transpose()
                        plot_data2.columns = ["Human", "LLM_without_human", "LLM_with_human"]
                    else:
                        fig_subtitle = "Human vs LLM word count" + t
                        plot_label = "word count"
                        fig_name = "Human_vs_LLM_" + t + ".png"
                        plot_data2 = pd.DataFrame(plot_data2).transpose()
                        plot_data2.columns = ["Human", "LLM"]

                    print(plot_data2)
                    time.sleep(60)

                    bell_chart(plot_data2, plot_label, fig_name, fig_subtitle)

        rep = int(question_number) + 1
        print('rep', rep)
        # repeat == "y"
        repeat = input("Would you like to go again? y/n: ")


main()
