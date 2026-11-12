"""
Server Templates configuration for Discord Setup Bot.
Each template defines roles, categories, channels, permissions, and welcome message.
"""
import discord

TEMPLATES = {
    "roblox_studio": {
        "name": "Roblox Game Studio & Dev Hub",
        "description": "Customized for Roblox game studios: Scripters, Builders, UI designers, QA testers, game sneaks, bug reports, and player community.",
        "roles": [
            {
                "name": "👑 Studio Owner / Lead Dev",
                "color": discord.Color.gold(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(administrator=True),
            },
            {
                "name": "🛠️ Studio Co-Owner",
                "color": discord.Color.red(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(administrator=True),
            },
            {
                "name": "💻 Lead Scripter",
                "color": discord.Color.blue(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(manage_messages=True, embed_links=True, attach_files=True),
            },
            {
                "name": "🏗️ 3D Modeler & Builder",
                "color": discord.Color.orange(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(manage_messages=True, embed_links=True, attach_files=True),
            },
            {
                "name": "🎨 UI / Graphic Designer",
                "color": discord.Color.magenta(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(embed_links=True, attach_files=True),
            },
            {
                "name": "🎵 Sound Designer",
                "color": discord.Color.teal(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(embed_links=True, attach_files=True),
            },
            {
                "name": "🧪 QA Tester",
                "color": discord.Color.purple(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=True, view_channel=True, attach_files=True),
            },
            {
                "name": "🛡️ Community Moderator",
                "color": discord.Color.dark_blue(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(manage_messages=True, kick_members=True, ban_members=True, mute_members=True),
            },
            {
                "name": "⭐ Gamepass / VIP Supporter",
                "color": discord.Color.yellow(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=True, attach_files=True, use_external_emojis=True),
            },
            {
                "name": "🤖 Bots & Webhooks",
                "color": discord.Color.dark_grey(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=True, embed_links=True),
            },
            {
                "name": "🎮 Player / Member",
                "color": discord.Color.green(),
                "hoist": False,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=True, view_channel=True, connect=True, speak=True),
            },
            {
                "name": "🔇 Muted",
                "color": discord.Color.dark_grey(),
                "hoist": False,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=False, speak=False),
            },
        ],
        "categories": [
            {
                "name": "📌 STUDIO INFORMATION",
                "sync_permissions": False,
                "channels": [
                    {
                        "name": "📜-rules-and-guidelines",
                        "type": "text",
                        "topic": "Official studio & game guidelines. Follow Discord and Roblox Terms of Use.",
                        "read_only": True,
                    },
                    {
                        "name": "📢-studio-announcements",
                        "type": "text",
                        "topic": "Important studio announcements, events, and releases.",
                        "read_only": True,
                    },
                    {
                        "name": "🚀-game-updates-logs",
                        "type": "text",
                        "topic": "Game patch notes, balance changes, and new features changelogs.",
                        "read_only": True,
                    },
                    {
                        "name": "👀-sneaks-and-leaks",
                        "type": "text",
                        "topic": "Exclusive teasers, concept art, and gameplay sneak peeks of upcoming game updates!",
                        "read_only": True,
                    },
                    {
                        "name": "🔗-official-links",
                        "type": "text",
                        "topic": "Official links: Roblox Game, Roblox Group, DevForum, and Socials.",
                        "read_only": True,
                    },
                ],
            },
            {
                "name": "💬 COMMUNITY & PLAYERS",
                "sync_permissions": True,
                "channels": [
                    {"name": "💬-general-chat", "type": "text", "topic": "General chat for all players and community members."},
                    {"name": "📸-gameplay-and-clips", "type": "text", "topic": "Share your screenshots, gameplay clips, and fanart."},
                    {"name": "💡-game-suggestions", "type": "text", "topic": "Got ideas for the game? Post your suggestions here!"},
                    {"name": "🐛-bug-reports", "type": "text", "topic": "Found a bug in-game? Report it here with video/screenshots and reproduction steps."},
                    {"name": "🤖-bot-commands", "type": "text", "topic": "Use bot commands here."},
                ],
            },
            {
                "name": "🛠️ DEV TEAM (STUDIO ONLY)",
                "staff_only": True,
                "channels": [
                    {"name": "💻-dev-general", "type": "text", "topic": "Private discussions for scripters, modelers, builders, and designers."},
                    {"name": "📝-sprints-and-tasks", "type": "text", "topic": "Track sprint milestones, Trello boards, and update deadlines."},
                    {"name": "🧪-qa-testing-logs", "type": "text", "topic": "Bug tracking and test builds with the QA testing team."},
                    {"name": "🔔-webhooks-and-git", "type": "text", "topic": "GitHub commits, Rojo sync, or Roblox Open Cloud webhooks."},
                    {"name": "🛡️-moderator-logs", "type": "text", "topic": "Moderation alerts and incident reports."},
                    {"name": "🔨 Dev Studio Voice", "type": "voice", "user_limit": 10},
                ],
            },
            {
                "name": "🔊 PLAYER VOICE LOUNGES",
                "sync_permissions": True,
                "channels": [
                    {"name": "🎮 Squad Comms 1", "type": "voice", "user_limit": 4},
                    {"name": "🎮 Squad Comms 2", "type": "voice", "user_limit": 4},
                    {"name": "Lobby Lounge (Casual)", "type": "voice", "user_limit": 0},
                    {"name": "🧪 Playtest Session", "type": "voice", "user_limit": 15},
                ],
            },
        ],
    },
    "community": {
        "name": "Community & Social Hub",
        "description": "Ideal for general clubs, social hangouts, interest groups, and public communities.",
        "roles": [
            {
                "name": "👑 Server Owner",
                "color": discord.Color.gold(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(administrator=True),
            },
            {
                "name": "🛡️ Administrator",
                "color": discord.Color.red(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(administrator=True),
            },
            {
                "name": "⚔️ Moderator",
                "color": discord.Color.blue(),
                "hoist": True,
                "mentionable": True,
                "permissions": discord.Permissions(
                    manage_messages=True,
                    kick_members=True,
                    ban_members=True,
                    mute_members=True,
                    deafen_members=True,
                    move_members=True,
                    view_audit_log=True,
                ),
            },
            {
                "name": "🤖 Bots",
                "color": discord.Color.teal(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    read_message_history=True,
                ),
            },
            {
                "name": "⭐ VIP / Supporter",
                "color": discord.Color.purple(),
                "hoist": True,
                "mentionable": False,
                "permissions": discord.Permissions(
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    use_external_emojis=True,
                ),
            },
            {
                "name": "👥 Member",
                "color": discord.Color.green(),
                "hoist": False,
                "mentionable": False,
                "permissions": discord.Permissions(
                    send_messages=True,
                    view_channel=True,
                    read_message_history=True,
                    connect=True,
                    speak=True,
                ),
            },
            {
                "name": "🔇 Muted",
                "color": discord.Color.dark_grey(),
                "hoist": False,
                "mentionable": False,
                "permissions": discord.Permissions(send_messages=False, speak=False),
            },
        ],
        "categories": [
            {
                "name": "📌 INFORMATION & RULES",
                "sync_permissions": False,
                "channels": [
                    {
                        "name": "rules-and-info",
                        "type": "text",
                        "topic": "Welcome! Please read the rules and guidelines before participating.",
                        "read_only": True,
                    },
                    {
                        "name": "announcements",
                        "type": "text",
                        "topic": "Official community announcements and updates.",
                        "read_only": True,
                    },
                    {
                        "name": "welcome",
                        "type": "text",
                        "topic": "Say hello to new members joining our community!",
                        "read_only": False,
                    },
                    {
                        "name": "roles-selection",
                        "type": "text",
                        "topic": "Get self-assignable roles here (configure with Reaction Roles bot).",
                        "read_only": True,
                    },
                ],
            },
            {
                "name": "💬 COMMUNITY CHAT",
                "sync_permissions": True,
                "channels": [
                    {"name": "general-chat", "type": "text", "topic": "General discussion and chat for everyone."},
                    {"name": "media-and-memes", "type": "text", "topic": "Share funny memes, clips, images, and videos."},
                    {"name": "bot-playground", "type": "text", "topic": "Use bot commands here (!rank, /play, etc.)"},
                    {"name": "introductions", "type": "text", "topic": "Introduce yourself to the server community!"},
                ],
            },
            {
                "name": "🎨 INTERESTS & HOBBIES",
                "sync_permissions": True,
                "channels": [
                    {"name": "gaming-talk", "type": "text", "topic": "Chat about PC, Console, and Mobile games."},
                    {"name": "tech-and-creations", "type": "text", "topic": "Showcase your projects, artwork, tech, or setups."},
                    {"name": "music-and-films", "type": "text", "topic": "Recommend songs, shows, anime, and movies."},
                ],
            },
            {
                "name": "🔊 VOICE LOUNGES",
                "sync_permissions": True,
                "channels": [
                    {"name": "Lounge 1 (General)", "type": "voice", "user_limit": 0},
                    {"name": "Lounge 2 (Chill)", "type": "voice", "user_limit": 10},
                    {"name": "Gaming Voice 1", "type": "voice", "user_limit": 5},
                    {"name": "Gaming Voice 2", "type": "voice", "user_limit": 5},
                    {"name": "Stream / Watch Party", "type": "voice", "user_limit": 0},
                ],
            },
            {
                "name": "🛡️ STAFF HEADQUARTERS",
                "staff_only": True,
                "channels": [
                    {"name": "staff-chat", "type": "text", "topic": "Private discussions for Admins and Moderators."},
                    {"name": "mod-logs", "type": "text", "topic": "Audit logs, bot alerts, and moderation actions."},
                    {"name": "bot-setup-guide", "type": "text", "topic": "Server configuration notes and bot command manuals."},
                    {"name": "Staff Meeting", "type": "voice", "user_limit": 10},
                ],
            },
        ],
    },
    "gaming": {
        "name": "Gaming Clan / Esports",
        "description": "Tailored for gaming teams, clans, streaming squads, and matchmaking.",
        "roles": [
            {"name": "👑 Clan Leader", "color": discord.Color.gold(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(administrator=True)},
            {"name": "🛡️ Captain / Admin", "color": discord.Color.red(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(administrator=True)},
            {"name": "⚔️ Tournament Host", "color": discord.Color.orange(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(manage_messages=True, manage_channels=True)},
            {"name": "🎮 Competitive Team", "color": discord.Color.purple(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(send_messages=True, speak=True)},
            {"name": "📺 Content Creator", "color": discord.Color.magenta(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(send_messages=True, embed_links=True)},
            {"name": "🕹️ Member", "color": discord.Color.blue(), "hoist": False, "mentionable": False, "permissions": discord.Permissions(send_messages=True, speak=True)},
            {"name": "🤖 Bots", "color": discord.Color.teal(), "hoist": True, "mentionable": False, "permissions": discord.Permissions(send_messages=True, embed_links=True)},
        ],
        "categories": [
            {
                "name": "📌 CLAN HEADQUARTERS",
                "channels": [
                    {"name": "clan-rules", "type": "text", "topic": "Server and clan rules.", "read_only": True},
                    {"name": "announcements", "type": "text", "topic": "Events, tourneys, and roster updates.", "read_only": True},
                    {"name": "match-schedules", "type": "text", "topic": "Upcoming scrims and matches.", "read_only": True},
                ],
            },
            {
                "name": "💬 SQUAD LOBBY",
                "channels": [
                    {"name": "general-lobby", "type": "text", "topic": "General chat for members."},
                    {"name": "looking-for-group", "type": "text", "topic": "Ping to find squadmates for games!"},
                    {"name": "clips-and-highlights", "type": "text", "topic": "Post your best gameplay clips and aces."},
                    {"name": "bot-commands", "type": "text", "topic": "Stat checkers, music bots, and commands."},
                ],
            },
            {
                "name": "🔊 SQUAD COMMS",
                "channels": [
                    {"name": "Duo 1", "type": "voice", "user_limit": 2},
                    {"name": "Trio 1", "type": "voice", "user_limit": 3},
                    {"name": "Squad 1 (4-Player)", "type": "voice", "user_limit": 4},
                    {"name": "Competitive Team 5v5", "type": "voice", "user_limit": 5},
                    {"name": "General Gaming Voice", "type": "voice", "user_limit": 0},
                ],
            },
            {
                "name": "🛡️ LEADERSHIP",
                "staff_only": True,
                "channels": [
                    {"name": "leader-chat", "type": "text", "topic": "Clan management and recruitment."},
                    {"name": "mod-logs", "type": "text", "topic": "Moderation actions."},
                    {"name": "War Room", "type": "voice", "user_limit": 0},
                ],
            },
        ],
    },
    "developer": {
        "name": "Developer & Tech Studio",
        "description": "Optimized for software development, open source projects, tech startups, and bot builders.",
        "roles": [
            {"name": "👑 Founder / Lead Dev", "color": discord.Color.gold(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(administrator=True)},
            {"name": "🚀 Core Maintainer", "color": discord.Color.blue(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(administrator=True)},
            {"name": "💻 Developer / Contributor", "color": discord.Color.green(), "hoist": True, "mentionable": True, "permissions": discord.Permissions(send_messages=True, embed_links=True)},
            {"name": "🧪 Beta Tester", "color": discord.Color.orange(), "hoist": True, "mentionable": False, "permissions": discord.Permissions(send_messages=True)},
            {"name": "🤖 Bots & Webhooks", "color": discord.Color.teal(), "hoist": True, "mentionable": False, "permissions": discord.Permissions(send_messages=True, embed_links=True)},
            {"name": "👤 Member", "color": discord.Color.light_grey(), "hoist": False, "mentionable": False, "permissions": discord.Permissions(send_messages=True, view_channel=True)},
        ],
        "categories": [
            {
                "name": "📌 PROJECT OVERVIEW",
                "channels": [
                    {"name": "readme-and-guidelines", "type": "text", "topic": "Project documentation, roadmap, and guidelines.", "read_only": True},
                    {"name": "releases-and-updates", "type": "text", "topic": "Version releases, changelogs, and release notes.", "read_only": True},
                    {"name": "github-feed", "type": "text", "topic": "Automated commit, PR, and issue feeds via Webhooks.", "read_only": True},
                ],
            },
            {
                "name": "💬 DEV DISCUSSIONS",
                "channels": [
                    {"name": "general-dev", "type": "text", "topic": "General development and engineering talk."},
                    {"name": "architecture-design", "type": "text", "topic": "System design, databases, and APIs."},
                    {"name": "bug-reports", "type": "text", "topic": "Report bugs and edge cases with reproduction steps."},
                    {"name": "feature-requests", "type": "text", "topic": "Propose ideas and improvements."},
                    {"name": "code-showcase", "type": "text", "topic": "Show off your code snippets, demos, and repos."},
                ],
            },
            {
                "name": "🔊 PAIR PROGRAMMING",
                "channels": [
                    {"name": "Pair Coding 1", "type": "voice", "user_limit": 2},
                    {"name": "Pair Coding 2", "type": "voice", "user_limit": 2},
                    {"name": "Sprint / Standup", "type": "voice", "user_limit": 10},
                    {"name": "Coworking Lounge", "type": "voice", "user_limit": 0},
                ],
            },
            {
                "name": "🛡️ INTERNAL / OPS",
                "staff_only": True,
                "channels": [
                    {"name": "admin-chat", "type": "text", "topic": "Private founder and admin communications."},
                    {"name": "infrastructure-alerts", "type": "text", "topic": "Sentry, Datadog, or server uptime alerts."},
                    {"name": "Core Dev Voice", "type": "voice", "user_limit": 0},
                ],
            },
        ],
    },
}

RECOMMENDED_BOTS = [
    {
        "name": "Bloxlink (Roblox Account & Group Sync)",
        "description": "Crucial for Roblox studios! Syncs Roblox accounts, verifies players, and automatically binds Discord roles to your Roblox Group ranks.",
        "invite_url": "https://discord.com/oauth2/authorize?client_id=426537812993638400&permissions=8&scope=bot%20applications.commands",
        "category": "🧱 Roblox Integration",
    },
    {
        "name": "Carl-bot (Moderation & Reaction Roles)",
        "description": "Essential all-in-one bot for reaction roles, custom commands, advanced auto-moderation, and logging.",
        # Carl-bot invite URL with recommended permissions (8 = Administrator, or 402653208)
        "invite_url": "https://discord.com/oauth2/authorize?client_id=235148963503953920&permissions=8&scope=bot%20applications.commands",
        "category": "🛡️ Moderation & Utilities",
    },
    {
        "name": "Ticket Tool (Support Tickets)",
        "description": "Creates a private ticket channel when users click a button. Perfect for member support, reports, and inquiries.",
        "invite_url": "https://discord.com/oauth2/authorize?client_id=550624846044422152&permissions=8&scope=bot%20applications.commands",
        "category": "🎫 Customer & Community Support",
    },
    {
        "name": "ProBot (Welcome Images & Leveling)",
        "description": "Sends custom graphical welcome cards, XP leveling system, auto-roles, and automod.",
        "invite_url": "https://discord.com/oauth2/authorize?client_id=282859044593598464&permissions=8&scope=bot%20applications.commands",
        "category": "🎉 Engagement & Welcoming",
    },
    {
        "name": "Disboard (Grow Your Server)",
        "description": "Publishes your server to the global public Disboard directory so new members can find and join it.",
        "invite_url": "https://discord.com/oauth2/authorize?client_id=302050872383242240&permissions=274878220304&scope=bot",
        "category": "📈 Server Growth",
    },
    {
        "name": "Jockie Music (High Quality Voice Audio)",
        "description": "Play high quality music and radio directly in voice channels with multi-bot support.",
        "invite_url": "https://discord.com/oauth2/authorize?client_id=411916947793543168&permissions=36768768&scope=bot%20applications.commands",
        "category": "🎵 Music & Voice",
    },
]

MANUAL_ACTIONS_GUIDE = [
    {
        "title": "1. Enable Discord 'Community' Mode (CRITICAL)",
        "steps": [
            "Open **Server Settings** (top left dropdown next to server name).",
            "Scroll down to **Community** in the left sidebar and click **Enable Community**.",
            "Click **Get Started** and check the boxes for Verification level and Explicit Media filter.",
            "Choose `#rules-and-info` as the Rules channel and `#announcements` as the Community Updates channel.",
            "Click **Finish Setup**.",
            "🌟 *Why this matters:* Unlocks Announcement broadcasting, Welcome Screen, Server Insights, and Forum channels!",
        ],
    },
    {
        "title": "2. Set Default Notification Settings",
        "steps": [
            "Open **Server Settings** -> **Overview**.",
            "Change **Default Notification Settings** from 'All Messages' to **'Only @mentions'**.",
            "🌟 *Why this matters:* If set to 'All Messages', members get pinged for every message and will mute or leave your server.",
        ],
    },
    {
        "title": "3. Configure Discord AutoMod",
        "steps": [
            "Open **Server Settings** -> **Safety Setup** (under Community).",
            "Under **AutoMod Rules**, turn on **Block Mention Spam** (set max mentions to 4 or 5).",
            "Turn on **Block Suspected Spam Content**.",
            "Turn on **Block Common Bad Words**.",
            "🌟 *Why this matters:* Built-in Discord AI blocks phishing links, raids, and toxic words with zero latency.",
        ],
    },
    {
        "title": "4. Upload Server Icon & Banner",
        "steps": [
            "Open **Server Settings** -> **Overview**.",
            "Click **Upload Image** to add your server icon (recommended size: 512x512 PNG/GIF).",
            "Upload a Server Banner (if your server has Level 2 Boosts).",
        ],
    },
    {
        "title": "5. Turn On 2FA Requirement for Moderation",
        "steps": [
            "Open **Server Settings** -> **Safety Setup**.",
            "Enable **Require 2FA for moderator actions**.",
            "🌟 *Why this matters:* Prevents compromised staff accounts from deleting channels or banning everyone in a raid.",
        ],
    },
    {
        "title": "6. Invite Essential Bots",
        "steps": [
            "Run `/bot_invites` or `!botinvites` in your server to get 1-click links for Carl-bot, Ticket Tool, etc.",
            "Authorize them via your web browser with Administrator permissions.",
            "Drag each bot's role in Server Settings -> Roles above the Member role so they can manage permissions properly.",
        ],
    },
]
