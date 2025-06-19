# # app/crew/tools/vector_retriever.py

# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool
# from typing import Optional
# from elasticsearch import Elasticsearch
# import os
# import logging
# from langchain_community.embeddings import HuggingFaceEmbeddings

# logger = logging.getLogger(__name__)

# class VectorRetrieverToolSchema(BaseModel):
#     query: str

# class VectorRetrieverTool(BaseTool):
#     name: str = "vector_retriever"
#     description: str = "Use this tool to find documents related to a user's question from Elasticsearch."
#     args_schema = VectorRetrieverToolSchema

#     user_id: int
#     embeddings: Optional[HuggingFaceEmbeddings] = None
#     es_url: Optional[str] = None

#     def __init__(self, **kwargs):
#         if 'user_id' not in kwargs:
#             raise ValueError("user_id is required")

#         super().__init__(**kwargs)

#         self.user_id = kwargs['user_id']
#         self.embeddings = kwargs.get('embeddings') or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         self.es_url = kwargs.get('es_url') or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

#     def _get_index_name(self) -> str:
#         return f"user_docs_{self.user_id}"

#     def _check_index_exists(self, client: Elasticsearch, index_name: str) -> bool:
#         try:
#             return client.indices.exists(index=index_name)
#         except Exception as e:
#             logger.error(f"Error checking index existence: {str(e)}")
#             return False

#     def _run(self, query: str) -> str:
#         client = None
#         try:
#             client = Elasticsearch(self.es_url)
#             index_name = self._get_index_name()

#             if not self._check_index_exists(client, index_name):
#                 return (
#                     f"No documents found for user ID {self.user_id}. "
#                     "Please make sure documents have been uploaded and indexed first."
#                 )

#             query_vector = self.embeddings.embed_query(query)

#             search_query = {
#                 "query": {
#                     "bool": {
#                         "must": [
#                             {
#                                 "multi_match": {
#                                     "query": query,
#                                     "fields": ["content^2", "metadata.title^3"],
#                                     "fuzziness": "AUTO"
#                                 }
#                             }
#                         ],
#                         "should": [
#                             {
#                                 "script_score": {
#                                     "query": {"match_all": {}},
#                                     "script": {
#                                         "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
#                                         "params": {"query_vector": query_vector}
#                                     }
#                                 }
#                             }
#                         ],
#                         "filter": [
#                             {"term": {"metadata.user_id": self.user_id}}
#                         ]
#                     }
#                 },
#                 "_source": ["content", "metadata"],
#                 "size": 5
#             }

#             response = client.search(index=index_name, body=search_query)
#             hits = response["hits"]["hits"]

#             if not hits:
#                 return "I could not find any relevant documents to answer your question."

#             results = []
#             for hit in hits:
#                 source = hit["_source"]
#                 score = hit["_score"]
#                 metadata = source.get("metadata", {})
#                 title = metadata.get("title", "Untitled Document")
#                 content = source.get("content", "")

#                 start = max(0, content.lower().find(query.lower()) - 200)
#                 end = min(len(content), start + 1000)
#                 snippet = content[start:end]

#                 results.append(
#                     f"📄 Document: {title}\n"
#                     f"Relevance Score: {score:.2f}\n"
#                     f"Content:\n{snippet}\n"
#                 )

#             final_response = "\n\n---\n\n".join(results)
#             return (
#                 f"Here are the most relevant documents I found:\n\n{final_response}\n\n"
#                 f"These documents should help answer your question about: {query}"
#             )

#         except Exception as e:
#             logger.error(f"Search error: {str(e)}", exc_info=True)
#             return f"I encountered an error while searching: {str(e)}"
#         finally:
#             if client:
#                 client.close()




# app/crew/tools/vector_retriever.py
# ///////////////////////////////////////thsi on e was used//////
# from pydantic import BaseModel
# from crewai.tools import BaseTool
# from typing import Optional
# from elasticsearch import Elasticsearch
# import os
# import logging
# from langchain_community.embeddings import HuggingFaceEmbeddings

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# class VectorRetrieverToolSchema(BaseModel):
#     query: str

# class VectorRetrieverTool(BaseTool):
#     name: str = "vector_retriever"
#     description: str = "Use this tool to find documents related to a user's question from Elasticsearch."
#     args_schema = VectorRetrieverToolSchema

#     user_id: int
#     embeddings: Optional[HuggingFaceEmbeddings] = None
#     es_url: Optional[str] = None

#     def __init__(self, **kwargs):
#         if 'user_id' not in kwargs:
#             raise ValueError("user_id is required")
#         super().__init__(**kwargs)

#         self.user_id = kwargs['user_id']
#         self.embeddings = kwargs.get('embeddings') or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         self.es_url = kwargs.get('es_url') or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

#     def _get_index_name(self) -> str:
#         return f"user_docs_{self.user_id}"

#     def _check_index_exists(self, client: Elasticsearch, index_name: str) -> bool:
#         try:
#             return client.indices.exists(index=index_name)
#         except Exception as e:
#             logger.error(f"Error checking index existence: {str(e)}")
#             return False

#     def _run(self, query: str) -> str:
#         logger.info(f"🧠 VectorRetrieverTool triggered with query: {query}")

#         client = None

#         try:
#             client = Elasticsearch(self.es_url)
#             index_name = self._get_index_name()

#             if not self._check_index_exists(client, index_name):
#                 return (
#                     f"⚠️ No documents found for user ID {self.user_id}. "
#                     f"Make sure documents are uploaded and indexed in `{index_name}`."
#                 )

#             query_vector = self.embeddings.embed_query(query)

#             if not query_vector or not isinstance(query_vector, list):
#                 return "⚠️ Failed to generate a valid embedding vector for the query."

#             logger.debug(f"Query vector generated with length: {len(query_vector)}")

#             # MAIN FIX 🔧: Match user_id as FLAT field, not nested
#             search_query = {
#                 "size": 5,
#                 "query": {
#                     "script_score": {
#                         "query": {
#                             "bool": {
#                                 "filter": [
#                                     {"term": {"user_id": self.user_id}}  # Flattened user_id match
#                                 ]
#                             }
#                         },
#                         "script": {
#                             "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
#                             "params": {"query_vector": query_vector}
#                         }
#                     }
#                 },
#                 "_source": ["page_content", "title", "user_id", "document_id"]
#             }

#             logger.debug(f"🔎 Sending search request to index `{index_name}`...")
#             response = client.search(index=index_name, body=search_query)
#             hits = response.get("hits", {}).get("hits", [])

#             logger.debug(f"✅ Search returned {len(hits)} hits")

#             if not hits:
#                 return "❌ I could not find any relevant documents to answer your question."

#             results = []
#             for idx, hit in enumerate(hits):
#                 source = hit["_source"]
#                 score = hit.get("_score", 0)
#                 title = source.get("title", "Untitled Document")
#                 content = source.get("page_content", "").strip()

#                 logger.debug(f"\n--- Hit {idx + 1} ---\nTitle: {title}\nScore: {score:.2f}\nPreview: {content[:150]}...\n")

#                 if not content:
#                     continue

#                 # Highlight query snippet (optional, fallback to full content)
#                 lower_content = content.lower()
#                 lower_query = query.lower()
#                 if lower_query in lower_content:
#                     start = max(0, lower_content.find(lower_query) - 200)
#                     end = min(len(content), start + 1000)
#                     snippet = content[start:end]
#                 else:
#                     snippet = content[:500]

#                 results.append(
#                     f"📄 Document: {title}\n"
#                     f"Relevance Score: {score:.2f}\n"
#                     f"Content:\n{snippet}\n"
#                 )

#             if not results:
#                 return "⚠️ Documents were found, but they seem to be empty or irrelevant."

#             return (
#                 f"🔍 Here are the most relevant documents I found:\n\n" +
#                 "\n\n---\n\n".join(results) +
#                 f"\n\n🧠 These may help you answer your question about: **{query}**"
#             )

#         except Exception as e:
#             logger.error(f"❌ Search error: {str(e)}", exc_info=True)
#             return f"An error occurred while searching: {str(e)}"
#         finally:
#             if client:
#                 client.close()





# from pydantic import BaseModel
# from crewai.tools import BaseTool
# from typing import Optional
# from elasticsearch import Elasticsearch
# from langchain_community.embeddings import HuggingFaceEmbeddings
# import os
# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# class VectorRetrieverToolSchema(BaseModel):
#     query: str

# class VectorRetrieverTool(BaseTool):
#     name: str = "vector_retriever"
#     description: str = "Use this tool to find documents related to a user's question from Elasticsearch."
#     args_schema = VectorRetrieverToolSchema

#     user_id: int
#     embeddings: HuggingFaceEmbeddings
#     es_url: str

#     def __init__(self, **kwargs):
#         if 'user_id' not in kwargs:
#             raise ValueError("user_id is required")

#         super().__init__(**kwargs)

#         self.user_id = kwargs['user_id']
#         self.embeddings = kwargs.get('embeddings') or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         self.es_url = kwargs.get('es_url') or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

#     def _get_index_name(self) -> str:
#         return f"user_docs_{self.user_id}"

#     def _check_index_exists(self, client: Elasticsearch, index_name: str) -> bool:
#         try:
#             return client.indices.exists(index=index_name)
#         except Exception as e:
#             logger.error(f"Error checking index existence: {str(e)}")
#             return False

#     def _run(self, query: str) -> str:
#         client = None
#         try:
#             client = Elasticsearch(self.es_url)
#             index_name = self._get_index_name()

#             if not self._check_index_exists(client, index_name):
#                 return (
#                     f"❌ No documents found for user ID {self.user_id}. "
#                     "Please upload and index documents first."
#                 )

#             query_vector = self.embeddings.embed_query(query)

#             if not query_vector:
#                 return "❌ Failed to generate embedding for the query."

#             logger.debug(f"🔍 Query vector length: {len(query_vector)}")

#             search_query = {
#                 "size": 5,
#                 "query": {
#                     "script_score": {
#                         "query": {
#                             "bool": {
#                                 "filter": [
#                                     {"term": {"metadata.user_id": self.user_id}}
#                                 ]
#                             }
#                         },
#                         "script": {
#                             "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
#                             "params": {"query_vector": query_vector}
#                         }
#                     }
#                 },
#                 "_source": ["page_content", "metadata"]
#             }

#             response = client.search(index=index_name, body=search_query)
#             hits = response["hits"]["hits"]

#             logger.debug(f"✅ Retrieved {len(hits)} matching documents")

#             if not hits:
#                 return "I couldn't find any relevant documents for your query."

#             results = []
#             for hit in hits:
#                 source = hit["_source"]
#                 score = hit["_score"]
#                 metadata = source.get("metadata", {})
#                 title = metadata.get("title", "Untitled Document")
#                 content = source.get("page_content", "")

#                 # Create snippet around query match or from start
#                 if query.lower() in content.lower():
#                     start = max(0, content.lower().find(query.lower()) - 200)
#                 else:
#                     start = 0
#                 end = min(len(content), start + 1000)
#                 snippet = content[start:end]

#                 results.append(
#                     f"📄 Document: {title}\n"
#                     f"🔢 Relevance Score: {score:.2f}\n"
#                     f"📚 Snippet:\n{snippet.strip()}"
#                 )

#             return "\n\n---\n\n".join(results)

#         except Exception as e:
#             logger.error(f"Search error: {str(e)}", exc_info=True)
#             return f"❌ Error during document retrieval: {str(e)}"
#         finally:
#             if client:
#                 client.close()



from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Optional
from elasticsearch import Elasticsearch
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging
import os

logger = logging.getLogger(__name__)

class VectorRetrieverToolSchema(BaseModel):
    query: str


class VectorRetrieverTool(BaseTool):
    name: str = "vector_retriever"
    description: str = "Use this tool to find documents related to a user's question from Elasticsearch."
    args_schema = VectorRetrieverToolSchema

    user_id: int
    embeddings: HuggingFaceEmbeddings
    es_url: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    def _get_index_name(self):
        return f"user_docs_{self.user_id}"

    def _check_index_exists(self, client: Elasticsearch, index_name: str) -> bool:
        return client.indices.exists(index=index_name)

    def _run(self, query: str) -> str:
        logger.info(f"🧠 VectorRetrieverTool triggered with query: {query}")
        
        client = None
        try:
            client = Elasticsearch(self.es_url)
            index_name = self._get_index_name()

            if not self._check_index_exists(client, index_name):
                return (
                    f"⚠️ No documents found for user ID {self.user_id}. "
                    f"Make sure documents are uploaded and indexed in `{index_name}`."
                )

            query_vector = self.embeddings.embed_query(query)

            if not query_vector or not isinstance(query_vector, list):
                return "⚠️ Failed to generate a valid embedding vector for the query."

            search_query = {
                "size": 10,
                "query": {
                    "script_score": {
                        "query": {
                            "bool": {
                                "filter": [
                                    {"term": {"user_id": self.user_id}}
                                ]
                            }
                        },
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                            "params": {"query_vector": query_vector}
                        }
                    }
                },
                "_source": ["page_content", "title", "user_id", "document_id"]
            }

            response = client.search(index=index_name, body=search_query)
            hits = response.get("hits", {}).get("hits", [])

            if not hits:
                return "❌ I could not find any relevant documents to answer your question."

            results = []
            for idx, hit in enumerate(hits):
                source = hit["_source"]
                score = hit.get("_score", 0)
                title = source.get("title", "Untitled Document")
                content = source.get("page_content", "").strip()

                if not content:
                    continue

                lower_content = content.lower()
                lower_query = query.lower()
                if lower_query in lower_content:
                    start = max(0, lower_content.find(lower_query) - 200)
                    end = min(len(content), start + 1000)
                    snippet = content[start:end]
                else:
                    snippet = content[:500]

                results.append(
                    f"📄 Document: {title}\n"
                    f"Relevance Score: {score:.2f}\n"
                    f"Content:\n{snippet}\n"
                )

            if not results:
                return "⚠️ Documents were found, but they seem to be empty or irrelevant."

            return (
                f"🔍 Here are the most relevant documents I found:\n\n" +
                "\n\n---\n\n".join(results) +
                f"\n\n🧠 These may help you answer your question about: **{query}**"
            )

        except Exception as e:
            logger.error(f"❌ Search error: {str(e)}", exc_info=True)
            return f"An error occurred while searching: {str(e)}"
        finally:
            if client:
                client.close()
