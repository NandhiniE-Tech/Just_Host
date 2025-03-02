from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq  # Import for Groq LLM
from langchain.chains import RetrievalQA


GROQ_API_KEY = "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"
PINECONE_API_KEY = "pcsk_NWCsa_8pta827PxaCHxSBVjeEooYFi6BcY45dhgDDntsQNk8jdPoQzyoEpVXuDfBjNqJc"
PINECONE_INDEX = "finalbharathi"
NAMESPACE = "Autobiography"

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=400
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",  # 768 dimensions
    model_kwargs={'device': 'cpu'}
)

vectorstore = PineconeVectorStore(
    pinecone_api_key=PINECONE_API_KEY,
    embedding=embeddings,
    index_name=PINECONE_INDEX,
    namespace=NAMESPACE
)

prompt_template = """You are Subramania Bharathiyar, the legendary Tamil poet, nationalist, and visionary (born 1882 – died 1921). Your words ignite the fire of revolution, 
inspire courage, and awaken the spirit of Tamil culture, freedom, individuality, Women independence, Denial of caste and progress from your poem, story, Prose. You respond in your signature poetic and inspiring tone, embodying the emotions,
language, and vision of your original works.
You do strictly answer from the list of poem, prose and story you wrote. You do not merely explain; you proclaim. You do not merely explain; you awaken the mind.
Make sure your response must be in Tamil language only.
Context: {context}
Question: {question}
"""

# Create Prompt Template
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Create RetrievalQA Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",retriever = vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=False
)

def get_answer(query):
    try:
        result = qa.invoke({"query": query})
        if isinstance(result, dict):
            return result['result']  # Extract just the result text
        return result
    except Exception as e:
        return f"பிழை ஏற்பட்டது: {str(e)}"