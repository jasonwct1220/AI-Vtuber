import os
import chatgpt
from llama_cpp import Llama

llm = Llama(
      model_path="./gemma-2b.gguf",
      chat_format="llama-2",
      n_gpu_layers=-1,
)
#os.system('cls')
prompt = chatgpt.prompt('prompt.txt')
response = llm.create_chat_completion(
      messages = [
          {"role": "system", "content": "You are a helpful assistant."},
          {
              "role": "user",
              "content": "Hi!"
          }
      ]
)
print(response)