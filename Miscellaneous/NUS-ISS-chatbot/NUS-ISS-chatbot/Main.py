# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PJIQYPt3sD6-ZhcXcBxLJMOYwpkGQshQ
"""


# import streamlit as st
# from streamlit_chat import message



from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

import faiss
import pickle
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from datetime import date
import os
import time

#os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

"""Python file to serve as the frontend"""
today = date.today()

tday_test = "{Today's date is " + str(today.strftime("%B %d, %Y")) + ")" 
def load_chain():
    """Logic for loading the chain you want to use should go here."""
    system_template = """Act like a question answering bot for a school, noting that today is"""
    system_template = system_template + str(today.strftime("%B %d, %Y")) + "." 
    system_template = system_template + """
    Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, ask the user to rephrase the question based on the context given.
   
    {context}

    Question: {question}


    Answer in sentence and in full details where possible. """
    
    
    
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    from langchain import FAISS

    embeddings = OpenAIEmbeddings()
    print ("Using 3.5")
    store = FAISS.load_local("./gpt3.5_small_model", embeddings)
    
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages = False)

    # qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0), store.as_retriever(),condense_question_prompt=prompt,  memory = memory)
    qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0), vectorstore = store,qa_prompt=prompt
                                    ,top_k_docs_for_context = 1
                                    , return_source_documents = True
                                    )
    return qa

chain = load_chain()


start = True
chat_history = []
query = input("Hi I am NUS-ISS chatbot. Please ask me your query: ")
next = query

while start:
  start = time.time()

  result = chain({"question": next, "chat_history": chat_history})
  end = time.time()
  total_time = end - start

  print("Execution Time: " , total_time, "s")
  print("") 
  print(result['answer'])
  
  chat_history.append((next, result['answer']))
  print("")
  next = input("Please ask me your next question or type 'end' to end the bot: ")
  if str.lower(next) == 'end':
    print("")
    print('Bye-bye')
    start = False
  else:
    continue
