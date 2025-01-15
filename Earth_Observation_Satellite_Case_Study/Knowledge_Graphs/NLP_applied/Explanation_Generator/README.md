# Explanation Generator

This folder contains all the required functions for executing the LLMs with prompts containing the constraints, questions, and tabular results from the KG to create explanations to the end user. 

The main function locally to this folder is:

- ## extract_google_sheets.py
  Retrieves the data from Google sheets through the API for the LLM

- ## NLP_explanation_generator.py
  This function is responsible for extracting the results from the KG in tabular form, combining it with the constraints and creating explanations using the LLM

- ## GPT_files 
  - This file contains the prompts supplied to the LLM