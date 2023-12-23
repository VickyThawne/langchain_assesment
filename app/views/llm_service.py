from json_file_processor import JsonFileProcessor
from openapi import get_response_from_query
import textwrap
import json

def process_request(request,embeddings,chat):
    try:
        doc_file_path, question_file_path = prepare_file_path(request)
        if doc_file_path is None or question_file_path is None:
            return "Internal Server Error"

        json_llm = JsonFileProcessor()
        documents = json_llm.document_loader(doc_file_path)
        if documents is None:
            return "Internal Server Error"

        docs = json_llm.text_splitter(documents)
        if docs is None:
            return "Internal Server Error"

        db = json_llm.prepare_vectordb(docs,embeddings)
        if db is None:
            return "Internal Server Error"

        dict = {}
        with open(question_file_path) as data_file:
            data = json.load(data_file)
            for item in data:
                query = item["question"]
                response, docs = get_response_from_query(db, query, chat)
                curated_response = textwrap.fill(response, width=50)
                dict[item["question"]] = curated_response
        return dict
    except Exception as e:
        print("Something went wrong while performing 'Document Loader' operations", e)


def prepare_file_path(request):
    try:
        doc_file = request.files['doc_file']
        question_file = request.files['question_file']
        base_path = '/home/archit/Documents/workspace/langchain_assesment/app/data/uploads/'
        doc_file_path = base_path + doc_file.filename
        question_file_path = base_path + question_file.filename
        # Save the files to a specific location
        doc_file.save(doc_file_path)
        question_file.save(question_file_path)
        return doc_file_path, question_file_path
    except Exception as e:
        print("Something went wrong while performing 'prepare_file_path' operations", e)

