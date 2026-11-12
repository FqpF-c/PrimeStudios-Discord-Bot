# 🛠️ Discord Server Architect & Setup Bot

A complete, automated Discord server provisioning bot. When given the **Administrator** role, this bot can automatically create roles with hierarchical permissions, build structured categories and channels (read-only announcements, rules, staff headquarters, voice channels), publish welcome embeds, and provide one-click bot invites and manual configuration checklists.

---

## ⚡ What The Bot Automates (With Admin Role)
- **Role Hierarchy Creation:** Builds colored, hoisted roles (`👑 Owner`, `🛡️ Administrator`, `⚔️ Moderator`, `🤖 Bots`, `⭐ VIP`, `👥 Member`, `🔇 Muted`) with granular permissions.
- **Category & Channel Architecture:** Builds formatted text, voice, and announcement channels across 3 custom presets (`community`, `gaming`, `developer`).
- **Permission Lockdowns:** 
  - Makes `#rules-and-info` and `#announcements` read-only for `@everyone`, editable only by staff.
  - Hides `🛡️ STAFF HEADQUARTERS` (`#staff-chat`, `#mod-logs`) completely from ordinary members.
- **Interactive Embeds:** Automatically posts server guidelines into `#rules-and-info` and welcomes in `#welcome`.
- **Bot Invite Hub:** Generates one-click direct authorization links for essential third-party bots.
- **Admin Configuration Checklist:** Posts clear instructions on the Discord client settings you must enable manually.

---

## 🛑 What Bots CANNOT Do (Discord API Boundaries)

Discord's security model strictly prohibits bot tokens from performing certain actions. For these, the bot provides 1-click links and clear checklists:

1. **Inviting Other Bots:**
   - *Why:* Discord's OAuth2 security requires a verified human user with `Manage Server` permissions to authenticate third-party bot installations in a web browser. A bot cannot add another bot via API.
   - *Solution:* The bot provides `/bot_invites` with 1-click links with pre-calculated permission sets for Carl-bot, Ticket Tool, ProBot, Disboard, etc.
2. **Enabling Discord Community Mode:**
   - Must be clicked manually in **Server Settings -> Enable Community**.
3. **Setting Server Icon & Banner:**
   - Requires server boosts (for banner) and manual image upload in **Server Settings -> Overview**.
4. **Discord Native AutoMod Rule Activation:**
   - Mentions spam filters and keyword blocks must be toggled in **Server Settings -> Safety Setup**.
5. **Enabling 2FA Requirement for Moderation:**
   - Discord requires the server owner's 2FA device to enable this in **Server Settings -> Safety Setup**.

---

## 🚀 Quick Start Guide

### Step 1: Create Your Bot on Discord Developer Portal
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** (top right) and name your bot (e.g., `Server Architect`).
3. Click the **Bot** tab on the left sidebar:
   - Click **Reset Token** and copy your token.
   - Under **Privileged Gateway Intents**, turn ON:
     - ✅ **Server Members Intent**
     - ✅ **Message Content Intent**
   - Click **Save Changes**.

### Step 2: Invite Your Bot with Administrator Permissions
1. In the Developer Portal, go to **OAuth2** -> **URL Generator**.
2. Under **Scopes**, select:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, select:
   - `Administrator`
4. Copy the generated URL at the bottom, paste it into your browser, select your Discord server, and click **Authorize**.

---

### Step 3: Configure `.env`
Open the `.env` file in this directory and paste your bot token:
```env
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
GUILD_ID=
```
*(Optional: If you enter your server's Guild ID, slash commands sync instantly. Without it, global sync may take up to an hour, though you can use the `!setup` prefix command immediately!)*

---

### Step 4: Run the Bot
Double-click `start_bot.bat` or run in terminal:
```bash
.\venv\Scripts\python bot.py
```
When running, you will see:
```text
Logged in as Server Architect#1234
Bot is ready!
```

---

## 🎮 Server Setup Commands

Once the bot is in your server and possesses the **Administrator** role:

### 1. Provision Your Server
Run either the Slash Command or the Prefix Command:
- **Slash command:** `/setup preset:Community & Social Hub clean_old:False`
- **Prefix command:** `!setup community`

#### Available Presets:
| Preset | Target Audience | Key Features |
|---|---|---|
| `community` | General Discord servers, hangouts, clubs | Rules, welcome, general chat, media, hobby channels, voice lounges, staff HQ |
| `gaming` | Gaming squads, clans, esports teams | Looking-for-group, clip highlights, duo/trio/5v5 comms, scrim schedules |
| `developer` | Software teams, open source, tech projects | Releases, changelogs, GitHub webhook feed, architecture, bug reports, pair coding |

> **Tip:** If your server already has default channels you want removed first, pass `clean_old:True` or run `!setup community yes`.

---

### 2. View 1-Click Bot Invites
- **Command:** `/bot_invites` or `!botinvites`
- Provides direct invite links for:
  - **Carl-bot:** Moderation, reaction roles, audit logging.
  - **Ticket Tool:** Private 1-click support and help tickets.
  - **ProBot:** Graphical welcome cards and XP leveling.
  - **Disboard:** Public server listing and member discovery.
  - **Jockie Music:** High fidelity voice channel music playback.

---

### 3. View Manual Setup Checklist
- **Command:** `/manual_guide` or `!guide`
- Steps through the essential Discord client settings that must be configured by you (Community mode, AutoMod, 2FA, notification rules).
