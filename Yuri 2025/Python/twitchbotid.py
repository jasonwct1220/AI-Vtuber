import asyncio
import twitchio
import keys

async def main() -> None:
    async with twitchio.Client(client_id=keys.TWITCH_CLIENT_ID, client_secret=keys.TWITCH_CLIENT_SECRET) as client:
        await client.login()
        user = await client.fetch_users(logins=["your Twitch user name"])
        for u in user:
            print(f"User: {u.name} - ID: {u.id}")

if __name__ == "__main__":
    asyncio.run(main())