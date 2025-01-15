# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Extracts data such as questions, code, and answers from Google sheets
# ===========================================================================================================


import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials



# Loads the pandas file from googlesheet based on the question
def locate_number_google_sheets(spreadsheet_id, range1, vals, service):
    sheet = service.spreadsheets()
    # range_name = "A1:A300"
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range1).execute()
    values = result.get("values", [])
    # locate cell position of question/number
    a = 0
    vals = int(vals)

    for i in (values):

        a = a + 1
        if str(vals) in i:
            a0 = a
        if str(vals+1) in i:
            a1 = a
        # else:
        #     a0=a1=a

    return sheet, values, a0, a1

# Extract the code or explanations based on the question number
def extract_info(spreadsheet_id, range1, question_number, column, service):
    sheet, values, a0, a1 = locate_number_google_sheets(spreadsheet_id, range1 + "A1:A3000", question_number, service)
    # Extract the code or information based on cell position
    info_result = sheet.values().get(spreadsheetId=spreadsheet_id, range= range1 + column + str(a0)).execute()
    information = info_result.get("values", [])
    return a0,information

def extract_question(spreadsheet_id, range1, question_number, service):
    sheet, values, a0, a1 = locate_number_google_sheets(spreadsheet_id, range1 + "A1:A3000", question_number, service)
    # Extract the question
    q_result = sheet.values().get(spreadsheetId=spreadsheet_id, range= range1 + "B" + str(a0)).execute()
    question = q_result.get("values", [])
    print('question',question)

    # find the range where the table is and extract all the tabulated data
    range_name2 = "C" + str(a0) + ":AA" + str(a1 - 1)
    # Use the position to extract all the answers
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range= range1 + range_name2).execute()
    values = result.get("values", [])
    df = pd.DataFrame(values)
    # return the cell number for the question, the question in the new sheet and the dataframe for the response
    return a0, question, df



if __name__ == "__main__":
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    service = build("sheets", "v4", credentials=creds)
    spreadsheet_id ='1RVz6XBCH3745lXX9NYMM21G29DwEwHoD8t-zxDA7fAg'
    # spreadsheet_id = "<Spreadsheet here>"
    table_worksheet = "Single_Substitution" + "_Table_results!"
    question_number = 20
    # cell_num, question, tabulated_kg_results = extract_question(spreadsheet_id, table_worksheet, str(question_number))
    cell_num, question, tabulated_kg_results = extract_question(spreadsheet_id, table_worksheet,
                                                                str(question_number), service)



    print(cell_num, question, tabulated_kg_results)