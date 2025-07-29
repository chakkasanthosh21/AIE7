# ✅ Clean install from GitHub - the working version
# !pip uninstall -y ragas
# !pip install git+https://github.com/explodinggradients/ragas.git@main

# ✅ STEP 1: Imports
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    AnswerRelevancy,
    Faithfulness,
    ContextPrecision,
    ContextRecall
)

import pandas as pd
import os

# ✅ Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"  # Replace with your key

# ✅ STEP 2: Write sample text file
sample_text = """
Dengue fever is a mosquito-borne tropical disease caused by the dengue virus.
Symptoms typically begin three to fourteen days after infection. They include high fever,
headache, vomiting, muscle and joint pains, and a characteristic skin rash.
In severe cases, it can lead to bleeding, low platelet count, and blood plasma leakage.
There is no specific antiviral treatment for dengue; supportive care is recommended.
"""
with open("sample.txt", "w") as f:
    f.write(sample_text)

# ✅ STEP 3: Load and split documents
docs = TextLoader("sample.txt").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = splitter.split_documents(docs)

# ✅ STEP 4: Create golden dataset (Q/A/Context aligned)
contexts = [
    "Dengue fever is a mosquito-borne tropical disease caused by the dengue virus.",
    "Symptoms typically begin three to fourteen days after infection.",
    "They include high fever, headache, vomiting, muscle and joint pains, and a characteristic skin rash.",
    "In severe cases, it can lead to bleeding, low platelet count, and blood plasma leakage.",
    "There is no specific antiviral treatment for dengue; supportive care is recommended."
]

questions = [
    "What causes dengue fever?",
    "How soon do symptoms appear?",
    "What are common symptoms of dengue?",
    "What complications can dengue cause?",
    "Is there any antiviral treatment for dengue?"
]

answers = [
    "dengue virus",
    "three to fourteen days",
    "high fever, headache, vomiting, muscle and joint pains, and a characteristic skin rash",
    "bleeding, low platelet count, and blood plasma leakage",
    "no specific antiviral treatment"
]

golden_dataset = Dataset.from_dict({
    "question": questions,
    "reference": answers,  # Rename 'answer' to 'reference' for Ragas compatibility
    "context": contexts
})

# ✅ STEP 5: Build vectorstore retriever
embedding = OpenAIEmbeddings()
faiss_vectorstore = FAISS.from_documents(splits, embedding)
retriever = faiss_vectorstore.as_retriever()

# ✅ STEP 6: Create QA chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# ✅ STEP 7: Instantiate metrics and evaluator LLM
from ragas.llms import LangchainLLMWrapper

# Metric objects
metrics = [
    AnswerRelevancy(),
    Faithfulness(),
    ContextPrecision(),
    ContextRecall()
]

# Create evaluator LLM wrapper
evaluator_llm = LangchainLLMWrapper(llm)

# ✅ STEP 8: Run the QA chain on our dataset to get responses and contexts
responses = []
retrieved_contexts = []

for question in golden_dataset["question"]:
    response = qa_chain.invoke({"query": question})
    responses.append(response["result"])
    
    # Get the retrieved documents from the retriever
    retrieved_docs = retriever.get_relevant_documents(question)
    retrieved_contexts.append([doc.page_content for doc in retrieved_docs])

# Add responses and contexts to the dataset
golden_dataset = golden_dataset.add_column("response", responses)
golden_dataset = golden_dataset.add_column("retrieved_contexts", retrieved_contexts)

# ✅ STEP 9: Evaluate using Ragas
results = evaluate(
    dataset=golden_dataset,
    metrics=metrics,
    llm=evaluator_llm
)

# ✅ STEP 9: Display evaluation results
results_df = results.to_pandas()
print(results_df) 