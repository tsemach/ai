## from: https://python.langchain.com/docs/tutorials/rag/

# create python env
python -m venv venv
source venv/bin/activate
pip install -r ...

## package to install
pip install --quiet --upgrade langchain-text-splitters langchain-community langgraph
pip install -qU "langchain[openai]"
pip install -qU langchain-core
