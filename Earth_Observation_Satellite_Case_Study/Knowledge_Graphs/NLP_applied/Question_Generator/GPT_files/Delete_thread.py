# ------------------Copyright (C) 2023 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Used for deleting threads from the api assistant
# ===========================================================================================================

from GPT_connector import GPT_connector
from openai import OpenAI

OPENAI_API_KEY = GPT_connector()

client = OpenAI(api_key = OPENAI_API_KEY)


thread_id = "<Enter thread id here>"
# assistant_id = "asst_XoDtNtJumpLY2HcWlXWCXJk7"
# run_id="run_NGp0iv3CgHzcAgpDU8NqrLwa"

response = client.beta.threads.delete(thread_id)
print(response)