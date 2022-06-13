# smart-xai

Strathclyde Mechanical and Aerospace Research tools for Explainable Artificial Intelligence (XAI)

## Available Repositories
* [Earth Observation Case study](#Earth-Observation-Case-study)


## Earth Observation Case study

This Repository contains the code for a simple manual schedule, an updated schedule using Google-OR-Tools using the 
initially created schedule, thus in combination generating a heuristic OPTIMAL schedule. In addition,
Abstract Argumentation (AA) was applied to the schedule that is contained within.

Within this project there are 3 main sub repositories.
* [Environment](#Environment)
* [Offline schedule](#Offline-schedule)
* [Argumentation](#Argumentation)
  * [Abstract Argumentation](#Abstract-Argumentation)

### Environment
This file contains the coordinates of the satellite and the code used to determine day, 
night and land exposure.


### Offline schedule
This folder contains the code used to generate an offline schedule for heuristic with a suggested input 
from the end user.

### Argumentation
This file currently contains:

#### Abstract Argumentation
This contains 2 different types of techniques that may be used:
* SEP - Singular Exchange Property.
* PEP - Pairwise exchange properties


