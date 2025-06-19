# # app/crew/tasks.py
# from crewai import Agent, Task, Crew

# def create_tasks(question: str, retriever: Agent, summarizer: Agent, answer_composer: Agent):
#     task1 = Task(
#         description=f"Retrieve documents about: {question}",
#         expected_output="A list of 2-3 most relevant document excerpts",
#         agent=retriever
#     )

#     task2 = Task(
#         description="Summarize the documents retrieved",
#         expected_output="A concise paragraph summarizing the key points",
#         agent=summarizer,
#         context=[task1]
#     )

#     task3 = Task(
#         description=f"Answer the question: {question} using summarized documents",
#         expected_output="A complete answer to the original question in natural language",
#         agent=answer_composer,
#         context=[task2]
#     )

#     return task1, task2, task3




# app/crew/tasks.py
from crewai import Agent, Task

def create_tasks(question: str, retriever: Agent, summarizer: Agent, answer_composer: Agent):
    task1 = Task(
        description=(
            f"""Use the vector retriever tool to search and return 2–3 relevant document snippets related to the question: "{question}".
Only return meaningful chunks of text from indexed documents. If nothing relevant is found, state that explicitly."""
        ),
        expected_output="A list of 2–3 document excerpts (each ~200–300 words) that best match the question.",
        agent=retriever,
        context=[]  # Explicitly declared for clarity
    )

    task2 = Task(
        description=(
            "Summarize the provided document excerpts into a single cohesive paragraph highlighting key insights."
        ),
        expected_output="A concise paragraph summarizing the relevant document content.",
        agent=summarizer,
        context=[task1]
    )

    task3 = Task(
        description=(
            f"""Using the summary from Task 2, provide a complete and informative answer to the user's question: "{question}".
The answer should sound natural and reference insights from the summarized content."""
        ),
        expected_output="A well-written, informative answer to the user's question, based on retrieved documents.",
        agent=answer_composer,
        context=[task2]
    )

    return task1, task2, task3
