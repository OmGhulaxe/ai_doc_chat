# # app/embeddings.py

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_elasticsearch import ElasticsearchStore
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from app.database import get_db
# from app import models
# from sqlalchemy.orm import Session
# import os
# from langchain_huggingface import HuggingFaceEmbeddings
# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import ConnectionError
# import time

# ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

# # Initialize Embeddings and Text Splitter
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# def check_elasticsearch_connection(url: str, max_retries: int = 3) -> bool:
#     print(f"Checking Elasticsearch connection at {url}...")
#     for attempt in range(max_retries):
#         try:
#             client = Elasticsearch(url)
#             if client.ping():
#                 print("✅ Successfully connected to Elasticsearch")
#                 info = client.info()
#                 print(f"Elasticsearch version: {info['version']['number']}")
#                 client.close()
#                 return True
#             else:
#                 print("❌ Elasticsearch ping failed")
#         except Exception as e:
#             print(f"❌ Connection attempt {attempt + 1}/{max_retries} failed: {str(e)}")
#             if attempt < max_retries - 1:
#                 time.sleep(2)
#     return False

# def index_documents(user_id: int):
#     if not check_elasticsearch_connection(ELASTICSEARCH_URL):
#         print("❌ Could not connect to Elasticsearch. Please ensure it is running and accessible.")
#         return

#     print(f"🔍 Checking for unindexed documents for user_id={user_id}...")

#     db: Session = next(get_db())

#     documents = db.query(models.Document).filter(
#         models.Document.user_id == user_id,
#         models.Document.is_indexed == False,
#         models.Document.content.isnot(None)
#     ).all()

#     if not documents:
#         print("✅ No new documents to embed. All are already indexed.")
#         return

#     print(f"📄 Found {len(documents)} new document(s) to index.")

#     documents_with_metadata = []
#     for doc in documents:
#         chunks = text_splitter.create_documents([doc.content])
#         for chunk in chunks:
#             doc_with_metadata = Document(
#                 page_content=chunk.page_content,
#                 metadata={
#                     "title": getattr(doc, 'title', None) or getattr(doc, 'name', None) or getattr(doc, 'filename', None) or "Untitled",
#                     "user_id": doc.user_id,
#                     "document_id": doc.id
#                 }
#             )
#             documents_with_metadata.append(doc_with_metadata)

#     print(f"✂️ Split into {len(documents_with_metadata)} text chunk(s) for embedding...")

#     try:
#         client = Elasticsearch(ELASTICSEARCH_URL)
#         if not client.indices.exists(index=f"user_docs_{user_id}"):
#             print(f"Creating new index 'user_docs_{user_id}'...")

#         ElasticsearchStore.from_documents(
#             documents_with_metadata,
#             embeddings,
#             es_url=ELASTICSEARCH_URL,
#             index_name=f"user_docs_{user_id}",
#             embedding_field="vector",
#             metadata_field="metadata"
#         )
#         print(f"✅ Successfully indexed chunks to Elasticsearch index 'user_docs_{user_id}'")

#         for doc in documents:
#             doc.is_indexed = True
#         db.commit()
#         print(f"✅ Marked {len(documents)} document(s) as indexed in the database.")

#     except ConnectionError as e:
#         print(f"❌ Connection to Elasticsearch failed: {str(e)}")
#         print("Please ensure Elasticsearch is running and accessible at", ELASTICSEARCH_URL)
#     except Exception as e:
#         print(f"❌ Failed to index documents: {str(e)}")
#     finally:
#         if 'client' in locals():
#             client.close()
#     return




# /////////////////////////////////////this is used//////////
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import ElasticsearchStore
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from app.database import get_db
# from app import models
# from sqlalchemy.orm import Session
# from elasticsearch import Elasticsearch, exceptions as es_exceptions
# import os
# import time

# ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

# # Initialize once
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# def check_elasticsearch_connection(url: str, max_retries: int = 3) -> bool:
#     print(f"🔌 Checking Elasticsearch connection at {url}...")
#     for attempt in range(max_retries):
#         try:
#             client = Elasticsearch(url)
#             if client.ping():
#                 print("✅ Connected to Elasticsearch")
#                 print(f"Version: {client.info()['version']['number']}")
#                 client.close()
#                 return True
#         except Exception as e:
#             print(f"❌ Attempt {attempt + 1} failed: {e}")
#             time.sleep(2)
#     return False

# def create_index_if_not_exists(es: Elasticsearch, index_name: str):
#     if not es.indices.exists(index=index_name):
#         print(f"📁 Creating index '{index_name}'...")
#         index_body = {
#             "mappings": {
#                 "properties": {
#                     "vector": {"type": "dense_vector", "dims": 384},
#                     "page_content": {"type": "text"},
#                     "title": {"type": "text"},
#                     "user_id": {"type": "integer"},
#                     "document_id": {"type": "integer"}
#                 }
#             }
#         }
#         es.indices.create(index=index_name, body=index_body)
#         print("✅ Index created.")

# def index_documents(user_id: int):
#     if not check_elasticsearch_connection(ELASTICSEARCH_URL):
#         print("❌ Could not connect to Elasticsearch.")
#         return

#     db: Session = next(get_db())

#     documents = db.query(models.Document).filter(
#         models.Document.user_id == user_id,
#         models.Document.is_indexed == False,
#         models.Document.content.isnot(None)
#     ).all()

#     if not documents:
#         print("✅ No unindexed documents found.")
#         return

#     print(f"📄 Found {len(documents)} document(s) to index.")

#     all_chunks = []
#     for doc in documents:
#         chunks = text_splitter.create_documents([doc.content])
#         for chunk in chunks:
#             print(f"✂️ Chunk (preview): {chunk.page_content[:80].strip()}...")

#             # Fix: Add metadata as flat fields instead of nested "metadata"
#             doc_with_metadata = Document(
#                 page_content=chunk.page_content,
#                 metadata={
#                     "title": getattr(doc, "title", None) or doc.filename or "Untitled",
#                     "user_id": doc.user_id,
#                     "document_id": doc.id
#                 }
#             )
#             all_chunks.append(doc_with_metadata)

#     index_name = f"user_docs_{user_id}"
#     print(f"🚀 Total chunks to index: {len(all_chunks)}")

#     try:
#         client = Elasticsearch(ELASTICSEARCH_URL)
#         create_index_if_not_exists(client, index_name)

#         ElasticsearchStore.from_documents(
#             documents=all_chunks,
#             embedding=embeddings,
#             es_url=ELASTICSEARCH_URL,
#             index_name=index_name,
#         )

#         print(f"✅ Successfully indexed chunks to '{index_name}'")
#         client.indices.refresh(index=index_name)

#         for doc in documents:
#             doc.is_indexed = True
#         db.commit()
#         print(f"✅ Updated DB: Marked {len(documents)} documents as indexed.")

#     except es_exceptions.ConnectionError as e:
#         print(f"❌ Elasticsearch connection error: {str(e)}")
#     except Exception as e:
#         print(f"❌ Indexing failed: {str(e)}")
#     finally:
#         if 'client' in locals():
#             client.close()











# app/embeddings.py

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_elasticsearch import ElasticsearchStore
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from app.database import get_db
# from app import models
# from sqlalchemy.orm import Session
# from unstructured.partition.auto import partition
# import os
# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import ConnectionError
# import time

# # --- Configuration ---
# ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
# UPLOAD_DIR = "uploads"

# # --- Components ---
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


# def check_elasticsearch_connection(url: str, max_retries: int = 3) -> bool:
#     print(f"Checking Elasticsearch connection at {url}...")
#     for attempt in range(max_retries):
#         try:
#             client = Elasticsearch(url)
#             if client.ping():
#                 print("✅ Connected to Elasticsearch")
#                 info = client.info()
#                 print(f"Elasticsearch version: {info['version']['number']}")
#                 client.close()
#                 return True
#             else:
#                 print("❌ Elasticsearch ping failed")
#         except Exception as e:
#             print(f"❌ Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
#             if attempt < max_retries - 1:
#                 time.sleep(2)
#     return False


# def parse_document_from_file(filename: str) -> str:
#     try:
#         elements = partition(filename=filename)
#         content = "\n".join(
#             el.text.strip() for el in elements if hasattr(el, "text") and el.text
#         )
#         return content.strip()
#     except Exception as e:
#         print(f"❌ Failed to parse with unstructured.io: {str(e)}")
#         return ""


# def index_documents(user_id: int):
#     if not check_elasticsearch_connection(ELASTICSEARCH_URL):
#         print("❌ Could not connect to Elasticsearch.")
#         return

#     db: Session = next(get_db())

#     print(f"🔍 Checking for unindexed documents for user_id={user_id}...")

#     documents = db.query(models.Document).filter(
#         models.Document.user_id == user_id,
#         models.Document.is_indexed == False
#     ).all()

#     if not documents:
#         print("✅ No new documents to embed.")
#         return

#     print(f"📄 Found {len(documents)} document(s) to process...")

#     documents_with_metadata = []

#     for doc in documents:
#         # Parse content if missing
#         if not doc.content or not doc.content.strip():
#             file_path = os.path.join(UPLOAD_DIR, doc.filename)
#             if os.path.exists(file_path):
#                 print(f"🔍 Re-parsing missing content from file: {doc.filename}")
#                 doc.content = parse_document_from_file(file_path)
#                 if not doc.content:
#                     print(f"⚠️ Skipping file (no content): {doc.filename}")
#                     continue
#             else:
#                 print(f"⚠️ File not found: {file_path}")
#                 continue

#         # Split content into chunks
#         chunks = text_splitter.create_documents([doc.content])
#         for chunk in chunks:
#             documents_with_metadata.append(
#                 Document(
#                     page_content=chunk.page_content,
#                     metadata={
#                         "title": doc.title or doc.name or doc.filename or "Untitled",
#                         "user_id": doc.user_id,
#                         "document_id": doc.id
#                     }
#                 )
#             )

#     print(f"✂️ Prepared {len(documents_with_metadata)} chunk(s) for indexing.")

#     try:
#         client = Elasticsearch(ELASTICSEARCH_URL)
#         index_name = f"user_docs_{user_id}"

#         if not client.indices.exists(index=index_name):
#             print(f"🆕 Creating Elasticsearch index: {index_name}")

#         ElasticsearchStore.from_documents(
#             documents_with_metadata,
#             embeddings,
#             es_url=ELASTICSEARCH_URL,
#             index_name=index_name,
#             embedding_field="vector",
#             metadata_field="metadata"
#         )

#         print(f"✅ Indexed to Elasticsearch: {index_name}")

#         # Mark documents as indexed in DB
#         for doc in documents:
#             doc.is_indexed = True
#         db.commit()
#         print(f"✅ Updated indexing status in DB.")

#     except ConnectionError as e:
#         print(f"❌ Elasticsearch connection failed: {str(e)}")
#     except Exception as e:
#         print(f"❌ Indexing error: {str(e)}")
#     finally:
#         if 'client' in locals():
#             client.close()



# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_elasticsearch import ElasticsearchStore
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from app.database import get_db
# from app import models
# from sqlalchemy.orm import Session
# from elasticsearch import Elasticsearch, exceptions as es_exceptions
# import os
# import time

# ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

# # Initialize once
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# def check_elasticsearch_connection(url: str, max_retries: int = 3) -> bool:
#     print(f"🔌 Checking Elasticsearch connection at {url}...")
#     for attempt in range(max_retries):
#         try:
#             client = Elasticsearch(url)
#             if client.ping():
#                 print("✅ Connected to Elasticsearch")
#                 print(f"Version: {client.info()['version']['number']}")
#                 client.close()
#                 return True
#         except Exception as e:
#             print(f"❌ Attempt {attempt + 1} failed: {e}")
#             time.sleep(2)
#     return False

# def create_index_if_not_exists(es: Elasticsearch, index_name: str):
#     if not es.indices.exists(index=index_name):
#         print(f"📁 Creating index '{index_name}'...")
#         index_body = {
#             "mappings": {
#                 "properties": {
#                     "vector": {"type": "dense_vector", "dims": 384},  # Match your embedding dims
#                     "metadata": {"type": "object"},
#                     "page_content": {"type": "text"}  # ✅ Use page_content not content
#                 }
#             }
#         }
#         es.indices.create(index=index_name, body=index_body)
#         print("✅ Index created.")

# def index_documents(user_id: int):
#     if not check_elasticsearch_connection(ELASTICSEARCH_URL):
#         print("❌ Could not connect to Elasticsearch.")
#         return

#     db: Session = next(get_db())

#     documents = db.query(models.Document).filter(
#         models.Document.user_id == user_id,
#         models.Document.is_indexed == False,
#         models.Document.content.isnot(None)
#     ).all()

#     if not documents:
#         print("✅ No unindexed documents found.")
#         return

#     print(f"📄 Found {len(documents)} document(s) to index.")

#     all_chunks = []
#     for doc in documents:
#         chunks = text_splitter.create_documents([doc.content])
#         for chunk in chunks:
#             print(f"✂️ Chunk (preview): {chunk.page_content[:80].strip()}...")
#             doc_with_metadata = Document(
#                 page_content=chunk.page_content,
#                 metadata={
#                     "title": getattr(doc, "title", None) or doc.filename or "Untitled",
#                     "user_id": doc.user_id,
#                     "document_id": doc.id
#                 }
#             )
#             all_chunks.append(doc_with_metadata)

#     index_name = f"user_docs_{user_id}"
#     print(f"🚀 Total chunks to index: {len(all_chunks)}")

#     try:
#         client = Elasticsearch(ELASTICSEARCH_URL)
#         create_index_if_not_exists(client, index_name)

#         # ✅ Set text_field="page_content" to match retriever logic
#         ElasticsearchStore.from_documents(
#             documents=all_chunks,
#             embedding=embeddings,
#             es_url=ELASTICSEARCH_URL,
#             index_name=index_name,
#             text_field="page_content"
#         )

#         print(f"✅ Successfully indexed chunks to '{index_name}'")

#         for doc in documents:
#             doc.is_indexed = True
#         db.commit()
#         print(f"✅ Updated DB: Marked {len(documents)} documents as indexed.")

#     except es_exceptions.ConnectionError as e:
#         print(f"❌ Elasticsearch connection error: {str(e)}")
#     except Exception as e:
#         print(f"❌ Indexing failed: {str(e)}")
#     finally:
#         if 'client' in locals():
#             client.close()


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
