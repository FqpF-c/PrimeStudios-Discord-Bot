import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1570409938365452368

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    print(f"Logged in as {client.user} in {guild.name}")
    print(f"Guild Owner ID: {guild.owner_id}")
    
    prime_member = guild.me
    print(f"Prime's top role: {prime_member.top_role.name} (Position: {prime_member.top_role.position})")

    # Get target roles
    founder_role = discord.utils.get(guild.roles, name="👑 Studio Founder")
    member_role = discord.utils.get(guild.roles, name="🎮 Community Member")
    bot_role = discord.utils.get(guild.roles, name="🤖 Bots & Webhooks")
    
    print(f"Found roles -> Founder: {founder_role}, Member: {member_role}, Bot: {bot_role}")

    # Fetch all members via REST
    try:
        raw_members = await client.http.get_members(guild.id, 1000, 0)
        print(f"Fetched {len(raw_members)} members from Discord REST API.")
    except Exception as e:
        print(f"Error fetching members: {e}")
        raw_members = []

    # Assign roles
    for mdata in raw_members:
        u = mdata["user"]
        uid = int(u["id"])
        is_bot = u.get("bot", False)
        username = u["username"]
        
        try:
            member = await guild.fetch_member(uid)
        except Exception as e:
            print(f"Could not fetch member {username} ({uid}): {e}")
            continue

        if uid == guild.owner_id:
            print(f"Assigning Studio Founder to Owner: {username}")
            if founder_role:
                try:
                    await member.add_roles(founder_role, reason="Assign Owner highest role")
                    print(f"Successfully assigned {founder_role.name} to {username}")
                except Exception as e:
                    print(f"Failed to add Founder role to owner: {e}")
        elif is_bot:
            print(f"Assigning Bots & Webhooks to bot: {username}")
            if bot_role:
                try:
                    await member.add_roles(bot_role, reason="Assign Bot role")
                    print(f"Successfully assigned {bot_role.name} to {username}")
                except Exception as e:
                    print(f"Failed to add Bot role to {username}: {e}")
        else:
            print(f"Assigning Community Member to user: {username}")
            if member_role:
                try:
                    await member.add_roles(member_role, reason="Assign default Community Member auto-role")
                    print(f"Successfully assigned {member_role.name} to {username}")
                except Exception as e:
                    print(f"Failed to add Community Member to {username}: {e}")

    # Attempt to delete old custom roles
    old_role_names = ["One Above All", "High Tier God", "Bots", "Human"]
    for rname in old_role_names:
        r = discord.utils.get(guild.roles, name=rname)
        if r:
            print(f"Attempting to delete role: '{r.name}' (Pos: {r.position})")
            if r.position >= prime_member.top_role.position:
                print(f"CANNOT delete '{r.name}': Role position ({r.position}) is higher than Prime's top role ({prime_member.top_role.position})!")
            else:
                try:
                    await r.delete(reason="Deleting old redundant role")
                    print(f"Deleted old role '{r.name}' successfully!")
                except Exception as e:
                    print(f"Failed to delete '{r.name}': {e}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
