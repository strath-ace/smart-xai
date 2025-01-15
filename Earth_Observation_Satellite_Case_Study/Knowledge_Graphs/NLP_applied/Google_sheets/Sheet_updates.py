# ------------------Copyright (C) 2024 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Used to extract, update and append data  in spreadsheet (google sheet)
# ===========================================================================================================

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import time as t

def get_values(spreadsheet_id, range_name, creds):


  print(range_name)
  # pylint: disable=maybe-no-member
  # pylint: disable=maybe-no-member
  try:
      service = build("sheets", "v4", credentials=creds)
      # t.sleep(5)
      result = (
          service.spreadsheets()
          .values()
          .get(spreadsheetId=spreadsheet_id, range=range_name)
          .execute()
      )
      rows = result.get("values", [])

      if len(rows) == 0:
          print(f"{len(rows)} rows retrieved", rows)
          return len(rows), 0  # result
      else:
          print(f"{len(rows)} rows retrieved", rows, "\n", rows[len(rows) - 1])
          return len(rows), rows[len(rows) - 1]  # result
  except HttpError as error:
      print(f"An error occurred: {error}")
      return error


def update_values(spreadsheet_id, range_name, value_input_option, _values, data_generated, creds):
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)
        values = [
            [data_generated
             # Cell values ...
             ],
            # Additional rows ...
        ]
        body = {"values": values}
        print(body)
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                # range=range_name,
                valueInputOption=value_input_option,
                body=body,

            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def append_values(spreadsheet_id, range_name, value_input_option, _values, answer, creds):

  try:
      service = build("sheets", "v4", credentials=creds)
      values = answer

      body = {"values": values}
      print(body)
      result = (
          service.spreadsheets()
          .values()
          .append(
              spreadsheetId=spreadsheet_id,
              range= range_name,
              # range=range_name,
              valueInputOption=value_input_option,
              body=body,

          )
          .execute()
      )
      print(f"{result.get('updatedCells')} cells updated.")
      return result
  except HttpError as error:
      print(f"An error occurred: {error}")
      return error

if __name__ == "__main__":
    spreadsheet_id = '<enter here>'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    # Pass: spreadsheet_id, and range_name
    # question_generated = "Question here \nAnother test"
    range = "Swap_actions!"
    data_len, res = get_values(spreadsheet_id, range + "C1:C200", creds)
    # update_values(spreadsheetID, "B"+ str(data_len+1),
    #     "USER_ENTERED",
    #     ["A"], question_generated
    # )
    print(data_len, res)
