import discord
from discord.ext import commands
import logging
import datetime
import os
from config import CONFIG

logger = logging.getLogger('discord_bot')

class Logging(commands.Cog):
    """Server logging system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.log_channels = {}  # Guild ID -> Log Channel ID
        self.log_file = 'data/logging_settings.json'
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Load settings from file if it exists
        self.load_settings()
        
        logger.info("Logging cog initialized")
    
    def load_settings(self):
        """Load logging settings from file"""
        try:
            import json
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.log_channels = data.get('log_channels', {})
                    # Convert string keys to int
                    self.log_channels = {int(k): v for k, v in self.log_channels.items()}
                logger.info(f"Loaded logging settings for {len(self.log_channels)} guilds")
            else:
                logger.info("No logging settings file found, using defaults")
        except Exception as e:
            logger.error(f"Error loading logging settings: {e}")
    
    def save_settings(self):
        """Save logging settings to file"""
        try:
            import json
            with open(self.log_file, 'w') as f:
                json.dump({'log_channels': self.log_channels}, f)
            logger.info("Saved logging settings to file")
        except Exception as e:
            logger.error(f"Error saving logging settings: {e}")
    
    @commands.group(name="logs", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def logs(self, ctx):
        """Server logging commands
        
        Use subcommands to manage the logging system:
        - logs set #channel: Set the log channel
        - logs off: Turn off logging
        - logs status: Check logging status
        """
        if ctx.invoked_subcommand is None:
            # Show help for logs command
            embed = discord.Embed(
                title="📝 Server Logging",
                description="Use the following subcommands to manage server logs:",
                color=CONFIG['colors']['default']
            )
            
            embed.add_field(
                name="Commands",
                value=f"`{CONFIG['prefix']}logs set #channel` - Set the logging channel\n"
                      f"`{CONFIG['prefix']}logs off` - Disable logging\n"
                      f"`{CONFIG['prefix']}logs status` - Check logging status",
                inline=False
            )
            
            # Show current status
            log_channel_id = self.log_channels.get(ctx.guild.id)
            if log_channel_id:
                log_channel = ctx.guild.get_channel(log_channel_id)
                if log_channel:
                    embed.add_field(
                        name="Current Status",
                        value=f"Logs are being sent to {log_channel.mention}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="Current Status",
                        value="Logging is enabled but the channel was not found. Please set a new channel.",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="Current Status",
                    value="Logging is currently disabled.",
                    inline=False
                )
            
            await ctx.send(embed=embed)
    
    @logs.command(name="set")
    @commands.has_permissions(manage_guild=True)
    async def logs_set(self, ctx, channel: discord.TextChannel):
        """Set the channel for server logs
        
        Args:
            channel: The text channel to send logs to
        """
        # Update log channel
        self.log_channels[ctx.guild.id] = channel.id
        self.save_settings()
        
        embed = discord.Embed(
            title="✅ Logging Enabled",
            description=f"Server logs will now be sent to {channel.mention}",
            color=CONFIG['colors']['success']
        )
        
        # Add info about what events are logged
        embed.add_field(
            name="Logged Events",
            value="• Message edits and deletions\n"
                  "• Member joins and leaves\n"
                  "• Role and channel changes\n"
                  "• Nickname and username changes\n"
                  "• Voice channel movements\n"
                  "• Moderation actions",
            inline=False
        )
        
        # Send a test log to the channel
        try:
            test_log = discord.Embed(
                title="🔍 Logging System Activated",
                description=f"Server logging has been enabled by {ctx.author.mention}",
                color=CONFIG['colors']['info']
            )
            test_log.add_field(
                name="Timestamp",
                value=f"<t:{int(datetime.datetime.now().timestamp())}:F>",
                inline=False
            )
            await channel.send(embed=test_log)
        except discord.Forbidden:
            embed.add_field(
                name="⚠️ Warning",
                value="I don't have permission to send messages in the log channel.",
                inline=False
            )
        except Exception as e:
            embed.add_field(
                name="⚠️ Warning",
                value=f"Error sending test log: {str(e)}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @logs.command(name="off")
    @commands.has_permissions(manage_guild=True)
    async def logs_off(self, ctx):
        """Disable server logging"""
        if ctx.guild.id in self.log_channels:
            del self.log_channels[ctx.guild.id]
            self.save_settings()
            
            embed = discord.Embed(
                title="🛑 Logging Disabled",
                description="Server logging has been turned off.",
                color=CONFIG['colors']['error']
            )
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="ℹ️ Already Disabled",
                description="Server logging is already disabled.",
                color=CONFIG['colors']['info']
            )
            
            await ctx.send(embed=embed)
    
    @logs.command(name="status")
    @commands.has_permissions(manage_guild=True)
    async def logs_status(self, ctx):
        """Check logging status"""
        embed = discord.Embed(
            title="📊 Logging Status",
            color=CONFIG['colors']['info']
        )
        
        # Check if logging is enabled
        log_channel_id = self.log_channels.get(ctx.guild.id)
        if log_channel_id:
            log_channel = ctx.guild.get_channel(log_channel_id)
            if log_channel:
                embed.description = f"Logging is enabled and set to {log_channel.mention}"
                
                # Check permissions
                permissions = log_channel.permissions_for(ctx.guild.me)
                if not permissions.send_messages or not permissions.embed_links:
                    embed.add_field(
                        name="⚠️ Permission Warning",
                        value="I don't have permission to send messages or embeds in the log channel.",
                        inline=False
                    )
            else:
                embed.description = "Logging is enabled but the channel was not found. Please set a new channel."
                embed.color = CONFIG['colors']['warning']
        else:
            embed.description = "Logging is currently disabled."
        
        await ctx.send(embed=embed)
    
    async def log_event(self, guild, title, description, color=None, fields=None, thumbnail=None):
        """Log an event to the guild's log channel
        
        Args:
            guild: The guild where the event occurred
            title: The title of the log entry
            description: The description of the log entry
            color: The embed color (default: info color)
            fields: List of field tuples (name, value, inline) to add to the embed
            thumbnail: URL to use as the embed thumbnail
        """
        if not guild:
            return
            
        # Check if logging is enabled for this guild
        log_channel_id = self.log_channels.get(guild.id)
        if not log_channel_id:
            return
            
        # Get the log channel
        log_channel = guild.get_channel(log_channel_id)
        if not log_channel:
            # Channel not found, disable logging for this guild
            if guild.id in self.log_channels:
                del self.log_channels[guild.id]
                self.save_settings()
            return
            
        # Create log embed
        if color is None:
            color = CONFIG['colors']['info']
            
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now()
        )
        
        # Add fields if provided
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                
        # Set thumbnail if provided
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
            
        # Send log
        try:
            await log_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error sending log to channel {log_channel.id}: {e}")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log deleted messages"""
        if not message.guild or message.author.bot:
            return
            
        # Don't log private messages or messages from bots
        if message.channel.type == discord.ChannelType.private:
            return
            
        # Create fields for the log
        fields = [
            ("Channel", f"{message.channel.mention} `#{message.channel.name}`", True),
            ("Author", f"{message.author.mention} `{message.author.name}`", True),
            ("Created", f"<t:{int(message.created_at.timestamp())}:R>", True)
        ]
        
        # Add message content if available
        if message.content:
            # Truncate long messages
            content = message.content
            if len(content) > 1024:
                content = content[:1021] + "..."
                
            fields.append(("Content", f"```{content}```", False))
        
        # Add attachment info if any
        if message.attachments:
            attachment_info = "\n".join([f"• `{attachment.filename}` - {attachment.url}" for attachment in message.attachments])
            fields.append(("Attachments", attachment_info, False))
            
        await self.log_event(
            guild=message.guild,
            title="🗑️ Message Deleted",
            description=f"A message was deleted in {message.channel.mention}",
            color=CONFIG['colors']['error'],
            fields=fields,
            thumbnail=message.author.display_avatar.url
        )
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Log edited messages"""
        if not before.guild or before.author.bot:
            return
            
        # Don't log private messages, bot messages, or embeds-only edits
        if before.channel.type == discord.ChannelType.private or before.content == after.content:
            return
            
        # Create fields for the log
        fields = [
            ("Channel", f"{before.channel.mention} `#{before.channel.name}`", True),
            ("Author", f"{before.author.mention} `{before.author.name}`", True),
            ("Jump to Message", f"[Click Here]({after.jump_url})", True)
        ]
        
        # Add before and after content
        before_content = before.content or "*No content*"
        after_content = after.content or "*No content*"
        
        # Truncate long messages
        if len(before_content) > 1024:
            before_content = before_content[:1021] + "..."
        if len(after_content) > 1024:
            after_content = after_content[:1021] + "..."
            
        fields.append(("Before", f"```{before_content}```", False))
        fields.append(("After", f"```{after_content}```", False))
            
        await self.log_event(
            guild=before.guild,
            title="✏️ Message Edited",
            description=f"A message was edited in {before.channel.mention}",
            color=CONFIG['colors']['warning'],
            fields=fields,
            thumbnail=before.author.display_avatar.url
        )
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log member joins"""
        if member.bot:
            return
            
        # Calculate account age
        account_age = datetime.datetime.now() - member.created_at
        account_age_str = f"{account_age.days} days old"
        
        # Add warning if account is new (less than 7 days)
        account_age_warning = ""
        if account_age.days < 7:
            account_age_warning = "⚠️ **New Account Warning**"
            
        fields = [
            ("User", f"{member.mention} `{member.name}`", True),
            ("ID", f"`{member.id}`", True),
            ("Account Created", f"<t:{int(member.created_at.timestamp())}:R> ({account_age_str})", False)
        ]
        
        if account_age_warning:
            fields.append(("Warning", account_age_warning, False))
            
        await self.log_event(
            guild=member.guild,
            title="👋 Member Joined",
            description=f"{member.mention} joined the server",
            color=CONFIG['colors']['success'],
            fields=fields,
            thumbnail=member.display_avatar.url
        )
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log member leaves"""
        if member.bot:
            return
            
        # Calculate how long they were in the server
        joined_at = member.joined_at or datetime.datetime.now()
        member_for = datetime.datetime.now() - joined_at
        member_for_str = f"{member_for.days} days"
        
        # Get roles (exclude @everyone)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles_str = ", ".join(roles) if roles else "No roles"
        
        fields = [
            ("User", f"`{member.name}` (`{member.id}`)", True),
            ("Joined Server", f"<t:{int(joined_at.timestamp())}:R>", True),
            ("Member For", member_for_str, True),
            ("Roles", roles_str, False)
        ]
            
        await self.log_event(
            guild=member.guild,
            title="🚶 Member Left",
            description=f"`{member.name}` left the server",
            color=CONFIG['colors']['error'],
            fields=fields,
            thumbnail=member.display_avatar.url
        )
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Log member updates (nickname, roles)"""
        if before.bot:
            return
            
        # Log nickname changes
        if before.nick != after.nick:
            fields = [
                ("User", f"{after.mention} `{after.name}`", True),
                ("Before", f"`{before.nick or 'No nickname'}`", True),
                ("After", f"`{after.nick or 'No nickname'}`", True)
            ]
                
            await self.log_event(
                guild=after.guild,
                title="📝 Nickname Changed",
                description=f"{after.mention} changed their nickname",
                color=CONFIG['colors']['info'],
                fields=fields,
                thumbnail=after.display_avatar.url
            )
        
        # Log role changes
        before_roles = set(before.roles)
        after_roles = set(after.roles)
        
        # Check for added roles
        added_roles = after_roles - before_roles
        if added_roles:
            role_mentions = [role.mention for role in added_roles]
            role_str = ", ".join(role_mentions)
            
            fields = [
                ("User", f"{after.mention} `{after.name}`", True),
                ("Added Roles", role_str, True)
            ]
                
            await self.log_event(
                guild=after.guild,
                title="🏷️ Roles Added",
                description=f"{after.mention} was given new roles",
                color=CONFIG['colors']['success'],
                fields=fields,
                thumbnail=after.display_avatar.url
            )
        
        # Check for removed roles
        removed_roles = before_roles - after_roles
        if removed_roles:
            role_mentions = [role.mention for role in removed_roles]
            role_str = ", ".join(role_mentions)
            
            fields = [
                ("User", f"{after.mention} `{after.name}`", True),
                ("Removed Roles", role_str, True)
            ]
                
            await self.log_event(
                guild=after.guild,
                title="🏷️ Roles Removed",
                description=f"{after.mention} had roles removed",
                color=CONFIG['colors']['error'],
                fields=fields,
                thumbnail=after.display_avatar.url
            )
    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Log command usage"""
        if not ctx.guild or ctx.author.bot:
            return
            
        command_name = ctx.command.qualified_name
        command_args = ctx.message.content[len(f"{ctx.prefix}{command_name}"):]
        
        fields = [
            ("User", f"{ctx.author.mention} `{ctx.author.name}`", True),
            ("Channel", f"{ctx.channel.mention} `{ctx.channel.name}`", True),
            ("Command", f"`{ctx.prefix}{command_name}{command_args}`", False)
        ]
            
        await self.log_event(
            guild=ctx.guild,
            title="🤖 Command Used",
            description=f"{ctx.author.mention} used a command",
            color=CONFIG['colors']['info'],
            fields=fields,
            thumbnail=ctx.author.display_avatar.url
        )

async def setup(bot):
    await bot.add_cog(Logging(bot))