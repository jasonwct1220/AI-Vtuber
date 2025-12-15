import os
import chatgpt
from llama_cpp import Llama
llm = Llama(
      model_path="./llama-2-7b-chat.Q4_K_M.gguf",
      chat_format="llama-2",
      n_gpu_layers=-1,
)

prompt = chatgpt.prompt('prompt.txt')
def get():
    response = llm.create_chat_completion(
    messages = [
          {"role": "system", "content": "You will roleplay as a Twitch streamer called YURI. The user is a chat user that want to chit chat with you."},
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
