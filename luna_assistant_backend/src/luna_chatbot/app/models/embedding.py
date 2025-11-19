from langchain_openai import OpenAIEmbeddings

# load env here to give the embedding tool access to the api key while embedding
from dotenv import load_dotenv

load_dotenv()

basic_embedding = OpenAIEmbeddings(model="text-embedding-3-small")
