from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Initialize Flask and load environment variables
app = Flask(__name__)
load_dotenv()

# Load the same embedding model used during indexing
embeddings = download_hugging_face_embeddings()
# Connect to the persisted ChromaDB using those embeddings
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
# Create a retriever that fetches the top 3 most relevant chunks
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Initialize the Groq LLM with Llama 3.1
import os
groq_api_key = os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4, api_key=groq_api_key)

# Build the prompt template with system prompt, chat history, and user input
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Chain 1: takes retrieved docs + prompt and sends to the LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
# Chain 2: retrieves docs first, then passes them to chain 1
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# In-memory store for chat histories (one per session)
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # Create a new history if this session hasn't been seen before
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# Wrap the RAG chain with message history support
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)
# Route: serve the chat page
@app.route("/")
def index():
    return render_template("chat.html")


# Route: handle chat messages via POST
@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    response = conversational_rag_chain.invoke(
        {"input": msg},
        config={"configurable": {"session_id": "mother_user_1"}},
    )
    return jsonify({"response": response["answer"]})


if __name__ == "__main__":
    import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)), debug=False)