from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_chroma import Chroma

extracted_data = load_pdf("data/")
print(f"Documents loaded: {len(extracted_data)}")  # Should be > 0

text_chunks = text_split(extracted_data)
print(f"Text chunks created: {len(text_chunks)}")  # Should be > 0

# If either is 0, the problem is your PDF!
if len(text_chunks) == 0:
    print("ERROR: No text chunks found. Check your PDF has selectable text.")
else:
    embeddings = download_hugging_face_embeddings()
    print("Building your free local database... Please wait.")
    db = Chroma.from_documents(text_chunks, embeddings, persist_directory="./chroma_db")
    print(f"Local Database successfully built! {len(text_chunks)} chunks indexed.")