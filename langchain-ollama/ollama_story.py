from ollama import LLM
# Load the Llama 2 model
model = LLM("llama2")
# Generate text based on a prompt
prompt = "Write a short story about a curious robot exploring a new planet."
output = model.generate(prompt)
print(output)