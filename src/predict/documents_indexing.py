import logging

from pathlib import Path

from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.vector_stores.pinecone import PineconeVectorStore

from pinecone import Pinecone, ServerlessSpec

from src.models.response import DocumentsIndexingResponse

import os
import sys

from src.settings import Settings

settings = Settings()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("doc_index")

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT_PATH, "data")


class DocumentsIndexing:
    """
    A class for indexing tutorials' documents for the help centre
    """

    def __init__(
        self,
    ):
        """
        Init method setting the class attribute
        """
        self.vector_index = None

    def index(self):
        """
        A method that prepares and stores the vector database of the documents
        or loads it if it has already been created
        """
        dir_name = f"data/vector_store"
        dir_path = os.path.join(ROOT_PATH, dir_name)
        print(dir_path)
        # load the vector index if it has already been created
        if Path(dir_path).exists():
            logger.info(
                "Found a previously created vector index, loading it. This can take a good few minutes..."
            )
            logger.info("Creating Pinecone index")
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            pinecone_index = pc.Index("quickstart")

            vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

            # rebuild storage context
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store, persist_dir=dir_path
            )

            # load index
            self.vector_index = load_index_from_storage(storage_context)
            logger.info("Vector index set up successfully!")
            return

        # create and store the vector index for future use
        else:
            Path(dir_path).mkdir(parents=True)

        logger.info(f"Loading data from {PATH}")
        # This returns a list of documents reading files from a local directory
        documents = SimpleDirectoryReader(PATH, recursive=True).load_data()
        for doc in documents:
            print(doc.metadata["file_path"])

        logger.info(f"Loaded {len(documents)} files")

        pc = Pinecone(api_key=settings.PINECONE_API_KEY)

        logger.info("Creating Pinecone index")

        # Try to create new index. If index already exist in the cloud, but not in
        # local directory, then delete index in cloud and re-creates it.
        try:
            pc.create_index(
                name="quickstart",
                dimension=1536,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        except:
            pc.delete_index(name="quickstart")
            pc.create_index(
                name="quickstart",
                dimension=1536,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        pinecone_index = pc.Index("quickstart")

        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        logger.info("Creating Vector index")

        # Default indexer. LlamaIndex uses text-embedding-ada-002 by default
        vector_index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )

        self.vector_index = vector_index

        # store the vector index for future use
        self.vector_index.storage_context.persist(persist_dir=dir_path)
        return

    def query(self, query: str, top_k: int = 5, similarity_cutoff: float = 0.4):
        """
        A method that takes in a query and returns an answer to the query based on the code
        """
        logger.info(f"Querying for: {query}")

        # configure retriever
        retriever = VectorIndexRetriever(
            index=self.vector_index,
            similarity_top_k=top_k,
        )
        # configure response synthesizer
        response_synthesizer = get_response_synthesizer()

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[
                SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)
            ],
        )

        # Query the llm and returns response.
        # Return an empty string if any error occurs.
        try:
            response = query_engine.query(query)
            logger.info(
                f"Response obtained from {len(response.source_nodes)} source nodes"
            )
            return response
        except:
            logger.info(f"No response obtained.")
            return ""

    def indexing_and_query(self, query: str) -> DocumentsIndexingResponse:
        self.index()
        return self.query(query)


if __name__ == "__main__":
    di = DocumentsIndexing()
    query = "Can I use Logic with the Multi-Question Page?"
    # query = "Can I add a score or create an outcome quiz with the Multi-Question Page?"
    # query = "Are there any limitations with translating large forms?"
    # query = "What language will my responses be shown in?"
    print(di.indexing_and_query(query).response)
