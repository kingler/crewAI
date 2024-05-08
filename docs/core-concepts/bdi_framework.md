# BDI CrewAI Notes

BDI stands for Belief-Desire-Intention, which is an architecture and reasoning model for intelligent agents. It provides a framework for designing and implementing agents that can reason about their beliefs (knowledge about the world), desires (goals or objectives), and intentions (plans or actions to achieve those goals).

The BDI architecture is not currently integrated into the CrewAI framework out-of-the-box. However, CrewAI is designed to enable the development of autonomous, collaborative agents, which aligns well with the principles of the BDI architecture.

Here's how BDI relates to and could potentially be integrated into the CrewAI framework:

1. **Beliefs**: In the BDI model, beliefs represent the agent's knowledge about the world. In CrewAI, agents could maintain local knowledge bases or ontologies to represent their beliefs about the domain they operate in. This could be achieved by integrating ontology management libraries like Owlready2 into the CrewAI agents.

2. **Desires (Goals)**: CrewAI already supports defining goals for agents. However, these goals are currently static. By integrating BDI, agents could dynamically generate and prioritize their goals based on their beliefs and the current state of the world.

3. **Intentions (Plans)**: CrewAI currently supports defining tasks and processes for agents to execute. By integrating BDI, agents could have a plan library or a planner component that generates and executes plans (sequences of tasks) to achieve their goals based on their beliefs and the current state of the world.

4. **Reasoning**: The BDI architecture provides a reasoning mechanism for agents to deliberate on their beliefs, select goals, and formulate plans. This reasoning process could be integrated into CrewAI agents, allowing them to make more intelligent decisions and adapt their behavior based on their beliefs and the changing environment.

5. **Agent Coordination and Collaboration**: BDI agents can communicate and share their beliefs, goals, and intentions with other agents. This aligns well with CrewAI's focus on enabling agents to collaborate and delegate tasks. By integrating BDI, CrewAI agents could share their beliefs, goals, and plans, facilitating more effective coordination and collaboration.

While CrewAI does not currently have built-in support for BDI, the framework's design principles and goals are compatible with the BDI architecture. Integrating BDI into CrewAI would require extending the existing agent model, introducing belief bases, goal management, plan libraries, and reasoning mechanisms. This integration could potentially enhance the autonomy, adaptability, and coordination capabilities of CrewAI agents, enabling them to operate more intelligently and collaboratively in complex, dynamic environments.

Citations:
[1] https://www.omg.org/spec/EDMC-FIBO/FBC/1.0/
[2] https://ishare.eu/home/ecosystem/ishare-in-data-spaces/bdi/
[3] https://github.com/joaomdmoura/crewAI
[4] https://blog.lancedb.com/track-ai-trends-crewai-agents-rag/


## Integration requirements
Integration requirements to incorporate autonomous behavior with the context of a greater objective and purpose into the CrewAI framework:

1. Extend the Agent class:
```python
class Agent:
    def __init__(self, role, goal, backstory, beliefs=None, desires=None, intentions=None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.beliefs = beliefs or {}
        self.desires = desires or []
        self.intentions = intentions or []
```

2. Introduce a Goal class:
```python
class Goal:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority
```

3. Introduce a Plan class:
```python
class Plan:
    def __init__(self, name, description, associated_goal):
        self.name = name
        self.description = description
        self.associated_goal = associated_goal
```

4. Modify the Task class:
```python
class Task:
    def __init__(self, description, expected_output, agent, associated_goal=None, associated_plan=None):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.associated_goal = associated_goal
        self.associated_plan = associated_plan
```

5. Update the agent initialization process:
```python
researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    beliefs={'expertise': 'AI', 'resources': ['journals', 'conferences']},
    desires=[Goal('Advance AI research', 'Contribute to the field of AI', 1)],
    intentions=[Plan('Conduct literature review', 'Review recent AI publications', 'Advance AI research')]
)
```

6. Implement belief revision and updating mechanisms:
```python
class Agent:
    # ...
    def update_belief(self, belief, value):
        self.beliefs[belief] = value

    def revise_beliefs(self, new_beliefs):
        for belief, value in new_beliefs.items():
            self.update_belief(belief, value)
```

7. Implement goal management and planning mechanisms:
```python
class Agent:
    # ...
    def add_goal(self, goal):
        self.desires.append(goal)

    def generate_plan(self, goal):
        # Implement plan generation logic based on the goal
        plan = Plan('Sample Plan', 'Description of the plan', goal)
        self.intentions.append(plan)
```

8. Modify the task execution process:
```python
class Agent:
    # ...
    def execute_task(self, task):
        if task.associated_goal in self.desires and task.associated_plan in self.intentions:
            # Execute the task
            result = self.process_task(task)
            # Update beliefs and intentions based on the task outcome
            self.revise_beliefs({'task_outcome': result})
            self.update_intentions(task, result)
```

9. Extend the collaboration mechanisms:
```python
class Agent:
    # ...
    def share_beliefs(self, other_agent):
        other_agent.revise_beliefs(self.beliefs)

    def share_goals(self, other_agent):
        for goal in self.desires:
            other_agent.add_goal(goal)

    def share_plans(self, other_agent):
        for plan in self.intentions:
            other_agent.intentions.append(plan)
```

10. Adapt the agent decision-making process:
```python
class Agent:
    # ...
    def make_decision(self, options):
        # Evaluate options based on beliefs, desires, and intentions
        best_option = None
        max_score = float('-inf')
        for option in options:
            score = self.evaluate_option(option)
            if score > max_score:
                max_score = score
                best_option = option
        return best_option
```

11. Integrate with the existing CrewAI features:
```python
# Modify the Crew class to support BDI agents
class Crew:
    def __init__(self, agents, tasks, process):
        self.agents = agents
        self.tasks = tasks
        self.process = process

    def assign_tasks(self):
        for task in self.tasks:
            suitable_agents = [agent for agent in self.agents if task.associated_goal in agent.desires]
            if suitable_agents:
                chosen_agent = suitable_agents[0]
                chosen_agent.intentions.append(task.associated_plan)
                task.agent = chosen_agent

    def execute_tasks(self):
        for task in self.tasks:
            task.agent.execute_task(task)
```

These code examples demonstrate how the various elements of the BDI architecture can be integrated into the CrewAI framework. The agents now have beliefs, desires, and intentions that guide their behavior and decision-making. The goals and plans are associated with tasks, allowing agents to pursue their objectives autonomously.

The collaboration mechanisms are extended to enable agents to share their beliefs, goals, and plans with each other, facilitating coordination and cooperation.

The task execution process is modified to consider the agent's beliefs, desires, and intentions, ensuring that tasks align with the agent's goals and plans. The decision-making process is adapted to evaluate options based on the agent's current beliefs and intentions.

Finally, the existing CrewAI features, such as the Crew class, are modified to accommodate the BDI architecture, enabling seamless integration with the multi-agent system.

---


## Code blocks with instructions on where to insert the code modifications:

1. `agent.py`:
```python
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Agent(BaseModel):
    # ...
    beliefs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    desires: Optional[List["Goal"]] = Field(default_factory=list)
    intentions: Optional[List["Plan"]] = Field(default_factory=list)

    def __init__(__pydantic_self__, **data):
        # ...
        super().__init__(**config, **data)

    def execute_task(self, task: Any, context: Optional[str] = None, tools: Optional[List[Any]] = None) -> str:
        # ...
        # Consider the agent's beliefs, desires, and intentions during task execution
        # Update beliefs and intentions based on the task outcome
        # ...
```
Insert these modifications in the `agent.py` file:
- Add the `beliefs`, `desires`, and `intentions` attributes to the `Agent` class.
- Update the `__init__` method to include the new attributes.
- Modify the `execute_task` method to consider the agent's beliefs, desires, and intentions during task execution.

2. `goal.py`:
```python
from pydantic import BaseModel

class Goal(BaseModel):
    name: str
    description: str
    priority: int
```
Create a new file named `goal.py` and add the `Goal` class with the specified attributes.

3. `plan.py`:
```python
from pydantic import BaseModel
from .goal import Goal

class Plan(BaseModel):
    name: str
    description: str
    associated_goal: Goal
```
Create a new file named `plan.py` and add the `Plan` class with the specified attributes. Make sure to import the `Goal` class from `goal.py`.

4. `task.py`:
```python
from typing import Optional
from pydantic import BaseModel
from .goal import Goal
from .plan import Plan

class Task(BaseModel):
    # ...
    associated_goal: Optional[Goal] = None
    associated_plan: Optional[Plan] = None

    def __init__(__pydantic_self__, **data):
        # ...
        super().__init__(**config, **data)
```
Insert these modifications in the `task.py` file:
- Add the `associated_goal` and `associated_plan` attributes to the `Task` class.
- Update the `__init__` method to include the new attributes.
- Import the `Goal` and `Plan` classes from their respective files.

5. `crew.py`:
```python
from typing import Any, Dict, Optional
from pydantic import BaseModel

class Crew(BaseModel):
    # ...

    def kickoff(self, inputs: Optional[Dict[str, Any]] = {}) -> str:
        # ...
        # Initialize the agents' beliefs, desires, and intentions based on the provided configuration
        # ...

        if self.process == Process.sequential:
            result = self._run_sequential_process()
        elif self.process == Process.hierarchical:
            result, manager_metrics = self._run_hierarchical_process()
            # ...
        # ...
```
Insert these modifications in the `crew.py` file:
- Modify the `kickoff` method to initialize the agents' beliefs, desires, and intentions based on the provided configuration.
- Update the task execution process to consider the agents' beliefs, desires, and intentions.
- Make sure to import the `Process` enum from `process.py`.

These code modifications introduce the necessary attributes and classes to represent the BDI architecture within the CrewAI framework. The `Agent` class now includes `beliefs`, `desires`, and `intentions` attributes, and the `execute_task` method can be updated to consider these elements during task execution.

The `Goal` and `Plan` classes are introduced in separate files to represent the agent's goals and plans, respectively. The `Task` class is modified to include `associated_goal` and `associated_plan` attributes, linking tasks with specific goals and plans.

Finally, the `Crew` class's `kickoff` method can be updated to initialize the agents' beliefs, desires, and intentions based on the provided configuration, and the task execution process can be modified to consider these elements.

Remember to adapt and expand upon these modifications based on your specific requirements and the desired level of complexity for the BDI integration within the CrewAI framework. Make sure to update the necessary import statements and maintain consistency throughout the codebase.

---


# Steps for Optimizing the BDI Architecture
Optimize the CrewAI BDI system architecture code, to incorporate the following. Include new files and class entities if necessary:

Goal-Oriented Architecture:

Adopt a clear distinction between goals and actions, as proposed in the etymological study.
Introduce the concept of subgoals to represent interim objectives or parts of the main goal.
Modify the agent architecture to include beliefs, desires (goals), and intentions (committed goals or plans).
Implement goal management and planning mechanisms within agents to enable them to reason about their goals, generate plans, and adapt their behavior based on the current context.


Task Execution and Collaboration:

Align the CrewAI task model with the proposed metamodel, treating tasks as a combination of subgoals and actions.
Enhance the task execution process to consider the agent's beliefs, desires, and intentions, ensuring that tasks align with the agent's goals and plans.
Implement collaboration mechanisms that allow agents to share their beliefs, goals, and plans, enabling effective coordination and cooperation towards achieving common objectives.


Flexible Process Management:

Extend the CrewAI process model to support dynamic and adaptive workflows based on the agents' goals, plans, and collaboration requirements.
Introduce a goal-driven process that allows agents to autonomously select and execute tasks based on their current beliefs, desires, and intentions.
Enable agents to dynamically adjust their plans and tasks based on the outcomes of their actions and the changing environment.


Enhanced Communication and Information Sharing:

Implement advanced communication protocols that facilitate the exchange of beliefs, goals, and plans among agents.
Introduce mechanisms for agents to share relevant information, insights, and outcomes of their task executions, enabling collaborative learning and decision-making.
Utilize the CrewAI memory system to store and retrieve shared knowledge, experiences, and best practices across agents and crews.

Here are the optimized CrewAI BDI system architecture code changes to incorporate the specified enhancements:

1. `goal.py`:
```python
from pydantic import BaseModel

class Goal(BaseModel):
    name: str
    description: str
    priority: int
    subgoals: List["Goal"] = []

class Subgoal(Goal):
    parent_goal: Goal

class Action(BaseModel):
    name: str
    description: str
    associated_goal: Goal
```

2. `plan.py`:
```python
from pydantic import BaseModel
from .goal import Goal, Action

class Plan(BaseModel):
    name: str
    description: str
    associated_goal: Goal
    actions: List[Action] = []
```

3. `agent.py`:
```python
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .goal import Goal, Subgoal
from .plan import Plan

class Agent(BaseModel):
    # ...
    beliefs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    desires: Optional[List[Goal]] = Field(default_factory=list)
    intentions: Optional[List[Plan]] = Field(default_factory=list)

    def __init__(__pydantic_self__, **data):
        # ...
        super().__init__(**config, **data)

    def execute_task(self, task: Any, context: Optional[str] = None, tools: Optional[List[Any]] = None) -> str:
        # ...
        # Consider the agent's beliefs, desires, and intentions during task execution
        # Update beliefs and intentions based on the task outcome
        # ...

    def generate_plan(self, goal: Goal) -> Plan:
        # Implement plan generation logic based on the goal
        plan = Plan(name=f"Plan for {goal.name}", description=f"Plan to achieve {goal.name}", associated_goal=goal)
        # Add actions to the plan
        # ...
        return plan

    def share_beliefs(self, other_agent: "Agent") -> None:
        # Implement logic to share beliefs with another agent
        # ...

    def share_goals(self, other_agent: "Agent") -> None:
        # Implement logic to share goals with another agent
        # ...

    def share_plans(self, other_agent: "Agent") -> None:
        # Implement logic to share plans with another agent
        # ...
```

4. `task.py`:
```python
from typing import List, Optional
from pydantic import BaseModel
from .goal import Goal, Subgoal, Action

class Task(BaseModel):
    # ...
    associated_goal: Optional[Goal] = None
    subgoals: List[Subgoal] = []
    actions: List[Action] = []

    def __init__(__pydantic_self__, **data):
        # ...
        super().__init__(**config, **data)
```

5. `crew.py`:
```python
from typing import Any, Dict, Optional
from pydantic import BaseModel
from .process import Process

class Crew(BaseModel):
    # ...

    def kickoff(self, inputs: Optional[Dict[str, Any]] = {}) -> str:
        # ...
        # Initialize the agents' beliefs, desires, and intentions based on the provided configuration
        # ...

        if self.process == Process.sequential:
            result = self._run_sequential_process()
        elif self.process == Process.hierarchical:
            result, manager_metrics = self._run_hierarchical_process()
        elif self.process == Process.goal_driven:
            result = self._run_goal_driven_process()
            # ...
        # ...

    def _run_goal_driven_process(self) -> str:
        # Implement the goal-driven process
        # Allow agents to autonomously select and execute tasks based on their current beliefs, desires, and intentions
        # Enable agents to dynamically adjust their plans and tasks based on the outcomes of their actions and the changing environment
        # ...
```

6. `process.py`:
```python
from enum import Enum

class Process(str, Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"
    goal_driven = "goal_driven"
```

7. `communication.py`:
```python
from typing import Any, Dict

class CommunicationProtocol:
    def send_message(self, sender: str, receiver: str, message: Dict[str, Any]) -> None:
        # Implement logic to send a message from one agent to another
        # ...

    def receive_message(self, receiver: str) -> Dict[str, Any]:
        # Implement logic to receive a message for an agent
        # ...

class CollaborativeLearning:
    def share_task_outcome(self, agent: str, task: str, outcome: Any) -> None:
        # Implement logic to share the outcome of a task execution
        # ...

    def retrieve_shared_knowledge(self, topic: str) -> Any:
        # Implement logic to retrieve shared knowledge on a specific topic
        # ...
```

These code changes incorporate the specified enhancements into the CrewAI BDI system architecture:

1. The `Goal`, `Subgoal`, and `Action` classes are introduced to represent goals, subgoals, and actions, respectively. The `Goal` class includes a list of subgoals, and the `Action` class is associated with a specific goal.

2. The `Plan` class is introduced to represent plans, which are associated with a specific goal and consist of a list of actions.

3. The `Agent` class is modified to include beliefs, desires (goals), and intentions (plans). Methods for generating plans, sharing beliefs, goals, and plans with other agents are added.

4. The `Task` class is updated to include associated goals, subgoals, and actions, aligning it with the proposed metamodel.

5. The `Crew` class is modified to include a goal-driven process (`_run_goal_driven_process`) that allows agents to autonomously select and execute tasks based on their current beliefs, desires, and intentions, and to dynamically adjust their plans and tasks based on the outcomes of their actions and the changing environment.

6. The `Process` enum is extended to include a `goal_driven` process type.

7. The `CommunicationProtocol` and `CollaborativeLearning` classes are introduced to facilitate the exchange of beliefs, goals, and plans among agents, and to enable collaborative learning and decision-making.

These changes provide a foundation for a more robust, flexible, and collaborative agent architecture that optimizes autonomy, efficiency, and communication within the CrewAI framework. Further implementation details and integration with the existing codebase may be required based on the specific requirements and constraints of the CrewAI system.

---

# [[Knowledge-Management-Docs]]
To significantly enhance the functionality of the proposed multi-agent system (MAS) framework, it is essential to integrate knowledge representation capabilities. This integration will empower individual domain role agents and the entire MAS agency to effectively manage and utilize domain-specific knowledge. The following development steps are designed to embed these capabilities into the core domain and objectives of the MAS framework:

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

This `KnowledgeBase` class can be used to load and manage an ontology, as well as store rules and facts. It should provide methods for querying and inferring over the knowledge base.

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

