import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="notion_pages",
    embedding_function=embedding_fn)


def build_index(pages):
    documents = []
    metadatas = []
    ids = []

    for page in pages:
        content = f"{page['title']} {page['content']}"
        if not content.strip():
            continue
        documents.append(content)
        metadatas.append({"title": page["title"], "id": page["id"]})
        ids.append(page["id"])

    collection.add(documents=documents, metadatas=metadatas, ids=ids)


def retrieve_context(query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)

    context = ""
    for i, doc in enumerate(results["documents"][0]):
        title = results["metadatas"][0][i]["title"]
        context += f"[{title}]: {doc[:300]}\n"

    return context.strip()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    from notion_fetcher import fetch_pages, fetch_page_content

    pages = fetch_pages()
    for page in pages:
        page["content"] = fetch_page_content(page["id"])
        
    build_index(pages)
    print(f"Indexed {len(pages)} pages")

    query = "interview confirmation from Stripe"
    context = retrieve_context(query)
    print(f"\nContext for '{query}':")
    print(context)