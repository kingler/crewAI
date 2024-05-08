
---
title: crewAI Tasks
description: Detailed guide on managing and creating tasks within the crewAI framework with BDI architecture.
---

## Overview of a Task
!!! note "What is a Task?"
    In the crewAI framework with BDI architecture, tasks are specific assignments completed by agents. They are linked to the agent's goals and plans, guiding the agent's behavior and decision-making.

## Task Attributes

| Attribute                   | Description                                                                                 |
| :-------------------------- | :------------------------------------------------------------------------------------------ |
| **Associated Goal**         | The goal that the task is associated with, guiding the agent's behavior.                    |
| **Associated Plan**         | The plan that the task is associated with, specifying the actions to achieve the goal.      |
| **Description**             | A clear, concise statement of what the task entails.                                        |
| **Agent**                   | The agent responsible for the task, assigned either directly or by the crew's process.      |
| **Expected Output**         | A detailed description of what the task's completion looks like.                            |
| **Tools** *(optional)*      | The functions or capabilities the agent can utilize to perform the task.                    |
| **Context**  *(optional)*   | Specifies tasks whose outputs are used as context for this task.                            |

## Creating a Task

Creating a task involves defining its scope, responsible agent, associated goal and plan, and any additional attributes:

```python
from crewai import Task, Goal, Plan

task = Task(
    description='Find and summarize the latest news on AI',
    agent=research_agent,
    associated_goal=Goal(name='Stay updated on AI trends', description='Keep track of the latest AI developments', priority=2),
    associated_plan=Plan(name='Research AI news', description='Search and summarize recent AI news articles', associated_goal='Stay updated on AI trends')
)
