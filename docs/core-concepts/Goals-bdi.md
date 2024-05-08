---
title: Goals in CrewAI with BDI Architecture
description: Understanding and defining goals for agents in the CrewAI framework with BDI architecture.
---

## What is a Goal?
In the BDI (Belief-Desire-Intention) architecture, goals represent the objectives or desired states that an agent aims to achieve. They are part of the agent's desires and guide the agent's decision-making and behavior.

## Goal Attributes

| Attribute      | Description                                                                    |
| :------------- | :----------------------------------------------------------------------------- |
| **Name**       | A descriptive name for the goal.                                              |
| **Description**| A detailed explanation of what the goal entails and why it is important.       |
| **Priority**   | The relative importance or urgency of the goal compared to other goals.        |

## Creating a Goal

To create a goal for an agent, initialize an instance of the `Goal` class with the desired attributes:

```python
from crewai import Goal

goal = Goal(
    name='Improve customer satisfaction',
    description='Implement strategies to enhance customer experience and increase satisfaction ratings',
    priority=1
)
```
Associating Goals with Agents
Goals are associated with agents through the agent's desires attribute. An agent can have multiple goals, representing its various objectives and aspirations.

```python
from crewai import Agent, Goal

agent = Agent(
    role='Customer Support Representative',
    desires=[
        Goal(name='Resolve customer issues', description='Promptly address and resolve customer concerns', priority=1),
        Goal(name='Maintain knowledge base', description='Keep the customer support knowledge base up to date', priority=2)
    ]
)
