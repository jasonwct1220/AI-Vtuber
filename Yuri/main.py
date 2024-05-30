import pickle
import random
from datetime import datetime, timezone
import twitchio
from twitchio.ext import commands
from twitchio import Message, Channel

import socket
import sys

import tcp
import chatgpt
import googletts
import keys

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
host = IPAddr
port = 5065
address = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4, SOCK_STREAM as Stream socket for tcp/ip


# Import the prompt and a conversation example in the message

messages=[
    {
      "role": "system",
      "content": chatgpt.prompt('prompt.txt')
    },
    {
      "role": "user",
      "content": "hi"
    },
    {
      "role": "assistant",
      "content": "Hey chat! I'm YURI, and welcome to the stream! How's your day going?"
    }
  ]


# Setup the Twitch bot. Reference:(https://twitchio.dev/en/stable/quickstart.htm)
class Bot(commands.Bot):
    
    #Create the txp tunnel
    tunnel = tcp.TCP()

    # Initialise the bot with access token, prefix and channel.
    def __init__(self):
      super().__init__(
            token=keys.TWITCH_TOKEN, 
            prefix='!', 
            initial_channels=[keys.TWITCH_CHANNEL])
      #sock.connect(address)
      #print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(port))
      
    
    
    
    async def event_ready(self):
        # Send login user and id in console.
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        print('---------------------------------------')
        # Tell the chatroom the bot has started up
        channel = bot.get_channel(keys.TWITCH_CHANNEL)
        #await channel.send(f"yuri-chan has started up!")
  

    async def event_message(self, message: Message):
        # Ignore message from bot itself
        if message.echo:
            return
        
        # Check if it is a command
        if message.content[0] != '!':
        # Print the message to the console
          chat = message.content
          print(chat)
        # Append the input chat into the messages list
          messages.append(
            {"role": "user", "content": chat}
          )
        # Check if he is subscriber and pass the messages list to the GPT model
          if message.author.is_subscriber is True:
             reply = chatgpt.gpt4(messages)
          else:
             reply = chatgpt.gpt(messages)
        # Ouput the reply in the console
          print(reply)
          print('---------------------------------------')

        # Extract the emotion from the reply
          emotion = reply[reply.find("[")+1 : reply.find("]")]
          response = reply[reply.find("]")+1 :]
      
        # Output the reply to output.txt
          with open('output.txt', 'w') as f:
            caption = response
            words = caption.split()
            if(len(words)>8):
               i = 0
               while i < len(words):
                  i += 8
                  words.insert(i,"\n")
            caption = ""
            for word in words:
               caption += word + " "
            caption = caption[:len(caption)-2]
            f.write(caption)

        # Append the output back into the messages list
          messages.append(
              {"role": "assistant", "content": reply}
          )

        # Print out the response in the chatroom
          channel = bot.get_channel(keys.TWITCH_CHANNEL)
          #await channel.send(response)
        
        # Trigger the emotion animation and the text to speech
          self.tunnel.emotion(emotion)
          googletts.tts(response)
        
          

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        else:
          await self.handle_commands(message)

    async def event_raw_usernotice(self, channel: Channel, tags: dict):
      message = ""
      subid = 0
      match tags["msg-id"]:
         case "sub":
          message = tags["display-name"] + ", Thank you for subbing the channel!"
          subid = tags["user-id"]
         case "resub":
          message = tags["display-name"] + ", Thank you for the continuous support!"
         case "subgift":
          message = tags["display-name"] + ", Thank you for the gift sub!"
          subid = tags["msg-param-recipient-id"]
      googletts.tts(message)
      sub = []
      with open('subscriber.pkl','wb+') as f:
         sub = pickle.load(f)
         if subid not in sub:
            sub.append(subid)
      f.close()
       
    @commands.command()
    async def uptime(self, ctx: commands.Context):
      stream = await Bot.fetch_streams(self,user_ids=[self.user_id])
      start = stream[0].started_at
      now = datetime.now(timezone.utc)
      diff = now - start
      await ctx.send(f'The stream uptime is: {diff.days * 24 + diff.seconds // 3600} hours {(diff.seconds % 3600) // 60} minutes {diff.seconds % 60} seconds.')

    @commands.command()
    async def followers(self, ctx: commands.Context):
		  # Use get_followers to get how many following
      user = Bot.create_user(self,self.user_id,self.nick)
      count = await user.fetch_channel_follower_count()
      await ctx.send(f"There are currently {count} followers.")       

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        match random.randint(1,3):
          case 1:
            await ctx.send(f'Hello, {ctx.author.name}! Glad to have you here. Enjoy the stream!!')
          case 2:
            await ctx.send(f'Hey, {ctx.author.name}! Time to kick back, relax, and let the good times roll. Welcome!')
          case 3:
            await ctx.send(f'Hey, {ctx.author.name}! Brace yourself for an amazing time filled with fun and excitement!')
        
    @commands.command()
    async def cry(self, ctx : commands.Context):
       #if(ctx.author.is_subscriber):
          print("Crying ;-;")
          self.tunnel.cry()

    @commands.command()
    async def blush(self, ctx : commands.Context):
       #if(ctx.author.is_subscriber):
          print("Blushed ///")
          self.tunnel.blush()
          

    @commands.command()
    async def test(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send("Yuri is running!")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

# Main program

if __name__ == "__main__":
  print("##AI Vtuber initiated##")

  # Start the bot and infinitely read messages
  bot = Bot()
  bot.run()
  with open('output.txt', 'w') as f:
    f.truncate(0)