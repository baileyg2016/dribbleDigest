from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import os
from dotenv import load_dotenv
import json
from article import Article

load_dotenv()

# Load the JSON data
with open('samples/sample-articles.json', 'r') as f:
  data = json.load(f)

# Create Article objects
articles = [Article(**article) for article in data]


documents = [
  Document(
    page_content=str(article),
    metadata=article.to_dict()
  )
  for article in articles
]

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

def find_best_articles(prompts):
  interesting_articles = {}
  for prompt in prompts:
    docs = vectorstore.similarity_search(prompt, k=5)
    interesting_articles[prompt] = [doc.metadata for doc in docs]
  return interesting_articles

prompts = ['NBA', 'New York Yankees']
interesting_articles = find_best_articles(prompts)



print(interesting_articles)