from langchain_community.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# langchain_ollama import OllamaLLM
import re
from datetime import datetime
import sys

# Path to your log file
LOG_FILE_PATH = "logs.txt"

# Function to parse log entries into structured format
def parse_log_entries(log_content):
  # Regular expression to parse log entries
  pattern = r'\[(.*?)\] (.*?) ([A-Z]+): (.*)'
  
  structured_logs = []
  
  for line in log_content.strip().split('\n'):
    match = re.match(pattern, line)
    if match:
        timestamp_str, service, level, message = match.groups()
        try:
          timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
          structured_logs.append({
            'timestamp': timestamp,
            'service': service,
            'level': level,
            'message': message,
            'original': line
          })
        except ValueError:
            print(f"Warning: Could not parse timestamp in line: {line}")
  
  return structured_logs

# Function to format logs for better context
def format_logs_for_context(structured_logs):
    formatted_logs = []
    
    for log in structured_logs:
      formatted_entry = f"Time: {log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
      formatted_entry += f"Service: {log['service']}\n"
      formatted_entry += f"Level: {log['level']}\n"
      formatted_entry += f"Message: {log['message']}\n"
      formatted_entry += "-" * 40
      
      formatted_logs.append(formatted_entry)
    
    return "\n".join(formatted_logs)

def main():
  # Read the log file
  with open(LOG_FILE_PATH, 'r') as file:
      log_content = file.read()
  
  # Parse the log entries
  structured_logs = parse_log_entries(log_content)
  
  # Format logs for better context
  formatted_logs = format_logs_for_context(structured_logs)
  
  # Initialize Ollama for embeddings and LLM
  embedding_model = OllamaEmbeddings(model="llama3")
  llm = Ollama(model="llama3", temperature=0)
  
  # Create vector store from the formatted logs
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  texts = text_splitter.split_text(formatted_logs)
  
  # Create the vector store
  vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_model)
  retriever = vectorstore.as_retriever()
  
  # Create a custom prompt template for log analysis
  template = """
  You are a log analysis assistant. Use the following pieces of log information to answer the user's question.
  If you don't know the answer, just say that you don't know, don't try to make up an answer.
  
  Log Context:
  {context}
  
  Question: {question}
  """
  
  PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
  )
  
  # Create the QA chain
  qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
  )
  
  # Interactive question loop
  print("Log Analyzer using Llama 3 (via Ollama)")
  print("Type 'exit' to quit\n")
  
  while True:
    question = input("\nQuestion about logs: ")
      
    if question.lower() == 'exit':
        print("Exiting...")
        break
    
    # Get the answer
    result = qa_chain({"query": question})
    print("\nAnswer:", result["result"])
  
if __name__ == "__main__":
  main()