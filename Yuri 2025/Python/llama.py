import os
import chatgpt
from llama_cpp import Llama
llm = Llama(
      model_path="./llama-2-7b-chat.Q4_K_M.gguf",
      chat_format="llama-2",
      n_gpu_layers=-1,
)

prompt = chatgpt.prompt('prompt.txt')
def llama2():
    response = llm.create_chat_completion(
    messages = [
          {"role": "system", "content": prompt},
          {
              "role": "user",
              "content": "Hi!"
          }
      ],
      temperature=0.9,
        max_tokens=256,
        frequency_penalty=2,
        presence_penalty=2
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(get())
