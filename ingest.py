from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from transformers import AutoTokenizer, AutoModel
import torch
import pinecone


GROQ_API_KEY = "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"
PINECONE_API_KEY = "pcsk_NWCsa_8pta827PxaCHxSBVjeEooYFi6BcY45dhgDDntsQNk8jdPoQzyoEpVXuDfBjNqJc"
PINECONE_INDEX = "finalbharathi"
NAMESPACE = "Autobiography" 

# Load in word format:
from langchain_community.document_loaders import Docx2txtLoader

loader = Docx2txtLoader(r"C:\Users\NANDHINI\Desktop\Love_of_Bharathiyar\Just_HOST\Tamilal.docx")
# Load the PDF file
#loader = PyPDFLoader(r"C:\Users\NANDHINI\Desktop\Love_of_Bharathiyar\Coding__BHarathi\Bharathi Tamil =50pg.pdf")
print("done with textloader", loader)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


docs = loader.load_and_split(text_splitter=text_splitter)

chunks = text_splitter.split_documents(docs)
for i, chunk in enumerate(chunks[:5]):  # Print first 5 chunks
    print(f"Chunk {i+1}: {len(chunk.page_content)} characters")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")# 768 dimensions)
#embeddings = PINECONE_API_KEY(embed={'model':"multilingual-e5-large"})
#embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#embeddings = co.embed(docs, input_type="search_document", model="embed-english-v3.0").embeddings
vectorstore = PineconeVectorStore(
    pinecone_api_key=PINECONE_API_KEY,   
    embedding=embeddings,
    index_name=PINECONE_INDEX,
    namespace=NAMESPACE
    )
vectorstore.add_documents(docs)
print("done")
