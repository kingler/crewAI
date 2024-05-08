---
title: crewAI Agents
description: What are crewAI Agents and how to use them with BDI architecture.
---

## What is an Agent?
!!! note "What is an Agent?"
    An agent is an **autonomous unit** programmed to:
    <ul>
      <li class='leading-3'>Perform tasks</li>
      <li class='leading-3'>Make decisions</li>
      <li class='leading-3'>Communicate with other agents</li>
    </ul>
      <br/>
    In the BDI architecture, agents have beliefs, desires, and intentions that guide their behavior and decision-making. Beliefs represent the agent's knowledge about the world, desires are the agent's goals, and intentions are the plans the agent commits to in order to achieve its goals.

## Agent Attributes

| Attribute                   | Description                                                                                                                 |
| :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| **Beliefs**                 | Represents the agent's current knowledge and understanding of the world.                                                    |
| **Desires**                 | Represents the agent's long-term goals and objectives.                                                                      |
| **Intentions**              | Represents the agent's current commitments and plans to achieve its goals.                                                  |
| **Role**                    | Defines the agent's function within the crew. It determines the kind of tasks the agent is best suited for.                 |
| **Goal**                    | The individual objective that the agent aims to achieve. It guides the agent's decision-making process.                     |
| **Backstory**               | Provides context to the agent's role and goal, enriching the interaction and collaboration dynamics.                        |
| **LLM** *(optional)*        | The language model that will run the agent.                                                                                |
| **Tools** *(optional)*      | Set of capabilities or functions that the agent can use to perform tasks.                                                   |
| **Max Iter** *(optional)*   | The maximum number of iterations the agent can perform before being forced to give its best answer. Default is `25`.        |
| **Verbose** *(optional)*    | Setting this to `True` configures the internal logger to provide detailed execution logs. Default is `False`.               |
| **Allow Delegation** *(optional)* | Agents can delegate tasks or questions to one another. Default is `True`.                                                   |
| **Cache** *(optional)*      | Indicates if the agent should use a cache for tool usage. Default is `True`.                                               |

## Creating an Agent

To create an agent with the BDI architecture, initialize an instance of the `Agent` class with the desired properties, including `beliefs`, `desires`, and `intentions`:

```python
from crewai import Agent, Goal, Plan

agent = Agent(
  role='Data Analyst',
  goal='Extract actionable insights',
  backstory="...",
  beliefs={'expertise': 'data analysis', 'tools': ['Python', 'SQL']},
  desires=[Goal(name='Improve data quality', description='Ensure data accuracy and completeness', priority=1)],
  intentions=[Plan(name='Data cleaning', description='Clean and preprocess the dataset', associated_goal='Improve data quality')]
)
