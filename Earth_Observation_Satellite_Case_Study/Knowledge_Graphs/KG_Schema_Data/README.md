# The Development of Knowledge Graphs (KGs)

This repository contains the following for creating the KG, migration of the satellite schedule to the to the KG, and code samples to read the data from the KG.

## KG_Schema_Data - TypeDB files for Schema creation and reading data

  - ## Schema_data - contains all typedb code

    - ## sched_schema_final.tql
      - This file contains the code for creating the schema for the satellite scheduling problem. It was created using TypeDB studio
    - ## schema_view.tql
      - Contains the code to view the skeleton of the schema created - **Note - Data must be migrated from the satellite schedule to the KG. Please run [code](#Python) codes below**
    - ## data_read_all.tql
      - Provides the code for reading **ALL** the data loaded to the KG. **After the data has been loaded executing [code](#Satellite_migrate_csv_updated.py) below.**
    - ## data_read.tql
      - Contains test code for extracting data from the KG after the data has been loaded.


  - ## Python - load data to typeDB
    - ## tql_merge_sched_cond.py
      This file uses a sample satellite schedule data from Results Day 3 and modifies it the format required for the KG. It also uses:
      - ### Map_image_coord.py 
      Extracts all the satellite coordinates.
      
    - ## Satellite_migrate_csv_updated.py
      - This file contains the algorithm to populate the KG with the scheduled data using [tql_merge_sched_cond.py](#tql_merge_sched_cond.py) and may be expanded to different days.

Following the creation and population of the KG, The query creation and answering using LLMs can be found in the [NLP_applied](https://github.com/strath-ace-labs/smart-xai/tree/main/Knowledge_Graphs/Satellite_example/NLP_applied) repository.
