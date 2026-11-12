import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1570409938365452368

intents = discord.Intents.default()
# Note: if privileged members intent is not enabled, guild.fetch_members still works via chunk/REST if allowed or we can fetch members
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    print(f"Guild: {guild.name} (Owner ID: {guild.owner_id})")

    print("\n--- ROLES LIST ---")
    for r in reversed(guild.roles):
        print(f"ID: {r.id} | Name: '{r.name}' | Managed: {r.managed} | Default: {r.is_default()}")

    print("\n--- MEMBERS LIST ---")
    try:
        async for m in guild.fetch_members(limit=100):
            r_names = [r.name for r in m.roles if not r.is_default()]
            print(f"ID: {m.id} | Name: {m.name} | Bot: {m.bot} | Roles: {r_names}")
    except Exception as e:
        print(f"fetch_members error: {e}")
        for m in guild.members:
            r_names = [r.name for r in m.roles if not r.is_default()]
            print(f"ID: {m.id} | Name: {m.name} | Bot: {m.bot} | Roles: {r_names}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
