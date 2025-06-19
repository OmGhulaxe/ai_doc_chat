

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.database import get_db
from app import models
from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch, exceptions as es_exceptions, helpers
import os
import time

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def check_elasticsearch_connection(url: str, max_retries: int = 3) -> bool:
    print(f"🔌 Checking Elasticsearch connection at {url}...")
    for attempt in range(max_retries):
        try:
            client = Elasticsearch(url)
            if client.ping():
                print("✅ Connected to Elasticsearch")
                client.close()
                return True
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    return False


def create_index_if_not_exists(es: Elasticsearch, index_name: str):
    if not es.indices.exists(index=index_name):
        print(f"📁 Creating index '{index_name}'...")
        index_body = {
            "mappings": {
                "properties": {
                    "vector": {"type": "dense_vector", "dims": 384},
                    "page_content": {"type": "text"},
                    "title": {"type": "text"},
                    "user_id": {"type": "integer"},
                    "document_id": {"type": "integer"}
                }
            }
        }
        es.indices.create(index=index_name, body=index_body)
        print("✅ Index created.")


def index_documents(user_id: int):
    if not check_elasticsearch_connection(ELASTICSEARCH_URL):
        print("❌ Could not connect to Elasticsearch.")
        return

    db: Session = next(get_db())

    documents = db.query(models.Document).filter(
        models.Document.user_id == user_id,
        models.Document.is_indexed == False,
        models.Document.content.isnot(None)
    ).all()

    if not documents:
        print("✅ No unindexed documents found.")
        return

    print(f"📄 Found {len(documents)} document(s) to index.")
    all_chunks = []
    for doc in documents:
        chunks = text_splitter.create_documents([doc.content])
        for chunk in chunks:
            title = getattr(doc, "filename", "Untitled")
            metadata = {
                "page_content": chunk.page_content,
                "title": title,
                "user_id": doc.user_id,
                "document_id": doc.id,
            }
            all_chunks.append(metadata)
            print(f"✂️ Chunk (preview): {chunk.page_content[:80].strip()}...")

    index_name = f"user_docs_{user_id}"
    print(f"🚀 Total chunks to index: {len(all_chunks)}")

    try:
        es = Elasticsearch(ELASTICSEARCH_URL)
        create_index_if_not_exists(es, index_name)

        # Compute embeddings and bulk insert
        texts = [chunk["page_content"] for chunk in all_chunks]
        vectors = embeddings.embed_documents(texts)

        actions = []
        for i, chunk in enumerate(all_chunks):
            doc_body = {
                "page_content": chunk["page_content"],
                "title": chunk["title"],
                "user_id": chunk["user_id"],
                "document_id": chunk["document_id"],
                "vector": vectors[i],
            }
            actions.append({
                "_index": index_name,
                "_source": doc_body,
            })

        helpers.bulk(es, actions)
        es.indices.refresh(index=index_name)
        print(f"✅ Successfully indexed and refreshed '{index_name}'")

        for doc in documents:
            doc.is_indexed = True
        db.commit()
        print(f"✅ Updated DB: Marked {len(documents)} documents as indexed.")
        es.close()

    except es_exceptions.ConnectionError as e:
        print(f"❌ Elasticsearch connection error: {str(e)}")
    except Exception as e:
        print(f"❌ Indexing failed: {str(e)}")
