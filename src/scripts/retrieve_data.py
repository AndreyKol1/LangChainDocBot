import requests
import shutil
import os
import time
import gzip

from utils.logger import get_logger

from dotenv import load_dotenv

load_dotenv()


output_dir = "data/raw"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class FetchFilesFromGitHub:
    def __init__(self, api_url: str = "https://api.github.com/repos/langchain-ai/langchain/contents/docs/docs"):
        self.logger = get_logger("main")
        self.github_token = os.environ["GITHUB_TOKEN"]
        self.api_url = api_url

        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Python Script",
            "Authorization": f"token {self.github_token}"
        }
    def _download_file(self, item: dict) -> None:
        """Downloads a file from a given GitHub API item dictionary"""
        file_url = item['download_url']
        file_name = item['name']

        self.logger.info(f"Downloading {file_name}...")

        try:
            file_response = requests.get(file_url, stream=True, headers=self.headers)
            time.sleep(0.1)

            if file_response.status_code == 200:
                file_path = os.path.join(output_dir, file_name)

                if 'Content-Encoding' in file_response.headers and 'gzip' in file_response.headers['Content-Encoding']:
                    self.logger.info(f"Decompressing {file_name}...")
                    with gzip.GzipFile(fileobj=file_response.raw) as decompressed_file:
                        with open(file_path, 'wb') as f_out:
                            shutil.copyfileobj(decompressed_file, f_out)
                else:
                    with open(file_path, 'wb') as f:
                            shutil.copyfileobj(file_response.raw, f)
                            
                self.logger.info(f"Downloaded {file_name} successfully.")
            else:
                self.logger.warning(f"Error downloading {file_name}. Status code {file_response.status_code}")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {file_name}: {e}")

    def _fetch_and_download(self, current_url: str) -> None:
        """Utility function to recursively fetch and download files."""
        try:
            response = requests.get(current_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()

                for item in data:
                    if item['type'] == 'file' and item['name'].endswith('.mdx'):
                        self._download_file(item)
                    
                    elif item['type'] == 'dir':
                        dir_name = item['name']
                        dir_url = f"{current_url}/{dir_name}"
                        self.logger.info(f"Attempting to download files from directory '{dir_name}'")
                        self._fetch_and_download(dir_url)

            else:
                self.logger.warning(f"Error: Unable to fetch file list. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failder for {current_url}: {e}")

    def get_documents_from_github(self) -> None:
        """Initiates the recursive fetching and downloading process."""
        self.logger.info("Starting file download process.")
        self._fetch_and_download(current_url=self.api_url)
        self.logger.info("File download process completed")


            