import os
import shutil
import logging
from typing import List

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


class RAGSystemService:

    def __init__(self):

        # ----------------------------
        # Logger
        # ----------------------------

        self.logger = logging.getLogger("RAGSystem")

        if not self.logger.handlers:

            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s | %(levelname)s | %(message)s"
            )

        # ----------------------------
        # Paths
        # ----------------------------

        self.batch_folder = "App/storage/batches"

        self.persist_directory = "App/vectorstore/chroma"

        os.makedirs(
            self.batch_folder,
            exist_ok=True
        )

        os.makedirs(
            self.persist_directory,
            exist_ok=True
        )

        # ----------------------------
        # Gemini Embeddings
        # ----------------------------

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        # ----------------------------
        # ChromaDB
        # ----------------------------

        self.vector_store = Chroma(
            collection_name="candidate_batches",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        self.logger.info(
            "RAG System Initialized Successfully"
        )

    # ============================================================
    # Load Batch Document
    # ============================================================

    def load_batch_document(
        self,
        batch_id: int
    ) -> str:

        file_path = os.path.join(
            self.batch_folder,
            f"batch_{batch_id:03d}.txt"
        )

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"Batch file not found : {file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        self.logger.info(
            f"Loaded Batch {batch_id}"
        )

        return text

    # ============================================================
    # Create Chunks
    # ============================================================

    def create_chunks(
        self,
        text: str
    ) -> List[str]:

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=1200,

            chunk_overlap=200,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        chunks = splitter.split_text(text)

        self.logger.info(
            f"Created {len(chunks)} chunks"
        )

        return chunks

    # ============================================================
    # Create LangChain Documents
    # ============================================================

    def create_documents(
        self,
        chunks: List[str],
        batch_id: int
    ) -> List[Document]:

        documents = []

        for index, chunk in enumerate(chunks):

            document = Document(

                page_content=chunk,

                metadata={

                    "batch_id": batch_id,

                    "chunk_id": index + 1
                }
            )

            documents.append(document)

        self.logger.info(
            f"Created {len(documents)} LangChain Documents"
        )

        return documents

# ============================================================
# Build Batch
# ============================================================

    def build_batch(
        self,
        batch_id: int
    ) -> bool:

        self.logger.info(
            f"Building Batch {batch_id}"
        )

        text = self.load_batch_document(
            batch_id
        )

        chunks = self.create_chunks(
            text
        )

        documents = self.create_documents(
            chunks,
            batch_id
        )

        try:

            self.logger.info(
                "Adding documents to Chroma..."
            )

            self.vector_store.add_documents(
                documents=documents
            )

            self.logger.info(
                "Documents added successfully."
            )

            self.logger.info(
                f"Batch {batch_id} Indexed Successfully"
            )

            self.logger.info(
                f"Total vectors : {self.total_vectors()}"
            )

            return True

        except Exception as e:

            self.logger.exception(
                f"Failed to build batch {batch_id}"
            )

            raise e

    # ============================================================
    # Delete Batch
    # ============================================================

    def delete_batch(
        self,
        batch_id: int
    ) -> bool:

        self.logger.info(
            f"Deleting Batch {batch_id}"
        )

        try:

            results = self.vector_store.get(
                where={
                    "batch_id": batch_id
                }
            )

            ids = results.get(
                "ids",
                []
            )

            if len(ids) == 0:

                self.logger.info(
                    "No vectors found."
                )

                return True

            self.vector_store.delete(
                ids=ids
            )

            self.logger.info(
                f"Deleted {len(ids)} vectors."
            )

            return True

        except Exception as e:

            self.logger.exception(
                "Delete Batch Failed"
            )

            raise e

    # ============================================================
    # Rebuild Batch
    # ============================================================

    def rebuild_batch(
        self,
        batch_id: int
    ) -> bool:

        self.logger.info(
            f"Rebuilding Batch {batch_id}"
        )

        self.delete_batch(
            batch_id
        )

        self.build_batch(
            batch_id
        )

        self.logger.info(
            f"Batch {batch_id} Rebuilt Successfully"
        )

        return True

# ============================================================
    # Similarity Search
# ============================================================

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        batch_id: int | None = None
    ):

        self.logger.info(
            f"Running similarity search : {query}"
        )

        try:

            if batch_id is None:

                results = self.vector_store.similarity_search(
                    query=query,
                    k=k
                )

            else:

                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter={
                        "batch_id": batch_id
                    }
                )

            self.logger.info(
                f"Retrieved {len(results)} documents"
            )

            return results

        except Exception as e:

            self.logger.exception(
                "Similarity Search Failed"
            )

            raise e

    # ============================================================
    # Similarity Search With Scores
    # ============================================================

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5
    ):

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k
        )

    # ============================================================
    # Retriever
    # ============================================================

    def get_retriever(
        self,
        k: int = 5
    ):

        return self.vector_store.as_retriever(

            search_type="similarity",

            search_kwargs={
                "k": k
            }
        )

    # ============================================================
    # Total Vectors
    # ============================================================

    def total_vectors(self):

        try:

            data = self.vector_store.get()

            return len(
                data.get(
                    "ids",
                    []
                )
            )

        except Exception:

            return 0

    # ============================================================
    # Delete Entire Vector Store (Utility)
    # ============================================================

    def clear_vector_store(self):

        self.logger.info(
            "Clearing ChromaDB..."
        )

        if os.path.exists(
            self.persist_directory
        ):

            shutil.rmtree(
                self.persist_directory
            )

        os.makedirs(
            self.persist_directory,
            exist_ok=True
        )

        self.vector_store = Chroma(
            collection_name="candidate_batches",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        self.logger.info(
            "Vector Store Cleared Successfully"
        )

    # ============================================================
    # Health Check
    # ============================================================

    def health_check(self):

        return {
            "batch_folder": self.batch_folder,
            "vector_store": self.persist_directory,
            "total_vectors": self.total_vectors()
        }