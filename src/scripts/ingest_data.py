import os

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma 

from typing import List, Generator
from concurrent.futures import ProcessPoolExecutor

from db.chroma_db import initialize_vector_db, load_vector_db

from utils.logger import get_logger

class DataOrchestrator:
    def __init__(self, folder_path: str = 'data/raw/'):
        self.folder_path = folder_path
        self.persists_dir = 'data/vectorstore'
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                       chunk_overlap=200, 
                                                       separators=["\n## ", "\n### ", "\n```", "\n\n", "\n", " ", ""])
        self.logger = get_logger("main")
        self.vector_db = None


    def _load_and_split_file(self, file_path: str) -> List[Document]:
        try:
            loader = UnstructuredMarkdownLoader(file_path)
            docs = loader.load_and_split(text_splitter=self.splitter)
            self.logger.info(f"Loaded and split file: {file_path}, {len(docs)} docs")
            return docs
        except Exception as e:
            self.logger.error(f"Failed to load/split file {file_path}: {e}")
            return []

    def _load_all_docs_parallel(self) -> Generator[Document, None, None]:
        file_paths = [f.path for f in os.scandir(self.folder_path) if f.is_file()]
        self.logger.info(f"Found files: {file_paths}")
        if not file_paths:
            self.logger.warning(f"No files found in {self.folder_path} for preprocessing.")
        self.logger.info(f"Starting parallel processing for {len(file_paths)} files...")
        with ProcessPoolExecutor() as executor:
            results = executor.map(self._load_and_split_file, file_paths)
        self.logger.info(f"Finished processing")
        for r in results:
            yield from r
            
    
    def get_db(self) -> Chroma:
        if self.vector_db:
            self.logger.info("Loading cached vector database instance")
            return self.vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 20})
        if os.path.exists(self.persists_dir) and os.listdir(self.persists_dir):
            self.logger.info(f"Found existing database at '{self.persists_dir}'.")
            self.vector_db = load_vector_db(self.persists_dir)
        else:
            self.logger.info(f"No database found at '{self.persists_dir}'. Initializing new one.")
            docs = []
            for i, doc in enumerate(self._load_all_docs_parallel(), start=1):
                if i % 400 == 0:
                    if self.vector_db is None:
                        self.vector_db = initialize_vector_db(docs)
                    else:
                        self.vector_db.add_documents(docs)
                    docs.clear()
                docs.append(doc)
            if docs:
                if self.vector_db is None:
                    self.vector_db = initialize_vector_db(docs)
                else:
                    self.vector_db.add_documents(docs)
        if self.vector_db is None:
            self.logger.error("Vector DB was not initialized. No documents were processed.")
            raise RuntimeError("Vector DB initialization failed: No documents processed.")
        return self.vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 20})