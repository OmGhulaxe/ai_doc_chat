from langchain_community.vectorstores.elasticsearch import ElasticsearchStore
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Embeddings using HuggingFace
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# LLM via OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY,
    model_name="meta-llama/llama-3-70b-instruct",
    temperature=0.3
)

def query_user_documents(user_id: int, query: str) -> str:
    index_name = f"user_docs_{user_id}"

    vectorstore = ElasticsearchStore(
        index_name=index_name,
        embedding=embeddings,
        es_url=ELASTICSEARCH_URL,
        metadata_field="metadata",  # ✅ Important: matches how indexing stores metadata
        embedding_field="vector"
    )

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    result = qa_chain.run(query)
    return result
