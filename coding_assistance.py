from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from IPython.display import Image,display
from typing import Annotated,List
import operator
from pydantic import BaseModel,Field
from langgraph.constants import Send
from typing_extensions import Literal
from pydantic import BaseModel,Field
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
# from states import State
from states import Section
from states import Sections
from states import WorkerState
from langchain_groq import ChatGroq
from tools import tools


llm = ChatGroq(model="qwen-2.5-32b")

code_llm=llm
planner = llm.with_structured_output(Sections)

class State(TypedDict):
    user_prompt: str
    prompt: str
    problem_statement: str
    language: str
    test_cases: str
    code: str
    generated_code: str
    suggestions: str
    improved_code: str
    output: str
    steps: str
    logic: str
    failed_test_cases: str
    arguments: str
    result: str
    sections: list[Section] 
    completed_sections: Annotated[
        list,operator.add
    ]  
    final_report: str
    stop: str


class coding_assistance:

    def __init__(self):

        self.MemorySaver = MemorySaver
        t=tools()
        self.workflow = StateGraph(State)

        self.workflow.add_node("problem_statement_maker",t.problem_statement_maker)
        self.workflow.add_node("check_for_language",t.check_for_language)
        self.workflow.add_node("test_case_generator",t.test_case_generator)
        self.workflow.add_node("print_all_info",t.print_all_info)
        self.workflow.add_node("generate_code_fun",t.generate_code_fun)
        self.workflow.add_node("polish_code_fun",t.polish_code_fun)
        self.workflow.add_node("review_code_fun",t.review_code_fun)
        self.workflow.add_node("improve_code_fun",t.improve_code_fun)
        self.workflow.add_node("test_code_fun",t.test_code_fun)
        self.workflow.add_node("orchestrator",t.orchestrator)
        self.workflow.add_node("llm_call",t.llm_call)
        self.workflow.add_node("synthesizer",t.synthesizer)
        self.workflow.add_node("final_code",t.final_code)
        self.workflow.add_node("documentation",t.documentation)

        self.workflow.add_edge(START,"check_for_language")
        self.workflow.add_edge("check_for_language","problem_statement_maker")
        self.workflow.add_edge("problem_statement_maker","test_case_generator")
        self.workflow.add_edge("test_case_generator","print_all_info")
        self.workflow.add_conditional_edges("print_all_info",t.code_prompt_condition,{"Prompt": "generate_code_fun","Code": "polish_code_fun"})
        self.workflow.add_edge("generate_code_fun","polish_code_fun")
        self.workflow.add_edge("polish_code_fun","review_code_fun")
        self.workflow.add_conditional_edges("review_code_fun",t.condition_at_review,{"perfect":"test_code_fun","prob_stat + suggestion +code":"improve_code_fun"})
        self.workflow.add_edge("improve_code_fun","polish_code_fun")
        self.workflow.add_conditional_edges("test_code_fun",t.condition_at_test,{"prob_stat + suggestion +code + failed_test_cases":"improve_code_fun","pass":"documentation"})
        self.workflow.add_conditional_edges("documentation",t.documentation_condition,{"stop":END,"continue":"orchestrator"})
        self.workflow.add_conditional_edges(
            "orchestrator",t.assign_workers,["llm_call"]
        )
        self.workflow.add_edge("llm_call","synthesizer")
        self.workflow.add_edge("synthesizer","final_code")
        self.workflow.add_edge("final_code",END)

        memory = MemorySaver()

        self.chain = self.workflow.compile(checkpointer=memory,interrupt_after=["test_case_generator"],interrupt_before=["documentation"])

    def graph(self):
        return self.chain

