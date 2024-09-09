'''
Description: This script demonstrates how to use the RAG triad evaluation method.
It uses the BeyondLLM library to generate a response to a question and then e
valuates the response using the RAG triad evaluation method. It 
was a test to see if it would effectively evaluate our model. 

The source code is from:

'''

# Import modules
from beyondllm.source import fit
from beyondllm.embeddings import FastEmbedEmbeddings
from beyondllm.retrieve import auto_retriever
from beyondllm.llms import HuggingFaceHubModel
from beyondllm.generator import Generate

from dotenv import load_dotenv
import os

load_dotenv()

data = fit('before_and_after.txt', dtype='pdf')
embed_model = FastEmbedEmbeddings()
retriever = auto_retriever(data=data, embed_model=embed_model, type='normal', top_k=3)

llm = HuggingFaceHubModel(model='Ishreet1/FinanceLLM', token=os.getenv('HUGGINGFACE_ACCESS_TOKEN'))

pipeline = Generate(question='Explain the concept of buy and hold', llm=llm, retriever=retriever)

print(pipeline.call())
print(pipeline.get_rag_triad_evals())
