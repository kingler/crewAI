import uuid
from typing import Any, Dict, List, Optional

from langchain.agents.agent import RunnableAgent
from langchain.agents.tools import tool as LangChainTool
from langchain.tools.render import render_text_description
from langchain_core.agents import AgentAction
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from pydantic import UUID4, BaseModel, ConfigDict, Field, InstanceOf, PrivateAttr, field_validator, model_validator
from pydantic_core import PydanticCustomError

from crewai.agents import CacheHandler, CrewAgentExecutor, CrewAgentParser, ToolsHandler
from crewai.goal import Goal, Subgoal
from crewai.memory.contextual.contextual_memory import ContextualMemory
from crewai.plan import Plan
from crewai.utilities import I18N, Logger, Prompts, RPMController
from crewai.utilities.token_counter_callback import TokenCalcHandler, TokenProcess


class Agent(BaseModel):
    # ...
    _logger: Logger = PrivateAttr()
    _rpm_controller: RPMController = PrivateAttr(default=None)
    _request_within_rpm_limit: Any = PrivateAttr(default=None)
    _token_process: TokenProcess = TokenProcess()

    ontology: Ontology
    memory: Memory
    beliefs: Optional[Dict[str, Any]] = None
    desires: Optional[List[Goal]] = None
    intentions: Optional[List[Plan]] = None

    formatting_errors: int = 0
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: UUID4 = Field(default_factory=uuid.uuid4, frozen=True)
    role: str = Field(description="Role of the agent")
    goal: str = Field(description="Objective of the agent")
    backstory: str = Field(description="Backstory of the agent")
    cache: bool = Field(default=True, description="Whether the agent should use a cache for tool usage.")
    config: Optional[Dict[str, Any]] = Field(description="Configuration for the agent", default=None)
    max_rpm: Optional[int] = Field(default=None, description="Maximum number of requests per minute for the agent execution to be respected.")
    verbose: bool = Field(default=False, description="Verbose mode for the Agent Execution")
    allow_delegation: bool = Field(default=True, description="Allow delegation of tasks to agents")
    tools: Optional[List[Any]] = Field(default_factory=list, description="Tools at agents disposal")
    max_iter: Optional[int] = Field(default=25, description="Maximum iterations for an agent to execute a task")
    max_execution_time: Optional[int] = Field(default=None, description="Maximum execution time for an agent to execute a task")
    agent_executor: InstanceOf[CrewAgentExecutor] = Field(default=None, description="An instance of the CrewAgentExecutor class.")
    crew: Any = Field(default=None, description="Crew to which the agent belongs.")
    tools_handler: InstanceOf[ToolsHandler] = Field(default=None, description="An instance of the ToolsHandler class.")
    cache_handler: InstanceOf[CacheHandler] = Field(default=None, description="An instance of the CacheHandler class.")
    step_callback: Optional[Any] = Field(default=None, description="Callback to be executed after each step of the agent execution.")
    i18n: I18N = Field(default=I18N(), description="Internationalization settings.")
    llm: Any = Field(default_factory=lambda: ChatOpenAI(model=os.environ.get("OPENAI_MODEL_NAME", "gpt-4")), description="Language model that will run the agent.")
    function_calling_llm: Optional[Any] = Field(description="Language model that will run the agent.", default=None)
    callbacks: Optional[List[InstanceOf[BaseCallbackHandler]]] = Field(default=None, description="Callback to be executed")
    system_template: Optional[str] = Field(default=None, description="System format for the agent.")
    prompt_template: Optional[str] = Field(default=None, description="Prompt format for the agent.")
    response_template: Optional[str] = Field(default=None, description="Response format for the agent.")
    beliefs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    desires: Optional[List[Goal]] = Field(default_factory=list)
    intentions: Optional[List[Plan]] = Field(default_factory=list)

    _original_role: str | None = None
    _original_goal: str | None = None
    _original_backstory: str | None = None

    def __init__(__pydantic_self__, ontology: Ontology, memory: Memory, **data):
        config = data.pop("config", {})
        super().__init__(**config, **data)
        self.ontology = ontology
        self.memory = memory
        self.beliefs = self.memory.search("beliefs")
        self.desires = self.memory.search("desires")
        self.intentions = self.memory.search("intentions")


    def update_beliefs(self, beliefs: Dict[str, Any]):
        self.memory.save(beliefs, metadata={"type": "beliefs"}, agent=self.name)
        self.beliefs = self.memory.search("beliefs")

    def update_desires(self, desires: List[Goal]):
        self.memory.save(desires, metadata={"type": "desires"}, agent=self.name)
        self.desires = self.memory.search("desires")

    def update_intentions(self, intentions: List[Plan]):
        self.memory.save(intentions, metadata={"type": "intentions"}, agent=self.name)
        self.intentions = self.memory.search("intentions")

    @field_validator("id", mode="before")
    @classmethod
    def _deny_user_set_id(cls, v: Optional[UUID4]) -> None:
        if v:
            raise PydanticCustomError("may_not_set_field", "This field is not to be set by the user.", {})

    @model_validator(mode="after")
    def set_attributes_based_on_config(self) -> "Agent":
        if self.config:
            for key, value in self.config.items():
                setattr(self, key, value)
        return self

    @model_validator(mode="after")
    def set_private_attrs(self):
        self._logger = Logger(self.verbose)
        if self.max_rpm and not self._rpm_controller:
            self._rpm_controller = RPMController(max_rpm=self.max_rpm, logger=self._logger)
        return self

    @model_validator(mode="after")
    def set_agent_executor(self) -> "Agent":
        if hasattr(self.llm, "model_name"):
            token_handler = TokenCalcHandler(self.llm.model_name, self._token_process)

            if not isinstance(self.llm.callbacks, list):
                self.llm.callbacks = []

            if not any(isinstance(handler, TokenCalcHandler) for handler in self.llm.callbacks):
                self.llm.callbacks.append(token_handler)

        if not self.agent_executor:
            if not self.cache_handler:
                self.cache_handler = CacheHandler()
            self.set_cache_handler(self.cache_handler)
        return self

    def make_decision(self, plan: Plan, task: Task, action: Action):
        # Invoke the reason method at appropriate points during decision-making
        self.ontology.reason(plan, task, action)

        # Perform other decision-making logic
        # ...

    def execute_task(self, task: Task, context: Optional[str] = None, tools: Optional[List[Any]] = None) -> str:
      task_prompt = task.prompt()

      if context:
          task_prompt = self.i18n.slice("task_with_context").format(task=task_prompt, context=context)

      if self.crew and self.crew.memory:
          contextual_memory = ContextualMemory(self.crew._short_term_memory, self.crew._long_term_memory, self.crew._entity_memory)
          memory = contextual_memory.build_context_for_task(task, context)
          if memory.strip() != "":
              task_prompt += self.i18n.slice("memory").format(memory=memory)

      tools = tools or self.tools
      parsed_tools = self._parse_tools(tools)

      self.create_agent_executor(tools=tools)
      self.agent_executor.tools = parsed_tools
      self.agent_executor.task = task

      # Invoke the reason method before executing the task
      self.ontology.reason(task.plan, task, task.actions)

      result = self.agent_executor.invoke({"input": task_prompt, "tool_names": self.agent_executor.tools_names, "tools": self.agent_executor.tools_description})["output"]

      return result

    def set_cache_handler(self, cache_handler: CacheHandler) -> None:
        self.tools_handler = ToolsHandler()
        if self.cache:
            self.cache_handler = cache_handler
            self.tools_handler.cache = cache_handler
        self.create_agent_executor()

    def set_rpm_controller(self, rpm_controller: RPMController) -> None:
        if not self._rpm_controller:
            self._rpm_controller = rpm_controller
            self.create_agent_executor()

    def create_agent_executor(self, tools=None) -> None:
        tools = tools or self.tools

        agent_args = {
            "input": lambda x: x["input"],
            "tools": lambda x: x["tools"],
            "tool_names": lambda x: x["tool_names"],
            "agent_scratchpad": lambda x: self.format_log_to_str(x["intermediate_steps"]),
        }

        executor_args = {
            "llm": self.llm,
            "i18n": self.i18n,
            "crew": self.crew,
            "crew_agent": self,
            "tools": self._parse_tools(tools),
            "verbose": self.verbose,
            "original_tools": tools,
            "handle_parsing_errors": True,
            "max_iterations": self.max_iter,
            "max_execution_time": self.max_execution_time,
            "step_callback": self.step_callback,
            "tools_handler": self.tools_handler,
            "function_calling_llm": self.function_calling_llm,
            "callbacks": self.callbacks,
        }

        if self._rpm_controller:
            executor_args["request_within_rpm_limit"] = self._rpm_controller.check_or_wait

        prompt = Prompts(i18n=self.i18n, tools=tools, system_template=self.system_template, prompt_template=self.prompt_template, response_template=self.response_template).task_execution()

        execution_prompt = prompt.partial(goal=self.goal, role=self.role, backstory=self.backstory)

        stop_words = [self.i18n.slice("observation")]
        if self.response_template:
            stop_words.append(self.response_template.split("{{ .Response }}")[1].strip())

        bind = self.llm.bind(stop=stop_words)
        inner_agent = agent_args | execution_prompt | bind | CrewAgentParser(agent=self)
        self.agent_executor = CrewAgentExecutor(agent=RunnableAgent(runnable=inner_agent), **executor_args)

    def interpolate_inputs(self, inputs: Dict[str, Any]) -> None:
        if self._original_role is None:
            self._original_role = self.role
        if self._original_goal is None:
            self._original_goal = self.goal
        if self._original_backstory is None:
            self._original_backstory = self.backstory

        if inputs:
            self.role = self._original_role.format(**inputs)
            self.goal = self._original_goal.format(**inputs)
            self.backstory = self._original_backstory.format(**inputs)

    def increment_formatting_errors(self) -> None:
        self.formatting_errors += 1

    def format_log_to_str(self, intermediate_steps: List[Tuple[AgentAction, str]], observation_prefix: str = "Observation: ", llm_prefix: str = "") -> str:
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\n{observation_prefix}{observation}\n{llm_prefix}"
        return thoughts

    def _parse_tools(self, tools: List[Any]) -> List[LangChainTool]:
        tools_list = []
        try:
            from crewai_tools import BaseTool as CrewAITool

            for tool in tools:
                if isinstance(tool, CrewAITool):
                    tools_list.append(tool.to_langchain())
                else:
                    tools_list.append(tool)
        except ModuleNotFoundError:
            for tool in tools:
                tools_list.append(tool)
        return tools_list

    @staticmethod
    def __tools_names(tools) -> str:
        return ", ".join([t.name for t in tools])

    def __repr__(self):
        return f"Agent(role={self.role}, goal={self.goal}, backstory={self.backstory})"

    def generate_plan(self, goal: Goal) -> Plan:
        plan = Plan(name=f"Plan for {goal.name}", description=f"Plan to achieve {goal.name}", associated_goal=goal)
        return plan

    def share_beliefs(self, other_agent: "Agent") -> None:
        pass

    def share_goals(self, other_agent: "Agent") -> None:
        pass

    def share_plans(self, other_agent: "Agent") -> None:
        pass
