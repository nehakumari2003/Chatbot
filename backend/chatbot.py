import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Set up the LLM using ChatGroq
llm = ChatGroq(
    temperature=0.2,
    model_name="llama3-8b-8192",
    api_key=groq_api_key
)

# Load QA chain for context-based answers
qa_chain = load_qa_chain(llm, chain_type="stuff")

# Global variables to store PDF context and status
pdf_text = []
pdf_uploaded = False

def update_pdf_text(file_path):
    global pdf_text, pdf_uploaded
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        pdf_text = text_splitter.split_documents(pages)
        pdf_uploaded = True
    except Exception as e:
        print(f"❌ Failed to process PDF: {e}")
        pdf_text = []
        pdf_uploaded = False

def reset_pdf_context():
    global pdf_text, pdf_uploaded
    pdf_text = []
    pdf_uploaded = False

    # Delete all uploaded PDF files (optional but recommended)
    folder = 'uploaded_pdfs'
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"⚠️ Could not delete {file_path}: {e}")

def clean_response(text):
    if not text:
        return ""
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', str(text))
    cleaned = cleaned.replace('\n', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def ask_question(query):
    try:
        if pdf_uploaded and pdf_text:
            answer = qa_chain.run(input_documents=pdf_text, question=query)
            return clean_response(answer) if answer else "🤖 Neo couldn't find an answer. Try rephrasing your question."
        else:
            response = llm.invoke(query)
            content = response.content if hasattr(response, "content") else response
            return clean_response(content)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
