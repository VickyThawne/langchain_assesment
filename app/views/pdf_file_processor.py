from langchain.document_loaders import PyPDFLoader
# class PdfFileProcessor(LlmInterface):
#     @abstractmethod
#     def document_loader(self):
#         loader = PyPDFLoader( file_path=file_path)
#         # text_content=False)
#         documents = loader.load()
#         return documents
#
#     @abstractmethod
#     def text_splitter(self):
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
#         docs = text_splitter.split_documents(documents)
#         return docs
#     @abstractmethod
#     def prepare_vectordb(self):
#         vector_db = FAISS.from_documents(docs, embeddings)
#         return vector_db
