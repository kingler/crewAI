from pydantic import BaseModel

class Goal(BaseModel):
    name: str
    description: str
    priority: int
    subgoals: List['Goal'] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)

    def add_subgoal(self, subgoal: 'Goal'):
      subgoal.parent_goal = self
      subgoal.priority = min(subgoal.priority, self.priority)
      subgoal.deadline = min(subgoal.deadline, self.deadline) if subgoal.deadline and self.deadline else self.deadline
      self.subgoals.append(subgoal)

    def add_action(self, task: Task, action: Action):
      if task.goal == self:
          task.actions.append(action)
          action.task = task
          task.update_status()
      else:
          raise ValueError("The provided task is not associated with this goal.")

    def create_task(self, name: str, description: str) -> Task:
      task = Task(name=name, description=description, goal=self)
      self.tasks.append(task)
      return task

    def reason_and_update(self, ontology: Ontology):
    # Retrieve relevant concepts and relationships from the ontology
      relevant_concepts = ontology.query(f"SELECT ?concept WHERE {{ ?concept rdfs:label '{self.name}' }}")
      relevant_relationships = ontology.query(f"SELECT ?rel WHERE {{ ?rel rdfs:domain ?concept . ?concept rdfs:label '{self.name}' }}")

    # Perform reasoning based on the retrieved information
    # Example: Updating goal priority based on related concepts
    for concept in relevant_concepts:
        concept_priority = ontology.query(f"SELECT ?priority WHERE {{ <{concept['concept']}> ex:hasPriority ?priority }}")
        if concept_priority:
            self.priority = max(self.priority, int(concept_priority[0]['priority']))

    # Example: Adding subgoals based on related relationships
    for relationship in relevant_relationships:
        subgoal_name = ontology.query(f"SELECT ?name WHERE {{ <{relationship['rel']}> rdfs:range ?subgoal . ?subgoal rdfs:label ?name }}")
        if subgoal_name:
            subgoal = Goal(name=subgoal_name[0]['name'], description=f"Subgoal of {self.name}")
            self.add_subgoal(subgoal)

