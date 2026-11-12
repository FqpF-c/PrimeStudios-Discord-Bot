import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = 1570409938365452368

client = discord.Client(intents=discord.Intents.default())

DESIRED_ORDER = [
    "👑 Studio Founder",
    "🛠️ Studio Co-Owner",
    "💻 Lead Developer / Scripter",
    "🏗️ 3D Modeler & Builder",
    "🎨 UI & Graphic Designer",
    "🎵 Sound Designer",
    "🛡️ Senior Moderator",
    "⚔️ Moderator",
    "🧪 QA / Beta Tester",
    "⭐ Studio Sponsor / VIP",
    "📺 Creator / Streamer",
    "🎉 Events Host",
    "🤖 Bots & Webhooks",
    "🎮 Community Member",
    "🔇 Muted",
    "🦖 Dino Update Ping",
    "👀 Sneak Peeks Ping",
    "📢 Announcement Ping",
    "🎁 Giveaway Ping",
    "🎪 Event Ping",
]

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    print(f"Logged in as {client.user} in {guild.name}")
    print(f"Prime top role: '{guild.me.top_role.name}' (Pos: {guild.me.top_role.position})")

    # 1. Ensure all custom roles are hoisted (shown in server list)
    print("Updating hoist status for all custom roles...")
    for rname in DESIRED_ORDER:
        r = discord.utils.get(guild.roles, name=rname)
        if r and not r.managed:
            # We want all display roles hoisted
            if not r.hoist and "Ping" not in rname:
                try:
                    await r.edit(hoist=True, reason="Show role name in server member list")
                    print(f"Set hoist=True for '{r.name}'")
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"Error hoisting {r.name}: {e}")

    # 2. Reorder positions
    # In Discord, higher position number = higher in hierarchy = shows higher in member list
    # Prime is at position 23. The highest position we can assign is 22.
    print("\nCalculating and applying new role positions...")
    positions = {}
    base_pos = 22
    for i, rname in enumerate(DESIRED_ORDER):
        r = discord.utils.get(guild.roles, name=rname)
        if r and not r.managed:
            target_pos = base_pos - i
            positions[r] = target_pos
            print(f"Assigning '{r.name}' -> Target Pos: {target_pos}")

    try:
        await guild.edit_role_positions(positions=positions)
        print("Successfully reordered role hierarchy via guild.edit_role_positions!")
    except Exception as e:
        print(f"edit_role_positions error: {e}")

    # 3. Assign roles to remaining members (Dyno, lolicat, Sunflake, NPC)
    print("\nChecking remaining members without roles...")
    bot_role = discord.utils.get(guild.roles, name="🤖 Bots & Webhooks")
    member_role = discord.utils.get(guild.roles, name="🎮 Community Member")

    # Audit log scan for all members
    member_ids = set()
    try:
        async for entry in guild.audit_logs(limit=100):
            if entry.user:
                member_ids.add(entry.user.id)
            if entry.target and hasattr(entry.target, "id"):
                member_ids.add(entry.target.id)
    except Exception as e:
        print(f"Audit log error: {e}")

    for uid in member_ids:
        try:
            m = await guild.fetch_member(uid)
            if m.id == guild.owner_id:
                continue
            if m.bot:
                if bot_role and bot_role not in m.roles:
                    await m.add_roles(bot_role, reason="Assign bot role")
                    print(f"Assigned Bots & Webhooks to: {m.name}")
            else:
                if member_role and member_role not in m.roles:
                    await m.add_roles(member_role, reason="Assign Community Member")
                    print(f"Assigned Community Member to: {m.name}")
        except Exception:
            pass

    print("\nRole hierarchy rearrangement and member assignment complete!")
    await client.close()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
