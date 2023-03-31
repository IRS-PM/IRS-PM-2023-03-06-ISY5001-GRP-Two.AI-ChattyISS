# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PJIQYPt3sD6-ZhcXcBxLJMOYwpkGQshQ
"""


# import streamlit as st
# from streamlit_chat import message



from langchain.embeddings.openai import OpenAIEmbeddings


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
from langchain.chains import ChatVectorDBChain
from langchain.embeddings.openai import OpenAIEmbeddings

import os
os.environ["OPENAI_API_KEY"] = "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"

"""Python file to serve as the frontend"""




def load_chain():
    """Logic for loading the chain you want to use should go here."""
    system_template = """Act like a question answering bot for a school. 
    Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, ask the user to rephrase the question based on the context given.

    {context}

    Question: {question}


    Answer in sentence and in full details where possible:"""
    
    messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    from langchain import FAISS

    embeddings = OpenAIEmbeddings()

    store = FAISS.load_local(os.getcwd() + "/NUS_ISS_chatbot/model3", embeddings)

    qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0, model_name = 'gpt-4'), vectorstore = store,qa_prompt=prompt
                                    ,top_k_docs_for_context = 10
                                    , return_source_documents = True
                                    )
    return qa



#start = True
#chat_history = []
#query = input("Hi I am NUS-ISS chatbot. Please ask me your query: ")
#next = query

#while start:
#  result = chain({"question": next, "chat_history": chat_history})
#  print("") 
#  print(result['answer'])
#  chat_history.append((next, result['answer']))
#  print("")
#  next = input("Please ask me your next question or type 'end' to end the bot: ")
#  if str.lower(next) == 'end':
#    print("")
#    print('Bye-bye')
#    start = False
#  else:
#    continue

