# app/crew/crew_runner.py

# from crewai import Crew
# from app.crew.agents import create_agents
# from app.crew.tasks import create_tasks

# def run_crew_question(user_id: int, question: str):
#     retriever, summarizer, answer_composer = create_agents(user_id)
#     task1, task2, task3 = create_tasks(retriever, summarizer, answer_composer, question)
# # app/crew/crew_runner.py



from crewai import Crew
from app.crew.agents import create_agents
from app.crew.tasks import create_tasks
from app.crew.tools.vector_retriever import VectorRetrieverTool
from langchain_community.embeddings import HuggingFaceEmbeddings

# Use consistent embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def run_crew_question(user_id: int, question: str):
    # Pass embeddings into the retriever tool
    vector_tool = VectorRetrieverTool(user_id=user_id, embeddings=embeddings)

    # Pass tool into agent
    retriever, summarizer, answer_composer = create_agents(user_id, vector_tool)

    task1, task2, task3 = create_tasks(question, retriever, summarizer, answer_composer)

    # Setup crew
    crew = Crew(
        agents=[retriever, summarizer, answer_composer],
        tasks=[task1, task2, task3],
        verbose=True
    )

    # Optional: refine task prompts
    task1.description = f"Retrieve documents about: {question}"
    task3.description = f"Answer the question: {question} using summarized documents"

    return crew.kickoff()


# # /////////////////////////////////this was used//////////////////
# from crewai import Crew
# from app.crew.agents import create_agents
# from app.crew.tasks import create_tasks
# from app.crew.tools.vector_retriever import VectorRetrieverTool


# def run_crew_question(user_id: int, question: str):
#     vector_tool = VectorRetrieverTool(user_id=user_id)
#     retriever, summarizer, answer_composer = create_agents(user_id)
#     task1, task2, task3 = create_tasks(question, retriever, summarizer, answer_composer)

#     crew = Crew(
#         agents=[retriever, summarizer, answer_composer],
#         tasks=[task1, task2, task3],
#         verbose=True
#     )
#     retriever.tools = [vector_tool]
#     # Inject question dynamically into task descriptions
#     task1.description = f"Retrieve documents about: {question}"
#     task3.description = f"Answer the question: {question} using summarized documents"


#     return crew.kickoff()

    # crew = Crew(
    #     agents=[retriever, summarizer, answer_composer],
    #     tasks=[task1, task2, task3],
    #     verbose=True
    # )

    # return crew.kickoff()
