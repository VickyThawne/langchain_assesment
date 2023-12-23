from langchain.callbacks import get_openai_callback

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain

from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import textwrap
import pickle
import faiss
from langchain.vectorstores import FAISS


from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()


def create_db(embeddings):

    file_path = "../data/sample.json"
    
    # loader = DirectoryLoader("./data", glob="./*.pdf", loader_cls=PyPDFLoader)
    # loader = PyPDFLoader( file_path=file_path)
        # text_content=False)
    # if
    # {
    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.',
        text_content=False)
# }
    # else
    # pdf_file = "/content/the-memoirs-of-sherlock-holmes-001-adventure-1-silver-blaze.pdf"

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    vector_db = FAISS.from_documents(docs, embeddings)
    return vector_db


def get_response_from_query(db, query, model, depth=4):

    # retriever = db.as_retriever(search_kwargs={"k": depth})


    docs = db.similarity_search(query, k=depth)
    docs_page_content = " ".join([d.page_content for d in docs])

    # Template to use for the system message prompt
    template = """
        You are a helpful assistant that that can answer questions from the given context: {context}
        
        Only use the factual information from the context to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # Human question prompt
    human_template = "Answer the following question: {question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=model, prompt=chat_prompt)

    response = chain.run(question=query, context=docs_page_content)
    response = response.replace("\n", "")
    return response, docs

with get_openai_callback() as cb:
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
    db = create_db(embeddings)

    # query = "Please specify the primary data center location/region of the underlying cloud infrastructure used to host the service(s) as well as the backup location(s)."
    query = "Does Company have a Network Diagram?"
    response, docs = get_response_from_query(db, query, chat)
    print(textwrap.fill(response, width=50))

    print('='*50+"token usage"+ "="*50)
    print(cb)