from retrieve_data import FetchFilesFromGitHub
from ingest_data import DataOrchestrator

fetcher = FetchFilesFromGitHub()
orchestrator = DataOrchestrator()

def main():
    fetcher.get_documents_from_github()
    orchestrator.populate_db()

if __name__ == "__main__":
    main()