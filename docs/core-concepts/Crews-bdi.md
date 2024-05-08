---
title: crewAI Crews with BDI Architecture
description: Understanding and utilizing crews in the crewAI framework with BDI architecture.
---

## What is a Crew?
A crew in crewAI with BDI architecture represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow, taking into account the agents' beliefs, desires, and intentions.

## Crew Attributes

| Attribute                   | Description                                                                                 |
| :-------------------------- | :------------------------------------------------------------------------------------------ |
| **Tasks**                   | A list of tasks assigned to the crew, linked to the agents' goals and plans.                |
| **Agents**                  | A list of agents that are part of the crew, each with their own beliefs, desires, and intentions. |
| **Process** *(optional)*    | The process flow (e.g., sequential, hierarchical) the crew follows.                         |
| **Verbose** *(optional)*    | The verbosity level for logging during execution.                                          |
| **Config** *(optional)*     | Optional configuration settings for the crew, including agent beliefs, desires, and intentions. |

## Creating a Crew

When assembling a crew with BDI agents, you combine agents with complementary roles, goals, and plans, assign tasks, and select a process that dictates their execution order and interaction.

### Example: Assembling a Crew

```python
from crewai import Crew, Agent, Task, Process, Goal, Plan

# Define agents with specific roles, goals, and plans
researcher = Agent(
    role='Senior Research Analyst',
    goal='Discover innovative AI technologies',
    beliefs={'expertise': 'AI research', 'tools': ['Google Scholar', 'IEEE Xplore']},
    desires=[Goal(name='Identify AI trends', description='Discover emerging AI technologies', priority=1)],
    intentions=[Plan(name='Conduct literature review', description='Review recent AI publications', associated_goal='Identify AI trends')]
)

writer = Agent(
    role='Content Writer',
    goal='Write engaging articles on AI discoveries',
    beliefs={'expertise': 'technical writing', 'tools': ['Markdown', 'Grammarly']},
    desires=[Goal(name='Educate readers about AI', description='Create informative AI articles', priority=2)],
    intentions=[Plan(name='Draft AI article', description='Write an article on the latest AI trends', associated_goal='Educate readers about AI')]
)

# Create tasks for the agents
research_task = Task(
    description='Identify breakthrough AI technologies',
    agent=researcher,
    associated_goal=researcher.desires[0],
    associated_plan=researcher.intentions[0]
)
write_article_task = Task(
    description='Draft an article on the latest AI technologies',
    agent=writer,
    associated_goal=writer.desires[0],
    associated_plan=writer.intentions[0]
)

# Assemble the crew with a sequential process
my_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_article_task],
    process=Process.sequential
)

#
## 1. Introduce a Knowledge Base (KB) Component

Create a new component or module dedicated to representing and managing the knowledge base for the agents and the overall agency.

```python
class KnowledgeBase:
    def __init__(self):
        self.ontology = None
        self.rules = []
        self.facts = []

    def load_ontology(self, ontology_file):
        # Load and parse the ontology file
        self.ontology = parse_ontology(ontology_file)

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.append(fact)

    def query(self, query):
        # Implement query processing logic
        ...

    def infer(self):
        # Implement inference logic
        ...
```

## 2. Integrate Ontology Representation

Incorporate an ontology representation format, such as OWL (Web Ontology Language) or RDF (Resource Description Framework), to define the domain concepts, properties, and relationships.

You can use existing libraries like `owlready2` or `rdflib` to load and manipulate ontologies in Python.

```python
from owlready2 import get_ontology

def parse_ontology(ontology_file):
    return get_ontology(ontology_file).load()
```

## 3. Extend the Agent Class

Modify the `Agent` class to include a reference to the `KnowledgeBase` and methods for interacting with it.

```python
class Agent(BaseModel):
    ...
    knowledge_base: KnowledgeBase

    def __init__(self, ..., knowledge_base: KnowledgeBase):
        ...
        self.knowledge_base = knowledge_base

    def query_knowledge(self, query):
        return self.knowledge_base.query(query)

    def infer_knowledge(self):
        self.knowledge_base.infer()
        # Update beliefs based on inferred knowledge
        ...
```

## 4. Populate the Knowledge Base

Implement mechanisms to populate the knowledge base with domain-specific knowledge, rules, and facts. This can be done manually or by integrating with external knowledge sources or ontologies.

```python
# Load the domain ontology
agent.knowledge_base.load_ontology("domain.owl")

# Add domain-specific rules
agent.knowledge_base.add_rule(Rule(...))

# Add initial facts
agent.knowledge_base.add_fact(Fact(...))
```

## 5. Integrate Knowledge into Decision-Making and Task Execution

Modify the agent's decision-making and task execution processes to leverage the knowledge base for reasoning and inference.

```python
class Agent(BaseModel):
    ...
    def make_decision(self, options):
        # Query and infer over the knowledge base
        self.infer_knowledge()

        # Evaluate options based on beliefs, desires, intentions, and knowledge
        ...

    def execute_task(self, task):
        # Query the knowledge base for relevant information
        task_knowledge = self.query_knowledge(task.description)

        # Execute the task using the retrieved knowledge
        ...
```

## 6. Enable Knowledge Sharing and Collaboration

Implement mechanisms for agents to share their knowledge bases or specific knowledge components with other agents or the overall agency.

```python
class Agent(BaseModel):
    ...
    def share_knowledge(self, other_agent):
        # Share the entire knowledge base
        other_agent.knowledge_base = copy.deepcopy(self.knowledge_base)

        # Or share specific components
        other_agent.knowledge_base.rules.extend(self.knowledge_base.rules)
        ...
```

## 7. Integrate with the Crew and Process Management

Modify the `Crew` class and the process management components to incorporate the knowledge-based reasoning and decision-making capabilities of the agents.

```python
class Crew(BaseModel):
    ...
    def _run_goal_driven_process(self):
        # Allow agents to reason over their knowledge bases
        for agent in self.agents:
            agent.infer_knowledge()

        # Assign tasks based on agents' beliefs, desires, intentions, and knowledge
        ...
```

By following these development steps, you can extend the proposed MAS framework to incorporate knowledge representation and reasoning capabilities for individual domain role agents and the overall agency. This will enable the agents to leverage domain-specific knowledge, rules, and facts in their decision-making and task execution processes, as well as facilitate knowledge sharing and collaboration among agents and the agency.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/496050/e0a9f86c-b0d3-49b9-b9af-c74dae889b9b/bdi_framework.md
[2] https://core.ac.uk/download/pdf/148670021.pdf
[3] https://core.ac.uk/download/pdf/153409600.pdf
[4] https://www.mdpi.com/1996-1073/12/16/3200
[5] https://shop.harvard.com/book/9783031529801
[6] https://stackoverflow.com/questions/12423372/python-multi-agent-simulation-packages
[7] https://physics.mff.cuni.cz/wds/proc/pdf10/WDS10_103_i1_Kazik.pdf
[8] https://www.fi.muni.cz/usr/sojka/download/raslan2008/3.pdf
[9] https://academic.oup.com/bib/article/22/4/bbaa199/5922325
[10] https://towardsdatascience.com/multi-agent-deep-reinforcement-learning-in-15-lines-of-code-using-pettingzoo-e0b963c0820b
[11] https://stackoverflow.com/questions/6037996/multi-agent-system-application-idea
[12] https://www.sice.jp/siceac/sice2021/08-1.html
[13] https://github.com/topics/multi-agent-systems?l=python
[14] https://github.com/joaomdmoura/crewAI
[15] https://github.com/topics/multi-agent-systems
[16] https://boa.unimib.it/retrieve/9e2295a2-939c-40e9-8956-8d8b59b552a1/Osborne-2023-IEEEAccess-VoR.pdf
[17] https://www.youtube.com/watch?v=F9IatGEIukM
[18] https://www.toolify.ai/ai-news/introducing-crew-ai-revolutionize-your-ai-agents-with-this-autogen-alternative-2397053
[19] https://www.youtube.com/watch?v=oovLgT2oId4
[20] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11027160/
