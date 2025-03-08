import os
import warnings
import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Suppress warnings
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in the .env file.")
os.environ['OPENAI_API_KEY'] = openai_api_key

# Model settings
MODEL = 'gpt-3.5-turbo'

# Initialize conversation components
def process_pdf(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    return vectorstore

def chat(pdf, message, history):
    if pdf is None:
        return "Please upload a PDF file."
    vectorstore = process_pdf(pdf)
    llm = ChatOpenAI(temperature=0.7, model_name=MODEL, openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)
    result = conversation_chain.invoke({"question": message})
    return result["answer"]

# Create Gradio interface
demo = gr.Interface(
    fn=chat,
    inputs=[gr.File(label="Upload PDF"), gr.Textbox(label="Ask a question")],
    outputs=gr.Textbox(label="Answer"),
    title="PDF Chatbot",
    allow_flagging="never"
)

demo.launch(share=True)
