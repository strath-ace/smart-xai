# Knowledge Graph (KG) case study for a simple satellite schedule
This project explores the application using Knowledge Graphs (KGs) and Large Language Models (LLMs) in supporting eXplainable Artificial Intelligence (XAI) for a simple Earth Observation Satellite Case Study and can be found [here](https://github.com/strath-ace-labs/smart-xai/tree/main/Earth_Observation_Satellite_Case_Study). 

Please use the following citation to reference this work. Pending publication

```

@article{PowellJAIS2025,
author = {Powell, Cheyenne and Riccardi, Annalisa},
title = {Question Answering over Knowledge Graphs for Explainable Satellite Scheduling},
journal = {Journal of Aerospace Information Systems},
volume = {0},
number = {0},
pages = {1-41},
year = {2025},
}
```


## Definition of a Knowledge Graph (KG)
A KG is a graphically structured representation of information that are in the form of entities, relationships and attributes. A KG enable data to be stored allowing querying, reasoning and answering over complex and interrelated data nabling advanced analytics and insights.
In this project Vaticle TypeDB is used.

## Definition of the Satellite Scheduling Problem
The satellite schedule was created using Google-OR-Tools using the coordinates of Satellite over a period 
of 6 months, between December 2020 and May 2021.

The objective of this schedule was to capture images of land only when it is illuminated by sunlight and to downlink data whenever the satellite has access to a ground station, which can occur in either sunlight or shade.

To downlink data, the satellite first processes the captured images. Image processing can take place at any time. However, while processing images, the satellite retains the original files until the data has been successfully downlinked. This precaution ensures that, in the event of data corruption during processing, the original file remains available for reprocessing.

The number of images that can be processed and downlinked is constrained by the satellite’s hardware limitations. Consequently, depending on the onboard processing capabilities, it may require multiple processing cycles to fully process an image and several downlinking attempts to transmit the processed data for a single image.

## Project Aim

The purpose of this project is to investigate the use of KGs (using [TypeDB](https://typedb.com/docs/home/)) in representing the Satellite Schedule.
Additionally, investigating the capabilities of LLMs in creating queries, code to extract information from the KG based on the query, and answering the ueries using the solution provided from the executed code.

Therefore
It contains the KG schema used for the simple satellite scheduling problem and includes Natural Language Processing (NLP) techniques to generate the following:
   1. **Queries** - Created by the LLM to ask questions about the schedule.
   2. **Knowledge Graph code** - created by the LLM to create code based on the queries asked.
   3. **Data extraction and Explanation Generation** - based on the results by the code followed by the interpretation of the data using the queries, constraints and/or example answers provided.
   



Located in this folder are 2 repositories:


### Knowledge_Graphs
Contains the algorithms required to create a KG schema, population the KG and reading data from the KG.
### NLP_applied 
An LLM GPT-4 was used in this scenario to create the queries, code and generate explanations based on the data with constraints


 