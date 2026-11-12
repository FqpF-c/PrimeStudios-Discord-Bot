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
    print(f"Logged in to {guild.name}")
    
    # 1. Gather all member information
    member_ids = set()
    try:
        async for entry in guild.audit_logs(limit=100):
            if entry.user:
                member_ids.add(entry.user.id)
            if entry.target and hasattr(entry.target, "id"):
                member_ids.add(entry.target.id)
    except Exception as e:
        print(f"Audit log error: {e}")

    bots_count = 0
    humans_count = 0
    for uid in member_ids:
        try:
            m = await guild.fetch_member(uid)
            if m.bot:
                bots_count += 1
            else:
                humans_count += 1
        except Exception:
            pass

    # Include guild member count if higher
    total_count = guild.member_count or (bots_count + humans_count)
    if total_count > (bots_count + humans_count):
        # Adjust humans if guild.member_count reflects total
        humans_count = total_count - bots_count

    print(f"Stats -> Total: {total_count} | Humans: {humans_count} | Bots: {bots_count}")

    # 2. Check if SERVER STATS category already exists
    cat = discord.utils.get(guild.categories, name="📊 SERVER STATS 📊")
    everyone_role = guild.default_role
    
    locked_overwrites = {
        everyone_role: discord.PermissionOverwrite(
            view_channel=True,
            connect=False,  # Padlock icon
            speak=False
        )
    }

    if not cat:
        # Create category at the very top (position 0)
        cat = await guild.create_category(
            name="📊 SERVER STATS 📊",
            position=0,
            overwrites=locked_overwrites,
            reason="Server Stats counter setup"
        )
        print("Created 📊 SERVER STATS 📊 category at top!")
    else:
        await cat.edit(position=0)

    # 3. Create or update the 3 locked voice channels
    stat_configs = [
        (f"🏆 All Members: {total_count}", "All Members"),
        (f"⭐ Members: {humans_count}", "Members:"),
        (f"👾 Bots: {bots_count}", "Bots:"),
    ]

    for ch_name, identifier in stat_configs:
        existing_ch = next((c for c in cat.voice_channels if identifier in c.name), None)
        if existing_ch:
            await existing_ch.edit(name=ch_name, overwrites=locked_overwrites)
            print(f"Updated channel: {ch_name}")
        else:
            await guild.create_voice_channel(
                name=ch_name,
                category=cat,
                overwrites=locked_overwrites,
                reason="Server Stats counter"
            )
            print(f"Created channel: {ch_name}")
        await asyncio.sleep(0.5)

    print("Server stats channels created and positioned at the top!")
    await client.close()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
