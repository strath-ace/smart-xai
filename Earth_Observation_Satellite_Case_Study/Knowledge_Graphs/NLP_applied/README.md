

# The application of Knowledge Graphs used with Satellite Scheduling

This repository contains all the codes for the project. Starting with the main file:

- ### Main.py
  - This file calls all the functions required in generating the queries, codes and answers dataset. It is fully automated with pause clauses asking to continue and will run for *n* times, based on the number of questions you would like to generate.
- ## GPT_connector.py
  - This file connects to OpenAI API for GPT after it has been set up on local PC. Read OpenAI developer platform [here](https://platform.openai.com/docs/overview) for instructions.


- These files use Google Sheets to store results - therefore token.json file will be required. Please see file [here](https://developers.google.com/sheets/api/quickstart/python) (for python users) on how to create credentials to connecting to google sheets.
- Node.js, Java, and others on how to use Google API are also available



## The following repositories contained are:

- ### [Google_sheets](#Google_sheets)
- ### [Question_Generator](#Question_Generator)
- ### [Code_Generator](#Code_Generator)
- ### [Explanation_Generator](#Explanation_Generator)
- ### [Scoring](#Scoring)



- ## Google_sheets
    Responsible for updating data within the sheets from the LLM and KG results. Additionally, contains the following functions.
    - ##### Code_updates.py
    -  #### sheet_code_generator.py

- ## Question_Generator
This folder contains where the questions are generated using OpenAI's Assistant API, this enables a dialog to occur if the question isn't appropriate for the problem, establishing a human in the loop.
Within this file, is separated into 2 sub folders, these are:

- #### GPT_files
  - #### Contains all the codes and prompt files for creating questions
- #### Google_sheets_test_cases
  - ##### Contains test files that can be used for practice purposes


- ## Code Generation
This folder is responsible for using LLM through OpenAI API with prompt files to create the code required to execute the KG as well as codes responsible for connecting to Google sheets through the API.
The following files and functions are within this repository are:

  -  ### GPT_files
     Contains all the prompt files and functions for creating the executable code
      - #### Prompt_files folder
      - #### Code_generator.py
      - #### GPT_connector.py
  
  Last, the local code within this repository is:
  - ### TypeDB_executor.py
       Contains the main python code for executing the typeDB code for the KG and generating results

- ## Explanation_Generator
This folder contains the prompt files for creating the explanations and the respected local files:
  - ### NLP_explanation_generator.py
  - ### extract_google_sheets.py
  - ### GPT_connector.py
  - ### GPT_files
       Contains all the prompt files and functions for creating the executable code
      - #### Prompt_files folder

- ## Scoring
This folder contains the functions responsible for assessing the LLMs for Cosine Similarity and BertScore response and generating the graphs.

To calculate the Bert and Cosine:

  - ### Scoring.py

 - For graphs:
   - ### violin_plot.py
   - ### bell_chart.py
   - ### line_plot.py



