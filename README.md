# A_coding_assistant-AgenticAI

 **Problem Statement**: Large Language language struggle to Solve Complex programming problems. We need to go through a lot of requests and explanations to make LLM think about that particular problem Statement. Humans need to personally create a Lot of test cases to make LLM think about where it needs to improve, even though it fails to solve a lot of problems after multiple requests of the same problem statement.

 The main aim of this solution is to make LLM automatically think about why it is not generating a perfect approach and make it identify the potential issues with code internally, keeping that problem statement flow constant. This solution follows the same flow as humans do but without the involvement of humans. So basically, we automating the entire process of improving the code. LLM make LLM think what could be the better way to answer the question.

 > I divided the problem statement into # parts.
> 1. Generating problem statement and Edge/Complex Testcases Cases for that problem Statement.
>  2. Making LLM to solve created test cases by going though Generation, validation and Improvisation.
>  3. Once all the test cases are passed, we are now going to generate the documentation add doc strings and Comment lines to code for better understanding.

Before going from one step to the other. The model asks for human feedback if the generated response is correct for everything is okay. the user decides to go forward or not.

Humen feedback steps:
> asks if generated problem statement is correct.
>
> Ask for improvisation in the code.


 ## **LANGGRAPH WORKFLOW**
 ![Work flow](https://github.com/KoteshwarChinnolla/A_coding_assistant-AgenticAI/blob/main/output.png)
