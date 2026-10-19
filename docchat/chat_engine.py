import logging
from pathlib import Path

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class ChatEngine:
    def __init__(self, docs, api_key):
        if not docs:
            raise ValueError("Upload at least one PDF or TXT document.")
        if not api_key or not api_key.strip():
            raise ValueError("Enter an OpenAI API key.")

        chatbot = ChatOpenAI(temperature=0, openai_api_key=api_key)
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)

        documents = self.load_documents(docs)

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=40)
        documents = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 2}
        )
        self.qa = ConversationalRetrievalChain.from_llm(chatbot, retriever)

    @staticmethod
    def load_documents(docs):
        documents = []
        for doc in docs:
            path = Path(getattr(doc, "name", doc))
            if not path.is_file():
                raise ValueError(f"Uploaded document does not exist: {path.name}")
            if path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(path))
            elif path.suffix.lower() == ".txt":
                loader = TextLoader(str(path))
            else:
                raise ValueError("Only PDF and TXT documents are supported.")
            documents.extend(loader.load())

        if not documents:
            raise ValueError("No readable content was found in the uploaded documents.")

        num_docs = len(documents)
        num_chars = sum([len(document.page_content) for document in documents])

        LOGGER.debug(f"You have {num_docs} document(s) in your document(s)")
        LOGGER.debug(f"There are {num_chars} characters in your document(s)")

        return documents

    def run(self, query, chat_history):
        result = self.qa({"question": query, "chat_history": chat_history})
        return result["answer"]
