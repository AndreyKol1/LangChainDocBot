from langfuse import Langfuse


from dotenv import load_dotenv

import os

load_dotenv()

pk = os.environ["LANGFUSE_PUBLIC_KEY"]
sk = os.environ["LANGFUSE_SECRET_KEY"]

def tracing_setup():
    langfuse = Langfuse(
        public_key=pk,
        secret_key=sk,
        host="https://cloud.langfuse.com"
    )

    langfuse

