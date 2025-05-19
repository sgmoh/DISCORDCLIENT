import discord
from discord.ext import commands
import logging
from config import CONFIG

logger = logging.getLogger('discord_bot')

class ClearCommands(commands.Cog):
    """Commands for clearing messages and other content"""
    
    def __init__(self, bot):
        self.bot = bot
        logger.info("ClearCommands cog initialized")
    
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clear a specified number of messages from the channel
        
        Args:
            amount: The number of messages to delete (default: 5, max: 100)
        """
        # Check amount
        if amount < 1:
            embed = discord.Embed(
                title="❌ Invalid Amount",
                description="You must delete at least 1 message.",
                color=CONFIG['colors']['error']
            )
            await ctx.send(embed=embed)
            return
            
        if amount > 100:
            embed = discord.Embed(
                title="⚠️ Amount Limited",
                description="You can only delete up to 100 messages at a time. Amount has been set to 100.",
                color=CONFIG['colors']['warning']
            )
            await ctx.send(embed=embed, delete_after=5)
            amount = 100
        
        # Delete the command message first
        await ctx.message.delete()
        
        # Delete the messages
        deleted = await ctx.channel.purge(limit=amount)
        
        # Send confirmation (will be deleted after 5 seconds)
        embed = discord.Embed(
            title="✅ Messages Deleted",
            description=f"Successfully deleted {len(deleted)} messages.",
            color=CONFIG['colors']['success']
        )
        
        await ctx.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(ClearCommands(bot))