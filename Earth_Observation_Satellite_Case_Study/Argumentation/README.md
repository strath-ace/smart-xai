# Smart-XAI
Strathclyde Mechanical and Aerospace Research tools for Explainable Artificial Intelligence (XAI)

In support of XAI, it was discovered argumentation is a technique used to show where conflicts may occur within the decision making of a system. 
An approach currently applied to an EO satellite schedule is Abstract Argumentation (AA).

# Table Of Contents
- [Abstract](#Abstract)
- [Abstract Argumentation](#Abstract-Argumentation)
  - [Single Exchange Property (SEP)](#Single-Exchange-Property-(SEP))
  - [Pairwise Exchange Property (PEP)](#Pairwise-Exchange-Property-(PEP))

## Abstract
Satellite schedules are derived from satellite mission objectives, which are mostly managed manually from the
ground. This increases the need to develop autonomous on-board
scheduling capabilities and reduce the requirement for manual
management of satellite schedules. Additionally, this allows the
unlocking of more capabilities on-board for decision-making,
leading to an optimal campaign. However, there remain trust
issues in decisions made by Artificial Intelligence (AI) systems,
especially in risk-averse environments, such as satellite operations. Thus, an explanation layer is required to assist operators
in understanding decisions made, or planned, autonomously onboard. To this aim, a satellite scheduling problem is formulated,
utilizing real world data, where the total number of actions
are maximised based on the environmental constraints that
limit observation and down-link capabilities. The formulated
optimisation problem is solved with a Constraint Programming
(CP) method. Later, the mathematical derivation for an Abstract
Argumentation Framework (AAF) for the test case is provided.
This is proposed as the solution to provide an explanation layer
to the autonomous decision-making system. The effectiveness
of the defined AAF layer is proven on the daily schedule of
an Earth Observation (EO) mission, monitoring land surfaces,
demonstrating greater capabilities and flexibility, for a human
operator to inspect the machine provided solution.

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

- [Single Exchange Property (SEP)](#Single-Exchange-Property-(SEP))
- [Pairwise Exchange Property (PEP)](#Pairwise-Exchange-Property-(PEP))

### Single Exchange Property (SEP)

SEP is a technique used to see the effects of a schedule if an action was replaced with another.
SEP in this application, the concept was applied to a satellite schedule derived by a CP solver. 


### Pairwise Exchange Property (PEP)

PEP in this case is the swapping of any two actions throughout a schedule to observe the effects on a schedule. 