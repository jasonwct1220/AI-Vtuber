import asyncio
import logging
import random
from typing import TYPE_CHECKING

import asqlite

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

import socket
import sys
from datetime import datetime, timezone

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

if TYPE_CHECKING:
    import sqlite3


LOGGER: logging.Logger = logging.getLogger("Bot")

# Consider using a .env or another form of Configuration file!
CLIENT_ID: str = "..."  # The CLIENT ID from the Twitch Dev Console
CLIENT_SECRET: str = "..."  # The CLIENT SECRET from the Twitch Dev Console
BOT_ID = "..."  # The Account ID of the bot user...
OWNER_ID = "..."  # Your personal User ID..


class Bot(commands.AutoBot):
    
    #Create the tcp tunnel
    tunnel = tcp.TCP()
    
    def __init__(self, *, token_database: asqlite.Pool, subs: list[eventsub.SubscriptionPayload]) -> None:
        self.token_database = token_database

        super().__init__(
            client_id=keys.TWITCH_CLIENT_ID,
            client_secret=keys.TWITCH_CLIENT_SECRET,
            bot_id=keys.TWITCH_BOT_ID,
            #owner_id=OWNER_ID,
            prefix="!",
            subscriptions=subs,
            force_subscribe=True,
        )

    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.add_component(MyComponent(self))

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        '''if payload.user_id == self.bot_id:
            # We usually don't want subscribe to events on the bots channel...
            return'''

        # A list of subscriptions we would like to make to the newly authorized channel...
        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(broadcaster_user_id=payload.user_id, user_id=self.bot_id),
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        if resp.errors:
            LOGGER.warning("Failed to subscribe to: %r, for user: %s", resp.errors, payload.user_id)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)
        print(f'Logged in as | {self.user.name}')
        print(f'User id is | {self.user.id}')
        print(f'Bot id is | {self.bot_id}')
        print(f'Owner id is | {self.owner_id}')
        print('---------------------------------------')

class MyComponent(commands.Component):
    # An example of a Component with some simple commands and listeners
    # You can use Components within modules for a more organized codebase and hot-reloading.

    def __init__(self, bot: Bot) -> None:
        # Passing args is not required...
        # We pass bot here as an example...
        self.bot = bot

    # An example of listening to an event
    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")
        
        user = self.bot.create_partialuser(user_id=self.bot.bot_id)
        #await user.send_message(sender=self.bot.user, message="Hello World!")

        if payload.chatter.id == self.bot.user.id:
            return
        
        if payload.text.startswith('!') is False:
            # Print the message to the console
            chat = payload.text
            print(chat)
            # Append the input chat into the messages list
            messages.append(
                {"role": "user", "content": chat}
            )

            # Ouput the reply in the console
            reply = chatgpt.gpt4(messages)
            print(reply)
            print('---------------------------------------')

            # Extract the emotion from the reply
            emotion = reply[reply.find("[")+1 : reply.find("]")]
            response = reply[reply.find("]")+1 :]
        
            # Output the reply to output.txt
            with open('output.txt', 'w', encoding='utf-8') as f:
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
            await user.send_message(sender=self.bot.user, message=response)
            #await channel.send(response)
            
            # Trigger the emotion animation and the text to speech
            #self.bot.tunnel.emotion(emotion)
            mp3path = googletts.tts(response)
            #duration = googletts.getMp3Length()
            self.bot.tunnel.send_to_Unity(emotion, mp3path)

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        """Command that replies to the invoker with Hi <name>!

        !hi
        """
        await ctx.reply(f"Hi {ctx.chatter}!")

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str) -> None:
        """Command which repeats what the invoker sends.

        !say <message>
        """
        await ctx.send(message)

    @commands.command()
    async def add(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which adds to integers together.

        !add <number> <number>
        """
        await ctx.reply(f"{left} + {right} = {left + right}")

    @commands.command()
    async def choice(self, ctx: commands.Context, *choices: str) -> None:
        """Command which takes in an arbitrary amount of choices and randomly chooses one.

        !choice <choice_1> <choice_2> <choice_3> ...
        """
        await ctx.reply(f"You provided {len(choices)} choices, I choose: {random.choice(choices)}")

    @commands.command(aliases=["thanks", "thank"])
    async def give(self, ctx: commands.Context, user: twitchio.User, amount: int, *, message: str | None = None) -> None:
        """A more advanced example of a command which has makes use of the powerful argument parsing, argument converters and
        aliases.

        The first argument will be attempted to be converted to a User.
        The second argument will be converted to an integer if possible.
        The third argument is optional and will consume the reast of the message.

        !give <@user|user_name> <number> [message]
        !thank <@user|user_name> <number> [message]
        !thanks <@user|user_name> <number> [message]
        """
        msg = f"with message: {message}" if message else ""
        await ctx.send(f"{ctx.chatter.mention} gave {amount} thanks to {user.mention} {msg}")

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        """Group command for our social links.

        !socials
        """
        await ctx.send("discord.gg/..., youtube.com/..., twitch.tv/...")

    @socials.command(name="discord")
    async def socials_discord(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our discord invite.

        !socials discord
        """
        await ctx.send("discord.gg/...")

    #to Live2D command
    '''@commands.command()
    async def uptime(self, ctx: commands.Context):
      stream = await Bot.fetch_streams(self,user_ids=[self.user.id])
      start = stream[0].started_at
      now = datetime.now(timezone.utc)
      diff = now - start
      await ctx.send(f'The stream uptime is: {diff.days * 24 + diff.seconds // 3600} hours {(diff.seconds % 3600) // 60} minutes {diff.seconds % 60} seconds.')

    @commands.command()
    async def followers(self, ctx: commands.Context):
		  # Use get_followers to get how many following
      user = Bot.create_user(self,self.user_id,self.nick)
      count = await user.fetch_channel_follower_count()
      await ctx.send(f"There are currently {count} followers.")       '''

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
          self.bot.tunnel.cry()

    @commands.command()
    async def blush(self, ctx : commands.Context):
       #if(ctx.author.is_subscriber):
          print("Blushed ///")
          self.bot.tunnel.blush()
          

    @commands.command()
    async def test(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send("Yuri is running!")

    '''@commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')'''

async def setup_database(db: asqlite.Pool) -> tuple[list[tuple[str, str]], list[eventsub.SubscriptionPayload]]:
    # Create our token table, if it doesn't exist..
    # You should add the created files to .gitignore or potentially store them somewhere safer
    # This is just for example purposes...

    query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
    async with db.acquire() as connection:
        await connection.execute(query)

        # Fetch any existing tokens...
        rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        tokens: list[tuple[str, str]] = []
        subs: list[eventsub.SubscriptionPayload] = []

        for row in rows:
            tokens.append((row["token"], row["refresh"]))

            if row["user_id"] == BOT_ID:
                continue

            subs.extend([eventsub.ChatMessageSubscription(broadcaster_user_id=row["user_id"], user_id=BOT_ID)])

    return tokens, subs


# Our main entry point for our Bot
# Best to setup_logging here, before anything starts
def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb:
            tokens, subs = await setup_database(tdb)

            async with Bot(token_database=tdb, subs=subs) as bot:
                for pair in tokens:
                    await bot.add_token(*pair)

                await bot.start(load_tokens=False)

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()