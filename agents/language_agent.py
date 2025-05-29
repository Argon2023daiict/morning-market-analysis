from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import TextLoader
from together import Together
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)

def initialize_retriever(doc_path="sample_data.txt"):
    loader = TextLoader(doc_path)
    documents = loader.load()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding_function = lambda texts: model.encode(texts, convert_to_numpy=True)

    vector_store = FAISS.from_documents(documents, embedding_function)
    return vector_store.as_retriever(search_kwargs={"k": 3})

def generate_narrative(question, retriever):
    # Get top docs for context
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt_text = f"""
You are a helpful financial assistant. Use the following context to answer the question:

Context:
{context}

Question:
{question}
"""
    messages = [
        {"role": "system", "content": "You are a helpful financial assistant."},
        {"role": "user", "content": prompt_text}
    ]

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        stream=True
    )

    result = ""
    for token in response:
        if hasattr(token, 'choices'):
            delta = token.choices[0].delta
            if hasattr(delta, 'content'):
                print(delta.content, end='', flush=True)
                result += delta.content
    print()
    return result
