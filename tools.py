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
from AI_coding_assistence.states import State
from AI_coding_assistence.states import WorkerState
from AI_coding_assistence.states import Sections
from langchain_groq import ChatGroq

State=State
llm=ChatGroq(model="qwen-2.5-32b")
code_llm=llm
planner = llm.with_structured_output(Sections)

with open("test_output.md", "w", encoding="utf-8") as file:
    file.write("# test_output \n\n")
class tools:

    def __init__(self):
        self.State = State
        self.llm=llm
        self.code_llm=llm

    def problem_statement_maker(self,State : State):

        sys_prompt=f"you are a problem statement maker ,your task is to generate a problem statement for the following code or prompt {State['user_prompt']}"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## problem_statement_maker \n\n"+response.content+"\n")
        print(f"# problem_statement_maker \n {response.content}")
        return {"problem_statement":response.content}

    def check_for_language(self,State :State):

        sys_prompt= f"you are given with a code or prompt, your task is to classify into the language it belongs to. \n\n given_content : {State['user_prompt']},\n\n your response must be one word wither python, java, c, cpp, java script. if language is not specified consider python"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## check_for_language \n\n"+response.content+"\n")
        print(f"# check_language \n {response.content}")
        return {"language":response.content}

    def test_case_generator(self,State :State):
        format = '''
        test case {number}:
        input: {input_without_function}
        output: {output}
        explanation: {explanation}

        '''
        sys_prompt=f"you are a test case generator, your task is to generate 5 test cases for the following problem statement \n\n {State['problem_statement']}.\n\n the generated test cases must be relent and complex should cover all the edge cases. your response must be in this format {format}"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## test_cases \n\n"+response.content+"\n")
        print(f"# test_cases \n {response.content}")
        return {"test_cases":response.content,"prompt":State["user_prompt"]}

    def code_prompt_condition(self,State :State):

        sys_prompt=f"you are given with a user message, you need to decide whether the given information is code or just a prompt, respond as code if there is no prompt involved in the given message or else it is prompt. your response must be one word either Code or Prompt. \n\n given_message : {State['user_prompt']}"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("code_prompt_condition \n\n"+response.content+"\n")
        print(f"# code_prompt_condition \n {response.content}")
        return response.content

    def generate_code_fun(self,State :State):

        sys_prompt=f"generate code in {State.get('language','python')} for the following   \n\n problem_statement : {State['problem_statement']}"
        response=code_llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## generate code \n\n"+response.content+"\n")
        print(f"# generate code \n {response.content}")
        return {"generated_code":response.content,"code":response.content,"times_visit":0}

    def polish_code_fun(self,State :State):
        format = '''
        test case {number}:
        input: {input_without_function}
        output: {output}

        explanation: {Reason behan the failed testcase}

        '''
        sys_prompt=f"You are given with code and problem statement. generate test cases the given code might fail. Be careful, generate only if it fails or not work according to the problem statement otherwise just print no failed test cases \n\n problem_statement : {State['problem_statement']} \n\n given_code : {State.get("generated_code",State['user_prompt'])} \n\n Return output in this format {format} if there are any failed test cases otherwise respond with no \"failed test cases\""
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## polish_code \n\n"+response.content+"\n")
        print(f"# polish_code + {response.content}")
        if( "code" not in State):
            return {"failed_test_cases":response.content,"code":State.get("generated_code",State['user_prompt']),"times_visit":0}
        return {"failed_test_cases":response.content}

    def review_code_fun(self,State :State):
        format = '''
        Improvements in code for failed test cases : {Improvements}
        Suggestions to make code according to problem statement : {Suggestions}
        '''

        sys_prompt=f"your task is to review the code.you are given with the problem statement and the failed test cases. suggest improvements, if there are any fail test cases or if the code is not according to the problem statement otherwise respond with the word \"perfect\" \n\n problem_statement : {State['problem_statement']} \n\n given_code : {State.get("generated_code",State['user_prompt'])} \n\n failed test cases : {State.get('failed_test_cases','')}  /n/n. if there is no failed testcases and code is according to problem statement just respond with the word \"perfect\". your response must be either word \"perfect\" or suggestions in this format {format}"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## review_code \n\n"+response.content+"\n")
        print(f"# review_code \n {response.content}")
        return {"suggestions":response.content}

    def improve_code_fun(self,State :State):

        sys_prompt=f"you are a coding assistant, your task is to improve the given code according to the suggestions, problem statement and failed test cases. response must be accurate. \n\n problem_statement : {State['problem_statement']} \n\n  given_test_cases : {State["test_cases"]}  \n\n failed test cases : {State.get('failed_test_cases','')} \n\n suggestions : {State['suggestions']} \n\n code : {State['code']} "
        response=code_llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## Improve code \n\n"+response.content+"\n")
        print(f'improved code \n {response.content}')
        State["times_visit"]=State.get("times_visit",0)+1
        return {"improved_code":response.content, "failed_test_cases":"","times_visit":State["times_visit"]}
        
    def test_code_fun(self,State :State):
        format = '''
        test case {number}:
        input: {input_without_function}
        output: {output}

        explanation: {Reason}

        '''
        sys_prompt=f"you are a code tester, you are given with the testcases. check if the code pass all the testcases. if not respond with the fail test cases in this format {format} or respond with one word \"Pass\" . \n\n given_code : {State['code']} \n\n test cases : {State['test_cases']}  \n\n your response must be single word pass if all test cases pass or else respond with failed test cases"
        response=self.llm.invoke(sys_prompt)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## test_code \n\n"+response.content+"\n")
        print(f"# test_code \n {response.content}")
        return {"failed_test_cases":response.content}

    def comment_generate(self,State :State):

        sys_prompt=f"generate the comments for the given code {State["code"]}"
        response=self.llm.invoke(sys_prompt)
        print(f"# comment lines {response.content}")
        return {"code":response.content}

    def condition_at_review(self,State :State):
        print(State["times_visit"])
        if(State["times_visit"]>=2):
            return "limit_reached"

        if State["suggestions"]=="perfect":
            return "perfect"
        else:
            return "prob_stat + suggestion +code"

    def condition_at_test(self,State:State):

        if State["failed_test_cases"]=="Pass":
            return "pass"
        else:
            return "prob_stat + suggestion +code + failed_test_cases"

    def print_all_info(self,State :State):
        # print(answer)
        human_verification=State["problem_statement"]
        human_verification+=State["language"]
        human_verification+=State["test_cases"]
        return {}



    def final_code(self,State :State):
        sys_prompt = f"you are a code organizer, your task is to organism the given code according to the given report \n\n given code : {State["code"]} \n\n report : {State["final_report"]} \n\n your output must be just code with dockstrings and comment lines and description "
        response=self.llm.invoke(sys_prompt)
        print(response.content)
        with open("test_output.md", "a", encoding="utf-8") as file:
            file.write("## Final Code \n\n"+response.content+"\n")
        with open("final_report.md", "w", encoding="utf-8") as file:
            file.write("## Final Code \n\n"+response.content+"\n")
        return {"output":response.content}

    def orchestrator(self, State: State):
        print("orchestrator",State["code"])
        try:
        # Generate queries
            report_sections = planner.invoke(
                [
                    SystemMessage(content="you are given with a code and a problem statement, you need to generate a plan to write a report for the given code according to the problem statement. report must include every small details about code in well organized format."),
                    # SystemMessage(content="Generate a plan to transform the given code into a code with docstrings ,comments and description."),  
                    # SystemMessage(content="Generate a plan to write report for the given code with docstrings and comment lines"),  
                    HumanMessage(content=f"the given code is : {State["code"]}. \n\n problem statement is : {State['problem_statement']} \n\n programming language : {State['language']}"),
                ]
            )
            print(report_sections.sections)

            return {"sections": report_sections.sections}
        except:
            return {"sections":[{"name":"report","description":"write a detailed report for following code","session_code":State["code"],"problem_statement":State["problem_statement"],"full_code":State["code"]}] }

    def llm_call(self,State:WorkerState):
        """Worker writes a section of the report"""
        try:

            # Generate section
            section = llm.invoke(
                [
                    SystemMessage(
                        content=f"Write the report section according to provided name, description, code and problem statement. Include no preamble for each section. generate response in markdown format."
                    ),
                    HumanMessage(
                        content=f"Here is the section name: {State['section'].name} \n\n description: {State['section'].description} \n\n code: {State['section'].session_code} \n\n problem statement: {State['section'].problem_statement} \n\n and entire code is {State['section'].full_code}"
                    ),
                ]
            )
            # with open("test_output.md", "a", encoding="utf-8") as file:
            #     file.write(response.content)
            print("🎟️"*20)
            print(section.content)

            # Write the updated section to completed sections
            return {"completed_sections": [section.content]}
        except:
            return {"completed_sections": []}


    def synthesizer(self,State:State):
        """Synthesize full report from sections"""
        if State["completed_sections"] == []:
            response=self.llm.invoke(f"write a detailed report for the given code according to the problem statement \n\n given code : {State['code']} \n\n problem statement : {State['problem_statement']}")
            return {"final_report": response.content}
        else:

            # List of completed sections
            completed_sections = State["completed_sections"]

            # Format completed section to str to use as context for final sections
            completed_report_sections = "\n\n---\n\n".join(completed_sections)

            print("🎟️"*20)
            with open("test_output.md", "a", encoding="utf-8") as file:
                file.write("# Documentation \n\n"+completed_report_sections+"\n\n")
            print("#Documentation \n\n" + completed_report_sections + "\n\n")

            return {"final_report": completed_report_sections}

    def assign_workers(self,State:State):
        """Assign a worker to each section in the plan"""

        # Kick off section writing in parallel via Send() API
        return [Send("llm_call", {"section": s}) for s in State["sections"]]

    def documentation(self,State:State):

        if "stop" not in State:
            return {"stop":"continue"}
        elif State["stop"]=="failed":
            return {"failed_test_cases":State["failed_test_cases"],"stop":"failed"}
        else:
            return {"stop":"stop"}

    def documentation_condition(self,State:State):

        if State["stop"]=="stop":
            return "stop"
        elif State["stop"]=="failed":
            return "failed"
        else:
            return "continue"