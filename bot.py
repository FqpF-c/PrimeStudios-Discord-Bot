"""
Discord Server Setup & Architect Bot.
Automates complete server provisioning: roles, categories, channels, permissions,
welcome embeds, bot invitation links, and manual configuration checklists.
"""

import os
import sys
import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import web

from templates import TEMPLATES, RECOMMENDED_BOTS, MANUAL_ACTIONS_GUIDE

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("DiscordSetupBot")

# Lightweight web server to satisfy cloud health checks (Render, Koyeb, etc.)
async def handle_health_check(request):
    user_str = str(bot.user) if bot.user else "Connecting..."
    latency_ms = round(bot.latency * 1000) if bot.latency else 0
    guilds_count = len(bot.guilds)
    text = (
        f"🟢 Prime Studios Discord Bot is ONLINE 24/7!\n"
        f"Bot: {user_str}\n"
        f"Connected Guilds: {guilds_count}\n"
        f"Gateway Latency: {latency_ms}ms\n"
    )
    return web.Response(text=text, status=200)

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle_health_check)
    app.router.add_get("/health", handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Web health check server running on port {port}")


# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # Optional: For instant guild-specific slash command sync

# Configure intents
# We use default intents so the bot can connect immediately without requiring Privileged Intents.
# Slash commands (/setup, /bot_invites, /manual_guide) work 100% without privileged intents.
intents = discord.Intents.default()


bot = commands.Bot(command_prefix="!", intents=intents)


def is_admin_or_owner(member: discord.Member) -> bool:
    """Check if member is guild owner or has administrator permission."""
    return member.guild.owner_id == member.id or member.guild_permissions.administrator


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    # Generate bot invite URL with Admin permissions (permissions=8)
    invite_url = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=True),
        scopes=["bot", "applications.commands"]
    )
    logger.info("=" * 60)
    logger.info(f"Bot is ready! Invite your bot with this link:")
    logger.info(f"{invite_url}")
    logger.info("=" * 60)

    # Sync slash commands
    try:
        if GUILD_ID:
            guild_obj = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild_obj)
            synced = await bot.tree.sync(guild=guild_obj)
            logger.info(f"Synced {len(synced)} slash commands to guild {GUILD_ID}")
        else:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} global slash commands")
    except Exception as e:
        logger.error(f"Error syncing slash commands: {e}")

    # Start health check web server for Render / Cloud hosting
    try:
        await run_web_server()
    except Exception as e:
        logger.warning(f"Could not start web server: {e}")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="server setup | /setup or !setup"
        )
    )


# ==========================================
# CORE SERVER PROVISIONING ENGINE
# ==========================================

async def execute_server_setup(guild: discord.Guild, preset: str, clean_old: bool, progress_callback):
    """
    Creates roles, categories, channels, permissions, and welcome embeds.
    """
    if preset not in TEMPLATES:
        raise ValueError(f"Unknown preset '{preset}'. Available: {', '.join(TEMPLATES.keys())}")

    template = TEMPLATES[preset]

    # Verify bot permissions
    me = guild.me
    if not me.guild_permissions.administrator:
        raise PermissionError("The bot requires Administrator permissions to set up roles and channels!")

    await progress_callback(f"🚀 Starting setup using **{template['name']}** preset...")

    # 1. Clean existing channels if requested
    if clean_old:
        await progress_callback("🧹 Cleaning up existing channels...")
        for channel in list(guild.channels):
            try:
                await channel.delete(reason="Server setup cleanup")
                await asyncio.sleep(0.3)
            except Exception as e:
                logger.warning(f"Could not delete channel {channel.name}: {e}")

    # 2. Create Roles
    await progress_callback("👑 Creating and configuring server roles...")
    created_roles = {}
    existing_roles = {role.name.lower(): role for role in guild.roles}

    for role_info in reversed(template["roles"]):
        role_name = role_info["name"]
        color = role_info["color"]
        hoist = role_info["hoist"]
        mentionable = role_info["mentionable"]
        perms = role_info["permissions"]

        if role_name.lower() in existing_roles:
            role_obj = existing_roles[role_name.lower()]
            try:
                await role_obj.edit(
                    color=color,
                    hoist=hoist,
                    mentionable=mentionable,
                    permissions=perms,
                    reason="Server setup role update"
                )
            except Exception as e:
                logger.warning(f"Failed to edit existing role {role_name}: {e}")
        else:
            try:
                role_obj = await guild.create_role(
                    name=role_name,
                    color=color,
                    hoist=hoist,
                    mentionable=mentionable,
                    permissions=perms,
                    reason="Server setup role creation"
                )
            except Exception as e:
                logger.error(f"Failed to create role {role_name}: {e}")
                continue

        created_roles[role_name] = role_obj
        await asyncio.sleep(0.3)

    # Find staff roles for permissions
    admin_role = next((r for name, r in created_roles.items() if "admin" in name.lower()), None)
    mod_role = next((r for name, r in created_roles.items() if "mod" in name.lower()), None)
    bot_role = next((r for name, r in created_roles.items() if "bot" in name.lower()), None)

    # 3. Create Categories and Channels
    await progress_callback("📁 Constructing categories, channels, and security overrides...")
    everyone_role = guild.default_role
    welcome_channel = None
    rules_channel = None
    staff_channel = None

    for cat_data in template["categories"]:
        cat_name = cat_data["name"]
        is_staff_only = cat_data.get("staff_only", False)

        # Build category permission overwrites
        cat_overwrites = {
            everyone_role: discord.PermissionOverwrite(
                view_channel=not is_staff_only,
                send_messages=not is_staff_only,
                read_message_history=True,
                connect=not is_staff_only
            )
        }

        if is_staff_only:
            if admin_role:
                cat_overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True)
            if mod_role:
                cat_overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True)
            if bot_role:
                cat_overwrites[bot_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        category = await guild.create_category(name=cat_name, overwrites=cat_overwrites, reason="Server setup")
        await asyncio.sleep(0.4)

        for chan_data in cat_data["channels"]:
            ch_name = chan_data["name"]
            ch_type = chan_data["type"]
            ch_topic = chan_data.get("topic", "")
            is_read_only = chan_data.get("read_only", False)
            user_limit = chan_data.get("user_limit", 0)

            channel_overwrites = dict(cat_overwrites)
            if is_read_only:
                channel_overwrites[everyone_role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=False,
                    add_reactions=True,
                    read_message_history=True
                )
                if admin_role:
                    channel_overwrites[admin_role] = discord.PermissionOverwrite(send_messages=True, manage_messages=True)
                if mod_role:
                    channel_overwrites[mod_role] = discord.PermissionOverwrite(send_messages=True, manage_messages=True)

            if ch_type == "text":
                ch_obj = await guild.create_text_channel(
                    name=ch_name,
                    category=category,
                    topic=ch_topic,
                    overwrites=channel_overwrites,
                    reason="Server setup"
                )
                if "welcome" in ch_name:
                    welcome_channel = ch_obj
                elif "rules" in ch_name:
                    rules_channel = ch_obj
                elif "staff-chat" in ch_name or "admin-chat" in ch_name:
                    staff_channel = ch_obj

            elif ch_type == "voice":
                await guild.create_voice_channel(
                    name=ch_name,
                    category=category,
                    user_limit=user_limit,
                    overwrites=channel_overwrites,
                    reason="Server setup"
                )

            await asyncio.sleep(0.4)

    # 4. Post Welcome & Rules Embeds
    if rules_channel:
        rules_embed = discord.Embed(
            title=f"📜 Welcome to {guild.name} — Rules & Guidelines",
            description="Please read through the rules below to keep our community safe and enjoyable for everyone!",
            color=discord.Color.blue()
        )
        rules_embed.add_field(name="1. Be Respectful", value="Treat all members with respect. Harassment, discrimination, or hate speech will result in an immediate ban.", inline=False)
        rules_embed.add_field(name="2. No Spam or Self-Promotion", value="Keep links and promotional material to designated channels only. Do not DM members with unsolicited invites.", inline=False)
        rules_embed.add_field(name="3. Keep Channels on Topic", value="Use appropriate channels for discussions, memes, bot commands, and media.", inline=False)
        rules_embed.add_field(name="4. Follow Discord Community Guidelines", value="All members must adhere to the official [Discord Terms of Service](https://discord.com/terms).", inline=False)
        rules_embed.set_footer(text=f"{guild.name} • Setup Bot", icon_url=guild.icon.url if guild.icon else None)
        await rules_channel.send(embed=rules_embed)

    if welcome_channel:
        welcome_embed = discord.Embed(
            title=f"🎉 Welcome to {guild.name}!",
            description=(
                f"We are excited to have you here! 🎉\n\n"
                f"👉 Make sure to check out {rules_channel.mention if rules_channel else '#rules'}.\n"
                f"👉 Hop into our general chat and say hi!\n"
                f"👉 Enjoy your stay!"
            ),
            color=discord.Color.green()
        )
        await welcome_channel.send(embed=welcome_embed)

    # 5. Post Bot Invites and Manual Setup Guides to Staff Channel
    target_report_channel = staff_channel or welcome_channel
    if target_report_channel:
        # Bot Invites Embed
        bot_embed = build_bot_invites_embed()
        await target_report_channel.send(embed=bot_embed)

        # Manual Action Guides
        for guide in MANUAL_ACTIONS_GUIDE:
            g_embed = discord.Embed(
                title=guide["title"],
                description="\n".join([f"• {s}" for s in guide["steps"]]),
                color=discord.Color.orange()
            )
            await target_report_channel.send(embed=g_embed)
            await asyncio.sleep(0.3)

    await progress_callback(f"✅ **Server setup complete!** Channels, roles, rules, and admin guides have been posted to {target_report_channel.mention if target_report_channel else 'your server'}.")


def build_bot_invites_embed() -> discord.Embed:
    """Generate rich embed with 1-click bot invite links."""
    embed = discord.Embed(
        title="🤖 Recommended Discord Bot Invites (1-Click Links)",
        description=(
            "**⚠️ Note on Discord API Limits:**\n"
            "Discord **does not allow** bots to add or invite other bots programmatically for security reasons.\n"
            "As an administrator, click the links below to invite these trusted bots to your server:\n"
        ),
        color=discord.Color.purple()
    )
    for b in RECOMMENDED_BOTS:
        embed.add_field(
            name=f"{b['category']}: {b['name']}",
            value=f"{b['description']}\n🔗 [**Click to Invite {b['name'].split()[0]}**]({b['invite_url']})",
            inline=False
        )
    embed.set_footer(text="Tip: Once invited, assign them the '🤖 Bots' role!")
    return embed


def build_manual_guide_embeds() -> list[discord.Embed]:
    """Generate embeds for human admin manual settings."""
    embeds = []
    header_embed = discord.Embed(
        title="🛠️ Server Admin Checklist: Actions You Must Complete Manually",
        description=(
            "Discord's security model restricts certain settings to human server owners/admins inside the Discord client.\n"
            "Follow this checklist to finish configuring your server for prime time:"
        ),
        color=discord.Color.gold()
    )
    embeds.append(header_embed)

    for item in MANUAL_ACTIONS_GUIDE:
        emb = discord.Embed(
            title=item["title"],
            description="\n".join([f"• {step}" for step in item["steps"]]),
            color=discord.Color.dark_theme()
        )
        embeds.append(emb)
    return embeds


# ==========================================
# COMMANDS: SLASH & PREFIX
# ==========================================

@bot.tree.command(name="setup", description="Automatically provision roles, categories, and channels for this server.")
@app_commands.describe(
    preset="Choose template layout: 'roblox_studio', 'community', 'gaming', or 'developer'",
    clean_old="Delete existing channels before creating new layout (default: False)"
)
@app_commands.choices(preset=[
    app_commands.Choice(name="🧱 Roblox Game Studio & Dev Hub", value="roblox_studio"),
    app_commands.Choice(name="Community & Social Hub", value="community"),
    app_commands.Choice(name="Gaming Clan & Esports", value="gaming"),
    app_commands.Choice(name="Developer & Tech Studio", value="developer"),
])
async def slash_setup(interaction: discord.Interaction, preset: str = "roblox_studio", clean_old: bool = False):
    if not is_admin_or_owner(interaction.user):
        await interaction.response.send_message("❌ Only Administrators or the Server Owner can run this setup command.", ephemeral=True)
        return

    await interaction.response.send_message(f"⏳ Initiating server setup with preset `{preset}`... Please wait.")

    async def update_status(text: str):
        try:
            await interaction.followup.send(text)
        except Exception:
            pass

    try:
        await execute_server_setup(interaction.guild, preset, clean_old, update_status)
    except Exception as e:
        logger.error(f"Setup failed: {e}", exc_info=True)
        await interaction.followup.send(f"❌ Setup error: `{e}`")


@bot.command(name="setup")
async def prefix_setup(ctx: commands.Context, preset: str = "roblox_studio", clean_old: str = "no"):
    """
    Prefix command: !setup [roblox_studio|community|gaming|developer] [clean=yes|no]
    """
    if not is_admin_or_owner(ctx.author):
        await ctx.send("❌ Only Administrators or the Server Owner can run this setup command.")
        return

    clean_flag = clean_old.lower() in ("yes", "true", "clean", "1")
    status_msg = await ctx.send(f"⏳ Initiating server setup with preset `{preset}` (Clean channels: {clean_flag})...")

    async def update_status(text: str):
        await ctx.send(text)

    try:
        await execute_server_setup(ctx.guild, preset, clean_flag, update_status)
    except Exception as e:
        logger.error(f"Setup failed: {e}", exc_info=True)
        await ctx.send(f"❌ Setup error: `{e}`")


@bot.tree.command(name="bot_invites", description="Get direct 1-click invite links for top Discord bots.")
async def slash_bot_invites(interaction: discord.Interaction):
    embed = build_bot_invites_embed()
    await interaction.response.send_message(embed=embed)


@bot.command(name="botinvites")
async def prefix_bot_invites(ctx: commands.Context):
    """Get 1-click invite links for top bots."""
    embed = build_bot_invites_embed()
    await ctx.send(embed=embed)


@bot.tree.command(name="manual_guide", description="View the checklist of Discord settings only humans can configure.")
async def slash_manual_guide(interaction: discord.Interaction):
    embeds = build_manual_guide_embeds()
    await interaction.response.send_message(embed=embeds[0])
    for emb in embeds[1:]:
        await interaction.followup.send(embed=emb)


@bot.command(name="guide")
async def prefix_manual_guide(ctx: commands.Context):
    """View step-by-step checklist of manual Discord settings."""
    embeds = build_manual_guide_embeds()
    for emb in embeds:
        await ctx.send(embed=emb)
        await asyncio.sleep(0.3)


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Check bot latency."""
    await ctx.send(f"🏓 Pong! Latency: `{round(bot.latency * 1000)}ms`")


def main():
    if not TOKEN or TOKEN.strip() == "your_discord_bot_token_here":
        print("\n" + "=" * 65)
        print("⚠️  MISSING DISCORD BOT TOKEN!")
        print("Please edit the .env file and set your DISCORD_BOT_TOKEN.")
        print("See README.md for instructions on getting your token.")
        print("=" * 65 + "\n")
        return

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
