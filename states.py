from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Annotated, List
import operator
from pydantic import BaseModel, Field
from langgraph.constants import Send
from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq

llm=ChatGroq(model="qwen-2.5-32b")
code_llm=llm

class Section(BaseModel):
    
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )
    session_code: str = Field(
        description="code related to this section",
    )
    problem_statement: str = Field(
        description="problem statement to write report on",
    )
    full_code: str = Field(
        description="Entire code to write report on",
    )



class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )


planner = llm.with_structured_output(Sections)

class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]


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
        list, operator.add
    ]  
    final_report: str
    times_visit: int
