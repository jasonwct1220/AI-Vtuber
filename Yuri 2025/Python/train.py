import json
prompt = ""
with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()

jsonl_data = [
      #{"messages": [{"role": "system", "content": prompt}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]},
      #{"messages": [{"role": "system", "content": prompt}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?"}]},
      #{"messages": [{"role": "system", "content": prompt}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters."}]}
      ]
print("########################################\n")
print("AI Vtuber Fine Tune data input software\n")
print("########################################")
while True:
      x = input("Input + to create a new conversation. Input $ to save the file.\n")
      if x == "+":
            l = [{"role": "system", "content": prompt}]
            print("Input ! to stop the conversation")
            while True:
                  q = input("Question: ")
                  if q == "!":
                        break
                  r = input("Response: ")
                  l.append({"role": "user", "content": q})
                  l.append({"role": "assistant", "content": r})
            jsonl_data.append({"messages": l},)
      if x == "$":
            break
      

with open('fuga.jsonl', 'w+') as f:
    data = [json.loads(l) for l in f.readlines()]
    data += jsonl_data
    f.writelines([json.dumps(l)+"\n" for l in data])