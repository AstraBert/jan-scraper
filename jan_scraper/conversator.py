from models_source import choose_right_model
from anylang import TranslateFunctions
from transformers import AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
import torch
import subprocess as sp
import pyautogui
import time
import os
import sys
import json
import random


def generate_id():
    """
    Generates a random 26-character alphanumeric ID.

    Returns:
        str: The generated ID.
    """
    idx = []
    for i in range(13):
        idx.append(str(random.randint(0, 9)))
    alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    for i in range(13):
        idx.append(alphabet[random.randint(0, len(alphabet) - 1)].upper())
    random.shuffle(idx)
    return "".join(idx)


def create_a_persistent_db(pdfpath) -> None:
    """
    Creates a persistent database from a PDF file.

    Args:
        pdfpath (str): The path to the PDF file.
    """
    print("Started the operation...", file=sys.stderr)
    a = time.time()
    loader = PyPDFLoader(pdfpath)
    documents = loader.load()

    # Split the documents into smaller chunks for processing
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Use HuggingFace embeddings for transforming text into numerical vectors
    embeddings = HuggingFaceEmbeddings()
    store = LocalFileStore(
        os.path.join(
            os.path.dirname(pdfpath), os.path.basename(pdfpath).split(".")[0] + "_cache"
        )
    )
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embeddings,
        document_embedding_cache=store,
        namespace=os.path.basename(pdfpath).split(".")[0],
    )

    b = time.time()
    print(
        f"Embeddings successfully created and stored at {os.path.join(os.path.dirname(pdfpath), os.path.basename(pdfpath).split('.')[0]+'_cache')} under namespace: {os.path.basename(pdfpath).split('.')[0]}"
    )
    print(f"To load and embed, it took: {b - a}")

    persist_directory = os.path.join(
        os.path.dirname(pdfpath), os.path.basename(pdfpath).split(".")[0] + "_localDB"
    )
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=cached_embeddings,
        persist_directory=persist_directory,
    )
    c = time.time()
    print(
        f"Persistent database successfully created and stored at {os.path.join(os.path.dirname(pdfpath), os.path.basename(pdfpath).split('.')[0] + '_localDB')}"
    )
    print(f"To create a persistent database, it took: {c - b}", file=sys.stderr)


def jan_chatting(
    jan_app_path,
    jan_data_folder,
    thread_id,
    hfmodel,
    model_task,
    persistent_db_dir,
    embeddings_cache,
    pdfpath,
):
    """
    Implements a chat system using the Jan app, Hugging Face models, and a persistent database.

    Args:
        jan_app_path (str): Path to the Jan app executable.
        jan_data_folder (str): Folder containing Jan app data.
        thread_id (str): ID of the chat thread.
        hfmodel (str): Hugging Face model identifier.
        model_task (str): Task for the Hugging Face model.
        persistent_db_dir (str): Directory for the persistent database.
        embeddings_cache (str): Path to cache Hugging Face embeddings.
        pdfpath (str): Path to the PDF file.

    Raises:
        KeyboardInterrupt: Raised if the user interrupts the chat.
    """
    modelclass = choose_right_model(hfmodel, model_task)
    embeddings = HuggingFaceEmbeddings()
    store = LocalFileStore(embeddings_cache)
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embeddings,
        document_embedding_cache=store,
        namespace=os.path.basename(pdfpath).split(".")[0],
    )
    vectordb = Chroma(
        persist_directory=persistent_db_dir, embedding_function=cached_embeddings
    )
    model_id = hfmodel
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = modelclass.from_pretrained(
        model_id,
        trust_remote_code=True,
        ignore_mismatched_sizes=True,
    )
    pipe = pipeline(model_task, model=model, tokenizer=tokenizer)

    local_llm = HuggingFacePipeline(pipeline=pipe)
    llm_chain = ConversationalRetrievalChain.from_llm(
        llm=local_llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=False,
    )
    pyautogui.alert(text="We will now open Jan", title="Launching Jan", button="OK")
    sp.Popen(jan_app_path)
    file_to_scrape = os.path.join(
        jan_data_folder, "threads/" + thread_id + "/messages.jsonl"
    )
    try:
        lastlines = []
        while True:
            fp = open(file_to_scrape)
            lines = fp.readlines()
            fp.close()
            if len(lines) > 0 and lines[0] != "\n" and lines[0] != "":
                lastline = json.loads(lines[len(lines) - 1])
                lastlines.append(lastline)
                if lastline["role"] == "assistant" and (
                    len(lastlines) == 0 or lastlines[0] == lastline
                ):
                    lastlines.pop()
                    time.sleep(1)
                    continue
                elif lastline["role"] == "assistant" and not (
                    len(lastlines) == 0 or lastlines[0] == lastline
                ):
                    lastlines.remove(lastlines[0])
                    query_from_user = json.loads(lines[len(lines) - 2])
                    txt = TranslateFunctions(
                        query_from_user["content"][0]["text"]["value"], destination="en"
                    )
                    query = txt.translatef()
                    rst = llm_chain({"question": query, "chat_history": []})
                    re = TranslateFunctions(
                        rst["answer"].replace("\n", " "), destination=txt.original
                    )
                    response = re.translatef()
                    creat_time = time.time()
                    ftw = open(file_to_scrape, "a")
                    ftw.write(
                        '{"id":"'
                        + str(generate_id())
                        + '","thread_id":"'
                        + thread_id
                        + '","role":"assistant",'
                        '"content":[{"type":"text","text":{"value":"'
                        + hfmodel
                        + " says: "
                        + response
                        + '","annotations":[]}}],"status":"ready","created":'
                        + str(creat_time)
                        + ',"updated":'
                        + str(time.time())
                        + ',"object":"thread.message"}\n'
                    )
                    ftw.close()
                    time.sleep(1)
                    pyautogui.alert(
                        text="Page will be refreshed now",
                        title="Refreshing",
                        button="OK",
                    )
                    pyautogui.hotkey("ctrl", "r")
                    continue
                elif lastline["role"] == "user":
                    lastlines.pop()
                    query_from_user = lastline
                    txt = TranslateFunctions(
                        query_from_user["content"][0]["text"]["value"], destination="en"
                    )
                    query = txt.translatef()
                    rst = llm_chain({"question": query, "chat_history": []})
                    re = TranslateFunctions(
                        rst["answer"].replace("\n", " "), destination=txt.original
                    )
                    response = re.translatef()
                    creat_time = time.time()
                    ftw = open(file_to_scrape, "a")
                    ftw.write(
                        '{"id":"'
                        + str(generate_id())
                        + '","thread_id":"'
                        + thread_id
                        + '","role":"assistant","content":[{"type":"text","text":{"value":"'
                        + hfmodel
                        + " says: "
                        + response
                        + '","annotations":[]}}],"status":"ready","created":'
                        + str(creat_time)
                        + ',"updated":'
                        + str(time.time())
                        + ',"object":"thread.message"}\n'
                    )
                    ftw.close()
                    time.sleep(1)
                    pyautogui.alert(
                        text="Page will be refreshed now",
                        title="Refreshing",
                        button="OK",
                    )
                    pyautogui.hotkey("ctrl", "r")
                    continue
            else:
                time.sleep(1)
                continue
    except KeyboardInterrupt:
        sys.exit(0)
