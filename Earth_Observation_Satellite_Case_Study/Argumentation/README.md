# smart-xai
Strathclyde Mechanical and Aerospace Research tools for Explainable Artificial Intelligence (XAI)

In support of XAI, it was discovered argumentation is a technique used to show where conflicts may occur within the decision making of a system. 
An approach currently applied to an EO satellite schedule is Abstract Argumentation (AA).

## Abstract Argumentation (AA)
AA s a technique used to provide information, highlighting where conflicts of elements may occur in a system. 
This project contains the AA methods used to support with providing explanations to the End User of an EO satellite schedule.
The satellite schedule has 3 main actions and a fourth created when no other actions have occurred. 
Each of these actions as described in [EO case study](././README.md#Earth-Observation-Case-study).

The four actions are:
1. **Taking of images** - given a label '0' and 'a1' throughout the codes.
2. **Processing** of the taken image - given the label '1' and 'a2' throughout the codes.
3. **Down-linking** of the taken and processed image - given the label '2' and 'a3' throughout the codes.
4. **Idle time** - created when no other actions could be executed. This was given the label '-1' and 'a4' through the codes.


Within AA, 2 techniques were investigated.

- [Single Exchange Property(SEP)](#Single-Exchange-Property(SEP))
- [Pairwise Exchange Property (PEP)](#Pairwise-Exchange-Property-(PEP))

### Single Exchange Property(SEP)

SEP is a technique used to see the effects of a schedule if an action was replaced with another.
SEP in this application, the concept was applied to a satellite schedule derived by a CP solver. 


### Pairwise Exchange Property (PEP)

PEP in this case is the swapping of any two actions throughout a schedule to observe the effects on a schedule. 