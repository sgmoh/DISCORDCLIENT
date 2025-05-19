import discord
from discord.ext import commands
import logging
from typing import Dict, List, Optional
from config import CONFIG

logger = logging.getLogger('discord_bot')

# Command information for the enhanced help menu
COMMANDS_INFO = {
    "general": {
        "help": {
            "description": "Shows this help menu",
            "usage": "help",
            "emoji": "<:help:1373370856239267940>"
        },
        "ping": {
            "description": "Check the bot's latency",
            "usage": "ping",
            "emoji": "<:Prefix:1373605377609957426>"
        },
        "info": {
            "description": "Get information about the bot",
            "usage": "info",
            "emoji": "<:help:1373370856239267940>"
        }
    },
    "moderation": {
        "autorole": {
            "description": "Set a role to be automatically assigned to new members",
            "usage": "autorole <role>",
            "emoji": "<:Multipurpose:1373371000271409416>"
        },
        "clearautorole": {
            "description": "Clear the autorole setting",
            "usage": "clearautorole",
            "emoji": "<:clear:1373370955279110245>"
        },
        "kick": {
            "description": "Kick a user from the server",
            "usage": "kick <user> [reason]",
            "emoji": "<:kick:1373370930440569073>"
        },
        "ban": {
            "description": "Ban a user from the server",
            "usage": "ban <user> [reason]",
            "emoji": "<:banned:1373370889235726407>"
        },
        "warn": {
            "description": "Warn a user",
            "usage": "warn <user> [reason]",
            "emoji": "<:Warn:1373605418315677807>"
        },
        "timeout": {
            "description": "Timeout a user for a specified duration",
            "usage": "timeout <user> <duration> [reason]",
            "emoji": "<:timeout:1373371114155413504>"
        },
        "untimeout": {
            "description": "Remove a timeout from a user",
            "usage": "untimeout <user>",
            "emoji": "<:timeout:1373371114155413504>"
        },
        "lock": {
            "description": "Lock the current channel",
            "usage": "lock",
            "emoji": "<:Multipurpose:1373371000271409416>"
        },
        "unlock": {
            "description": "Unlock the current channel",
            "usage": "unlock",
            "emoji": "<:Multipurpose:1373371000271409416>"
        },
        "slowmode": {
            "description": "Set slowmode in the current channel",
            "usage": "slowmode <seconds>",
            "emoji": "<:mute:1373372051024248832>"
        },
        "clear": {
            "description": "Clear messages from a channel",
            "usage": "clear <amount>",
            "emoji": "<:clear:1373370955279110245>"
        }
    },
    "levels": {
        "level": {
            "description": "Check your level or someone else's level",
            "usage": "level [user]",
            "emoji": "<:Clipboard:1373605336820220097>"
        },
        "leaderboard": {
            "description": "View the server's leaderboard",
            "usage": "leaderboard <levels|messages|invites>",
            "emoji": "<:Clipboard:1373605336820220097>"
        }
    },
    "invites": {
        "invites": {
            "description": "Check your invite stats or someone else's",
            "usage": "invites [user]",
            "emoji": "<:Join:1373605236354056346>"
        }
    },
    "messages": {
        "messages": {
            "description": "Check your message stats or someone else's",
            "usage": "messages [user]",
            "emoji": "<:Logs:1373372085866598550>"
        },
        "topmessages": {
            "description": "Show top message senders in the server",
            "usage": "topmessages [all_time|today]",
            "emoji": "<:Logs:1373372085866598550>"
        },
        "resetmessages": {
            "description": "Reset message stats for a user (Admin only)",
            "usage": "resetmessages <user>",
            "emoji": "<:clear:1373370955279110245>"
        }
    },
    "giveaways": {
        "gstart": {
            "description": "Start a giveaway",
            "usage": "gstart <duration> <winners> <prize>",
            "emoji": "<:giveaway:1373607514112790610>"
        },
        "gend": {
            "description": "End a giveaway early",
            "usage": "gend <message_id>",
            "emoji": "<:giveaway:1373607514112790610>"
        },
        "greroll": {
            "description": "Reroll a giveaway",
            "usage": "greroll <message_id>",
            "emoji": "<:giveaway:1373607514112790610>"
        }
    },
    "roles": {
        "reactionrole": {
            "description": "Set up a reaction role message",
            "usage": "reactionrole create",
            "emoji": "<:ReactionRole:1373607898730725469>"
        },
        "reactionrole delete": {
            "description": "Delete a reaction role message",
            "usage": "reactionrole delete <message_id>",
            "emoji": "<:ReactionRole:1373607898730725469>"
        },
        "reactionrole list": {
            "description": "List all reaction role messages",
            "usage": "reactionrole list",
            "emoji": "<:ReactionRole:1373607898730725469>"
        }
    },
    "tickets": {
        "ticket": {
            "description": "Set up the ticket system",
            "usage": "ticket setup",
            "emoji": "<:ticket:1373371061340606594>"
        },
        "close": {
            "description": "Close a ticket channel",
            "usage": "close",
            "emoji": "<:ticket:1373371061340606594>"
        }
    },
    "welcome": {
        "welcome": {
            "description": "Configure welcome messages for new members",
            "usage": "welcome",
            "emoji": "<:joinleave:1373607445439709225>"
        },
        "welcome on": {
            "description": "Enable welcome messages",
            "usage": "welcome on",
            "emoji": "<:joinleave:1373607445439709225>"
        },
        "welcome off": {
            "description": "Disable welcome messages",
            "usage": "welcome off",
            "emoji": "<:joinleave:1373607445439709225>"
        },
        "welcome channel": {
            "description": "Set welcome channel",
            "usage": "welcome channel #channel",
            "emoji": "<:joinleave:1373607445439709225>"
        },
        "welcome message": {
            "description": "Set custom welcome message",
            "usage": "welcome message Your message here",
            "emoji": "<:joinleave:1373607445439709225>"
        }
    },
    "polls": {
        "poll create": {
            "description": "Create a poll with multiple options",
            "usage": "poll create \"Question?\" \"Option 1\" \"Option 2\" ...",
            "emoji": "<:Clipboard:1373605336820220097>"
        },
        "poll timed": {
            "description": "Create a timed poll that automatically ends",
            "usage": "poll timed \"Question?\" 1h \"Option 1\" \"Option 2\" ...",
            "emoji": "<:Clipboard:1373605336820220097>"
        },
        "poll quick": {
            "description": "Create a quick yes/no poll",
            "usage": "poll quick \"Question?\"",
            "emoji": "<:Clipboard:1373605336820220097>"
        },
        "poll end": {
            "description": "End a poll early and show results",
            "usage": "poll end <poll_id>",
            "emoji": "<:Clipboard:1373605336820220097>"
        },
        "poll list": {
            "description": "List all active polls in the server",
            "usage": "poll list",
            "emoji": "<:Clipboard:1373605336820220097>"
        }
    },
    "islamic": {
        "hadith": {
            "description": "Get a random hadith",
            "usage": "hadith",
            "emoji": "☪️"
        },
        "quran": {
            "description": "Get a Quran verse",
            "usage": "quran <surah:ayah>",
            "emoji": "📖"
        },
        "dua": {
            "description": "Get a random dua",
            "usage": "dua [name]",
            "emoji": "🤲"
        },
        "islamic": {
            "description": "Islamic commands and information",
            "usage": "islamic",
            "emoji": "☪️"
        },
        "islamic reminder": {
            "description": "Get a random Quranic reminder",
            "usage": "islamic reminder",
            "emoji": "📖"
        },
        "islamic calendar": {
            "description": "View Islamic calendar date",
            "usage": "islamic calendar",
            "emoji": "📅"
        }
    }
}

# Category colors for better visual organization
CATEGORY_COLORS = {
    "general": 0x7289DA,    # Discord Blue
    "moderation": 0xE74C3C,  # Red
    "levels": 0x2ECC71,     # Green
    "invites": 0x3498DB,    # Blue
    "messages": 0x9B59B6,   # Purple
    "giveaways": 0xF1C40F,  # Yellow
    "roles": 0xE67E22,      # Orange
    "tickets": 0x1ABC9C,    # Teal
    "welcome": 0xF39C12,    # Orange-Yellow
    "polls": 0x11806A,      # Dark Teal
    "islamic": 0x2ECC71     # Green
}

# Category emojis for better visual identification
CATEGORY_EMOJIS = {
    "general": "<:help:1373370856239267940>",
    "moderation": "<:Multipurpose:1373371000271409416>",
    "levels": "<:Clipboard:1373605336820220097>",
    "invites": "<:Join:1373605236354056346>",
    "messages": "<:Logs:1373372085866598550>",
    "giveaways": "<:giveaway:1373607514112790610>",
    "roles": "<:ReactionRole:1373607898730725469>",
    "welcome": "<:joinleave:1373607445439709225>",
    "tickets": "<:ticket:1373371061340606594>",
    "polls": "<:Clipboard:1373605336820220097>",
    "islamic": "☪️"
}

class CategorySelect(discord.ui.Select):
    """Dropdown for selecting help categories"""
    
    def __init__(self, bot):
        self.bot = bot
        
        # Create options for each category
        options = [
            discord.SelectOption(
                label="General",
                description="General bot commands",
                emoji=CATEGORY_EMOJIS["general"],
                value="general"
            ),
            discord.SelectOption(
                label="Moderation",
                description="Server moderation commands",
                emoji=CATEGORY_EMOJIS["moderation"],
                value="moderation"
            ),
            discord.SelectOption(
                label="Levels",
                description="Level tracking and rewards",
                emoji=CATEGORY_EMOJIS["levels"],
                value="levels"
            ),
            discord.SelectOption(
                label="Invites",
                description="Invite tracking and statistics",
                emoji=CATEGORY_EMOJIS["invites"],
                value="invites"
            ),
            discord.SelectOption(
                label="Messages",
                description="Message tracking and leaderboards",
                emoji=CATEGORY_EMOJIS["messages"],
                value="messages"
            ),
            discord.SelectOption(
                label="Giveaways",
                description="Create and manage giveaways",
                emoji=CATEGORY_EMOJIS["giveaways"],
                value="giveaways"
            ),
            discord.SelectOption(
                label="Roles",
                description="Self-assignable reaction roles",
                emoji=CATEGORY_EMOJIS["roles"],
                value="roles"
            ),
            discord.SelectOption(
                label="Welcome",
                description="Welcome messages for new members",
                emoji=CATEGORY_EMOJIS["welcome"],
                value="welcome"
            ),
            discord.SelectOption(
                label="Tickets",
                description="Support ticket system",
                emoji=CATEGORY_EMOJIS["tickets"],
                value="tickets"
            ),
            discord.SelectOption(
                label="Polls",
                description="Create and manage polls",
                emoji=CATEGORY_EMOJIS["polls"],
                value="polls"
            ),
            discord.SelectOption(
                label="Islamic",
                description="Islamic commands and resources",
                emoji=CATEGORY_EMOJIS["islamic"],
                value="islamic"
            )
        ]
        
        super().__init__(
            placeholder="Select a command category...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="help_category_select",
            row=0
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle category selection"""
        category = self.values[0]
        
        # Get the theme color for this category
        color = CATEGORY_COLORS.get(category, CONFIG['colors']['default'])
        emoji = CATEGORY_EMOJIS.get(category, "ℹ️")
        
        # Create embed for the selected category - NO IMAGE
        embed = discord.Embed(
            title=f"{emoji} {category.title()} Commands",
            description=f"Use {CONFIG['prefix']}help <command> for more details on a command.",
            color=color
        )
        
        # Format commands in a compact view
        commands = COMMANDS_INFO.get(category, {})
        
        if commands:
            command_list = []
            for cmd_name, cmd_info in commands.items():
                # Add emoji if available
                cmd_emoji = cmd_info.get('emoji', '')
                command_list.append(f"{cmd_emoji} `{CONFIG['prefix']}{cmd_name}` - {cmd_info['description']}")
            
            # Make sure description is not None before appending
            if embed.description:
                embed.description = f"{embed.description}\n\n" + "\n".join(command_list)
            else:
                embed.description = "\n".join(command_list)
        else:
            # Safely update description
            if embed.description:
                embed.description = f"{embed.description}\n\nNo commands available in this category."
            else:
                embed.description = "No commands available in this category."
        
        # Add footer
        embed.set_footer(text="Created by gh_sman", 
                        icon_url=self.bot.user.display_avatar.url)
        
        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(discord.ui.View):
    """View containing the help menu components"""
    
    def __init__(self, bot):
        super().__init__(timeout=180)  # 3 minute timeout
        self.bot = bot
        
        # Add category select
        self.add_item(CategorySelect(bot))
        
        # Add home button
        self.home_button = discord.ui.Button(
            label="Home",
            emoji="🏠",
            style=discord.ButtonStyle.secondary,
            custom_id="help_home_button",
            row=1
        )
        self.home_button.callback = self.home_callback
        self.add_item(self.home_button)
        
        # Add invite button
        self.invite_button = discord.ui.Button(
            label="Invite",
            emoji="📨",
            style=discord.ButtonStyle.link,
            url="https://discord.com/api/oauth2/authorize?client_id=1373013347590602944&permissions=1099511627775&scope=bot%20applications.commands",
            row=1
        )
        self.add_item(self.invite_button)
        
        # Add support button
        self.support_button = discord.ui.Button(
            label="Support",
            emoji="❓",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/gazaguild",
            row=1
        )
        self.add_item(self.support_button)
    
    async def home_callback(self, interaction: discord.Interaction):
        """Handle home button clicks"""
        embed = await self.create_home_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def create_home_embed(self):
        """Create the main help menu embed"""
        embed = discord.Embed(
            title="Bot Help Menu",
            description=f"Created by gh_sman\nMy prefix is {CONFIG['prefix']}\nUse the dropdown menu below to browse commands.",
            color=CONFIG['colors']['default']
        )
        
        # Set footer with bot avatar
        embed.set_footer(
            text="Created by gh_sman", 
            icon_url=self.bot.user.display_avatar.url
        )
        
        return embed

class EnhancedHelpMenu(commands.Cog):
    """Enhanced help menu with complete command listings"""
    
    def __init__(self, bot):
        self.bot = bot
        logger.info("EnhancedHelpMenu cog initialized")
    
    @commands.hybrid_command(name="help", description="Shows the help menu with interactive dropdown")
    async def help_command(self, ctx, command=None):
        """Show the help menu with interactive dropdown"""
        if command is not None:
            # Show help for a specific command
            await self.show_command_help(ctx, command)
            return
        
        # Show the main help menu
        view = HelpView(self.bot)
        embed = await view.create_home_embed()
        
        # Simple help menu with no GIF, just the dropdown
        await ctx.send(embed=embed, view=view)
    
    async def show_command_help(self, ctx, command_name):
        """Show detailed help for a specific command"""
        cmd = self.bot.get_command(command_name)
        if not cmd:
            embed = discord.Embed(
                title="Command Not Found",
                description=f"Cannot find command `{command_name}`. Use `{CONFIG['prefix']}help` to see all available commands.",
                color=CONFIG['colors']['error']
            )
            await ctx.send(embed=embed)
            return
        
        # Create detailed command help
        embed = discord.Embed(
            title=f"Help: {CONFIG['prefix']}{cmd.name}",
            description=cmd.help or "No description available.",
            color=CONFIG['colors']['default']
        )
        
        # Add aliases if any
        if cmd.aliases:
            embed.add_field(name="Aliases", value=", ".join(cmd.aliases), inline=False)
        
        # Add usage
        usage = f"{CONFIG['prefix']}{cmd.name}"
        if cmd.signature:
            usage += f" {cmd.signature}"
        
        embed.add_field(name="Usage", value=f"`{usage}`", inline=False)
        
        # Try to find the command in our info dictionary
        for category, commands in COMMANDS_INFO.items():
            if cmd.name in commands:
                cmd_info = commands[cmd.name]
                
                # Add example
                embed.add_field(
                    name="Example", 
                    value=f"`{CONFIG['prefix']}{cmd_info['usage']}`", 
                    inline=False
                )
                
                # Add category info
                emoji = CATEGORY_EMOJIS.get(category, "ℹ️")
                embed.add_field(
                    name="Category",
                    value=f"{emoji} {category.title()}",
                    inline=True
                )
                
                # Add command emoji if available
                cmd_emoji = cmd_info.get('emoji', '')
                if cmd_emoji:
                    embed.add_field(
                        name="Command Icon",
                        value=f"{cmd_emoji}",
                        inline=True
                    )
                
                break
        
        await ctx.send(embed=embed)

async def setup(bot):
    # Remove the old help command
    bot.remove_command('help')
    # Add the new help command
    await bot.add_cog(EnhancedHelpMenu(bot))