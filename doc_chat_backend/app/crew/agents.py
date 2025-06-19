# # app/crew/agents.py

# from crewai import Agent
# from app.crew.llmprovider import llm
# from app.crew.tools.vector_retriever import VectorRetrieverTool
# from app.crew.llmprovider import llm  # This should now be the callable function, not a dict


# def create_agents(user_id: int):
#     # Dynamically create the tool for the current user
#     vector_tool = VectorRetrieverTool(user_id=user_id)

#     retriever = Agent(
#         role="Document Retriever",
#         goal="Search and retrieve relevant documents",
#         backstory="Expert in navigating document embeddings and queries.",
#         llm=llm,
#         tools=[vector_tool],
#         verbose=True
#     )

#     summarizer = Agent(
#         role="Summarizer",
#         goal="Summarize relevant sections from the documents",
#         backstory="Knows how to boil down complex documents into digestible insights.",
#         llm=llm,
#         verbose=True
#     )

#     answer_composer = Agent(
#         role="Answer Composer",
#         goal="Generate final answer based on retrieved context",
#         backstory="Great at writing human-like, context-rich responses.",
#         llm=llm,
#         verbose=True
#     )

#     return retriever, summarizer, answer_composer


from crewai import Agent
from app.crew.llmprovider import llm

def create_agents(user_id: int, vector_tool):
    retriever = Agent(
        role="Document Retriever",
        goal="Search and retrieve relevant documents",
        backstory="Expert in navigating document embeddings and queries.",
        llm=llm,
        tools=[vector_tool],
        verbose=True
    )

    summarizer = Agent(
        role="Summarizer",
        goal="Summarize relevant sections from the documents",
        backstory="Knows how to boil down complex documents into digestible insights.",
        llm=llm,
        verbose=True
    )

    answer_composer = Agent(
        role="Answer Composer",
        goal="Generate final answer based on retrieved context",
        backstory="Great at writing human-like, context-rich responses.",
        llm=llm,
        verbose=True
    )

    return retriever, summarizer, answer_composer
