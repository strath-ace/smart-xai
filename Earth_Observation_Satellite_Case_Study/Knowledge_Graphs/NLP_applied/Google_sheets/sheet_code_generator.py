# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Section 2 - Connects to Google Sheets and adds the generated code to the sheets list from GPT
# ===========================================================================================================

import sys

import string
nonalpha = string.digits + string.punctuation + string.whitespace


def sheet_code_generator(worksheet_name,spreadsheet_id, data_lenc, update_values, append_values, code_generated, question_loaded, data_results, question_number, get_values,creds,range1, col_code_store, col_iter_store):
    # Select the respective worksheet


    print("Question: ", question_loaded)

    print(code_generated)
    if data_results == '':

        # Add code Results to the next set of cells (column C) based on location of last entry
        update_values(spreadsheet_id, range1 + col_code_store + data_lenc,
                      "USER_ENTERED",
                      [col_code_store], code_generated[0]
                      ,creds)

        # Add the number of iterations (Column T)
        update_values(spreadsheet_id, range1 + col_iter_store + data_lenc,
                      "USER_ENTERED",
                      [col_iter_store], code_generated[1]
                      , creds)

    else:
        # Call the next worksheet to store tabulated data from TypeDB_executor
        range2 = worksheet_name + "_Table_results!"

        # Locate where the last data was filled in next sheet//
        # Get the data length (current position) and all data entered from the worksheet in Column C for new data entry
        data_lenc, row_data = get_values(spreadsheet_id, range2 + "C1:C2000",creds)
        data_lenc = str(data_lenc+1)

        # Question number copied to next sheet
        update_values(spreadsheet_id, range2 + "A" + data_lenc,
                      "USER_ENTERED",
                      ["A"], question_number
                      ,creds)

        # Question copied to next sheet
        update_values(spreadsheet_id, range2 + "B" + data_lenc,
                      "USER_ENTERED",
                      ["B"], question_loaded[0][0]
                      ,creds)

        # Add TypeDB Table Results to the next sheet (Table_Results) to (column C) based on location of last entry
        append_values(spreadsheet_id, range2 + "C" + data_lenc,
                      "RAW",
                      ["C"], data_results # data results must be in the form [[xx],[xx]]
                      ,creds)


        # Add the next number below the answer of the code
        question_number2 = int(question_number) + 1

        # get the new length of the sheet
        data_lenc2, row_data = get_values(spreadsheet_id, range2 + "C1:C2000",creds)

        # Put new number in the sheet
        update_values(spreadsheet_id, range2 + "A" + str(data_lenc2+1),
                      "USER_ENTERED",
                      ["A"], str(question_number2)
                      ,creds)

