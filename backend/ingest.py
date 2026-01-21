from sentence_transformers import SentenceTransformer
import faiss, os, pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(path="documents"):
    texts = []
    for file in os.listdir(path):
        with open(f"{path}/{file}", encoding="utf-8") as f:
            texts.extend(f.read().split("\n\n"))
    return texts

def create_vector_store():
    docs = load_documents()
    embeddings = model.encode(docs)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "vector_store/index.faiss")
    pickle.dump(docs, open("vector_store/docs.pkl", "wb"))

create_vector_store()
