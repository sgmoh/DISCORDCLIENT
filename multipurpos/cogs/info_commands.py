import discord
from discord.ext import commands
import logging
import platform
import datetime
from config import CONFIG

logger = logging.getLogger('discord_bot')

class InfoCommands(commands.Cog):
    """Information commands for the bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        logger.info("InfoCommands cog initialized")
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check the bot's latency"""
        # Send initial message
        start_time = datetime.datetime.utcnow()
        message = await ctx.send("Pinging...")
        end_time = datetime.datetime.utcnow()
        
        # Calculate latencies
        api_latency = round(self.bot.latency * 1000)
        message_latency = round((end_time - start_time).total_seconds() * 1000)
        
        # Create embed
        embed = discord.Embed(
            title="🏓 Pong!",
            color=CONFIG['colors']['info']
        )
        
        embed.add_field(
            name="API Latency",
            value=f"{api_latency}ms",
            inline=True
        )
        
        embed.add_field(
            name="Message Latency",
            value=f"{message_latency}ms",
            inline=True
        )
        
        await message.edit(content=None, embed=embed)
    
    @commands.command(name="info")
    async def info(self, ctx):
        """Show information about the bot"""
        # Calculate uptime
        uptime_delta = datetime.datetime.utcnow() - self.start_time
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        # Get server count
        server_count = len(self.bot.guilds)
        
        # Get user count (excluding bots)
        user_count = sum(1 for m in self.bot.get_all_members() if not m.bot)
        
        # Get channel count
        channel_count = sum(1 for _ in self.bot.get_all_channels())
        
        # Create embed
        embed = discord.Embed(
            title=f"{self.bot.user.name} Bot Information",
            description="A multipurpose Discord bot with moderation, welcome messages, tickets, and more!",
            color=CONFIG['colors']['default']
        )
        
        # Set bot avatar as thumbnail
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        # Add developer information
        embed.add_field(
            name="💻 Developer",
            value="<@930131254106550333>",
            inline=True
        )
        
        embed.add_field(
            name="💠 Contact",
            value="Email: ghsammo55@gmail.com",
            inline=True
        )
        
        # Add general information
        embed.add_field(
            name="📊 Bot ID",
            value=self.bot.user.id,
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Uptime",
            value=uptime_str,
            inline=True
        )
        
        # Add statistics
        embed.add_field(
            name="🖥️ Servers",
            value=server_count,
            inline=True
        )
        
        embed.add_field(
            name="👥 Users",
            value=user_count,
            inline=True
        )
        
        embed.add_field(
            name="📝 Channels",
            value=channel_count,
            inline=True
        )
        
        # Add commands count
        command_count = len(self.bot.commands)
        cog_count = len(self.bot.cogs)
        
        embed.add_field(
            name="⚙️ Commands",
            value=f"{command_count} commands in {cog_count} modules",
            inline=True
        )
        
        # Add prefix info
        embed.add_field(
            name="📌 Prefix",
            value=f"`{CONFIG['prefix']}`",
            inline=True
        )
        
        # Add version info
        embed.add_field(
            name="🔧 Version",
            value=f"Discord.py {discord.__version__}\nPython {platform.python_version()}",
            inline=True
        )
        
        # Set footer with the developer's information
        embed.set_footer(text="Bot Developed by gh_sman") 
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))