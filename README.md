# A_coding_assistant-AgenticAI

 **Problem Statement**: Large Language language struggle to Solve Complex programming problems. We need to go through a lot of requests and explanations to make LLM think about that particular problem Statement. Humans need to personally create a Lot of test cases to make LLM think about where it needs to improve, even though it fails to solve a lot of problems after multiple requests of the same problem statement.

 The main aim of this solution is to make LLM automatically think about why it is not generating a perfect approach and make it identify the potential issues with code internally, keeping that problem statement flow constant. This solution follows the same flow as humans do but without the involvement of humans. So basically, we automating the entire process of improving the code. LLM make LLM think what could be the better way to answer the question.

 > I divided the problem statement into # parts.
> 1. Generating problem statement and Edge/Complex Testcases Cases for that problem Statement.
>  2. Making LLM to solve created test cases by going though Generation, validation and Improvisation.
>  3. Once all the test cases are passed, we are now going to generate the documentation add doc strings and Comment lines to code for better understanding.

Before going from one step to the other. The model asks for human feedback if the generated response is correct for everything is okay. the user decides to go forward or not.

Humen feedback steps:
> asks if the generated problem statement is correct.
>
> Ask for improvisation in the code.

## **Work Flow Explanation**

**Start**: User can give code or prompt Ask for generation of code.

**Check for language**: Check for what language to print the solution IN.

**Problem Statement Maker**: Generate well-structured problem statements for given user prompt/code

**Test case generator**: Generate the most complex and edge test cases according to the problem statement

**Ask for human review if the generated problem statement is according to the User request**

**Print all info**: Decide whether the user input is code or prompt

**Polish code**: checks if there are any Test cases the generated/given code fails to answer.

**Review Code**: checks if the given code is according to the problem statement and if there are anything that goes wrong; generates suggestions and sends it to Improving code

**If everything is perfect at the review code, then it sends the code to the test case checker**

**Improving code function**: Improves code according to the given problem statement, suggestion, and failed test cases.

**Test code function**: checks if the code passes all the generated test cases; if it fails any, it passes the failed test cases to improve code function.

**Human feedback if any test cases are failing in their IDE. then it sends back to the review code so that the flow repeats until the code is executed properly. If everything is okay, the user wants documentation and explanation, then it goes to the documentation function; otherwise wise it stops**

**Orchestrater**: It is responsible for most structured documentation. In a way that explains the entire code. This is a loop of LLM_call, synthesizer.

**Final_code**: here the code is generated with docstrings and comment lines explaining all the functions and logic.




 ## **LANGGRAPH WORKFLOW**
 ![Work flow](https://github.com/KoteshwarChinnolla/A_coding_assistant-AgenticAI/blob/main/output.png)
