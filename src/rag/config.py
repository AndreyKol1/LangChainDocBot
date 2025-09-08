from rag.generator import initialize_model
from scripts.ingest_data import DataOrchestrator
from utils.logger import get_logger
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler
import cohere
import os

load_dotenv()
cohere_api = os.environ["COHERE_API"]
langfuse_handler = CallbackHandler()
llm = initialize_model()
data = DataOrchestrator()
retriever = data.get_db()
logger = get_logger("main")
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
co = cohere.ClientV2(api_key=cohere_api)