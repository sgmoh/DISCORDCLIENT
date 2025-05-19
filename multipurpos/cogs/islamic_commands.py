import discord
from discord.ext import commands
import logging
import json
import os
import random
import datetime
from config import CONFIG

logger = logging.getLogger('discord_bot')

class IslamicCommands(commands.Cog):
    """Islamic commands and utilities"""
    
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/islamic_settings.json'
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Define daily hadith database
        self.hadiths = [
            {"text": "The Messenger of Allah (ﷺ) said, 'The world is sweet and green, and verily Allah is going to install you as vicegerent in it in order to see how you act. So avoid the allurement of women: verily, the first trial for the people of Israel was caused by women.'", "source": "Sahih Muslim"},
            {"text": "The Prophet (ﷺ) said, 'Religion is very easy and whoever overburdens himself in his religion will not be able to continue in that way. So you should not be extremists, but try to be near to perfection and receive the good tidings that you will be rewarded.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'The best among you are those who have the best manners and character.'", "source": "Sahih al-Bukhari"},
            {"text": "Allah's Messenger (ﷺ) said, 'Whoever builds a mosque for Allah, Allah will build for him likewise in Paradise.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'Do not wish to be like anyone except in two cases: A person whom Allah has given wealth and he spends it righteously, and a person whom Allah has given wisdom and he acts according to it and teaches it to others.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'When Allah loves a servant, He calls Gabriel and says: I love so-and-so, so love him. Then Gabriel loves him and makes an announcement in heaven: Allah loves so-and-so, so love him. Then the inhabitants of heaven love him, and he is given acceptance on earth.'", "source": "Sahih al-Bukhari and Muslim"},
            {"text": "The Prophet (ﷺ) said, 'The believer's shade on the Day of Resurrection will be his charity.'", "source": "Tirmidhi"},
            {"text": "The Prophet (ﷺ) said, 'A Muslim is the one who avoids harming Muslims with his tongue and hands. And a Muhajir (emigrant) is the one who gives up (abandons) all what Allah has forbidden.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'Whoever is not merciful to others will not be treated mercifully.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'Make things easy and do not make them difficult, cheer the people up by conveying glad tidings to them and do not repulse them.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'The signs of a hypocrite are three: When he speaks, he lies; when he promises, he breaks his promise; and when he is entrusted with something, he betrays that trust.'", "source": "Sahih al-Bukhari"},
            {"text": "The Prophet (ﷺ) said, 'None of you truly believes until he loves for his brother what he loves for himself.'", "source": "Sahih al-Bukhari and Muslim"},
            {"text": "The Prophet (ﷺ) said, 'The most beloved of deeds to Allah are those that are most consistent, even if it is small.'", "source": "Sahih al-Bukhari and Muslim"},
            {"text": "The Prophet (ﷺ) said, 'Allah does not look at your figures, nor at your attire but He looks at your hearts and accomplishments.'", "source": "Sahih Muslim"},
            {"text": "The Prophet (ﷺ) said, 'The strong person is not the one who overcomes people by his strength, but the strong person is the one who controls himself while in anger.'", "source": "Sahih al-Bukhari"},
        ]
        
        # Define Quran verses for reminder
        self.quran_verses = [
            {"verse": "Indeed, Allah is with those who fear Him and those who are doers of good.", "surah": "An-Nahl 16:128"},
            {"verse": "And whoever relies upon Allah - then He is sufficient for him. Indeed, Allah will accomplish His purpose. Allah has already set for everything a [decreed] extent.", "surah": "At-Talaq 65:3"},
            {"verse": "And whoever fears Allah - He will make for him a way out. And will provide for him from where he does not expect.", "surah": "At-Talaq 65:2-3"},
            {"verse": "And We have already created man and know what his soul whispers to him, and We are closer to him than his jugular vein.", "surah": "Qaf 50:16"},
            {"verse": "So remember Me; I will remember you. And be grateful to Me and do not deny Me.", "surah": "Al-Baqarah 2:152"},
            {"verse": "Those who believe and whose hearts find rest in the remembrance of Allah, Verily, in the remembrance of Allah do hearts find rest.", "surah": "Ar-Ra'd 13:28"},
            {"verse": "And your Lord says, 'Call upon Me; I will respond to you.'", "surah": "Ghafir 40:60"},
            {"verse": "And We have certainly created man and know what his soul whispers to him, and We are closer to him than [his] jugular vein.", "surah": "Qaf 50:16"},
            {"verse": "For indeed, with hardship [will be] ease. Indeed, with hardship [will be] ease.", "surah": "Ash-Sharh 94:5-6"},
            {"verse": "And whoever puts all his trust in Allah, then He will suffice him.", "surah": "At-Talaq 65:3"},
        ]
        
        # Define Islamic duas
        self.duas = [
            {"name": "Morning Supplication", "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَٰهَ إِلاَّ اللهُ وَحْدَهُ لاَ شَرِيكَ لَهُ", "translation": "We have reached the morning and at this very time all sovereignty belongs to Allah, and all praise is for Allah. None has the right to be worshipped except Allah, alone, without any partner."},
            {"name": "Evening Supplication", "arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ للهِ، وَالْحَمْدُ للهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "translation": "We have reached the evening and at this very time all sovereignty belongs to Allah, and all praise is for Allah. None has the right to be worshipped except Allah, alone, without any partner."},
            {"name": "Before Sleeping", "arabic": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "translation": "In Your name, O Allah, I die and I live."},
            {"name": "When Waking Up", "arabic": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", "translation": "All praise is for Allah who gave us life after having taken it from us and unto Him is the resurrection."},
            {"name": "Entering the Mosque", "arabic": "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ", "translation": "O Allah, open the gates of Your mercy for me."},
            {"name": "Leaving the Mosque", "arabic": "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ", "translation": "O Allah, I ask You from Your favour."},
            {"name": "Before Eating", "arabic": "بِسْمِ اللهِ", "translation": "In the name of Allah."},
            {"name": "After Eating", "arabic": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا، وَرَزَقَنِيهِ، مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ", "translation": "All praise is for Allah who fed me this and provided it for me without any might or power on my part."},
            {"name": "When Afflicted with Hardship", "arabic": "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ", "translation": "There is no deity except You; exalted are You. Indeed, I have been of the wrongdoers."},
            {"name": "For Anxiety and Sorrow", "arabic": "اللَّهُمَّ إِنِّي عَبْدُكَ، ابْنُ عَبْدِكَ، ابْنُ أَمَتِكَ، نَاصِيَتِي بِيَدِكَ، مَاضٍ فِيَّ حُكْمُكَ، عَدْلٌ فِيَّ قَضَاؤُكَ", "translation": "O Allah, I am Your servant, son of Your servant, son of Your maidservant, my forelock is in Your hand, Your command over me is forever executed and Your decree over me is just."},
        ]
        
        logger.info("IslamicCommands cog initialized")
    
    @commands.group(name="islamic", invoke_without_command=True)
    async def islamic(self, ctx):
        """Islamic commands and information"""
        embed = discord.Embed(
            title="☪️ Islamic Commands",
            description="Various Islamic commands and utilities",
            color=CONFIG['colors']['default']
        )
        
        # Add command examples
        commands = [
            f"`{CONFIG['prefix']}hadith` - Get a random hadith",
            f"`{CONFIG['prefix']}quran <surah:ayah>` - Get a Quran verse",
            f"`{CONFIG['prefix']}dua` - Get a random dua",
            f"`{CONFIG['prefix']}islamic reminder` - Get a random Quranic reminder",
            f"`{CONFIG['prefix']}islamic calendar` - View Islamic calendar date"
        ]
        
        embed.add_field(
            name="Available Commands",
            value="\n".join(commands),
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="hadith")
    async def hadith(self, ctx):
        """Get a random hadith"""
        # Select a random hadith
        hadith = random.choice(self.hadiths)
        
        embed = discord.Embed(
            title="📜 Hadith",
            description=hadith["text"],
            color=CONFIG['colors']['default']
        )
        
        embed.set_footer(text=f"Source: {hadith['source']}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="dua")
    async def dua(self, ctx, *, dua_name=None):
        """Get a dua
        
        Args:
            dua_name: Specific dua to show (optional)
        """
        if dua_name:
            # Look for specific dua
            matching_duas = [d for d in self.duas if d["name"].lower() == dua_name.lower()]
            
            if not matching_duas:
                # Try partial match
                matching_duas = [d for d in self.duas if dua_name.lower() in d["name"].lower()]
                
            if not matching_duas:
                embed = discord.Embed(
                    title="❌ Dua Not Found",
                    description=f"Could not find a dua with the name '{dua_name}'. Try using one of the following:\n" + 
                                "\n".join([f"• {d['name']}" for d in self.duas]),
                    color=CONFIG['colors']['error']
                )
                await ctx.send(embed=embed)
                return
                
            dua = matching_duas[0]
        else:
            # Select a random dua
            dua = random.choice(self.duas)
        
        embed = discord.Embed(
            title=f"🤲 {dua['name']}",
            color=CONFIG['colors']['default']
        )
        
        embed.add_field(
            name="Arabic",
            value=dua["arabic"],
            inline=False
        )
        
        embed.add_field(
            name="Translation",
            value=dua["translation"],
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @islamic.command(name="reminder")
    async def quran_reminder(self, ctx):
        """Get a random Quranic reminder"""
        # Select a random verse
        verse = random.choice(self.quran_verses)
        
        embed = discord.Embed(
            title="📖 Quranic Reminder",
            description=verse["verse"],
            color=CONFIG['colors']['default']
        )
        
        embed.set_footer(text=f"Surah {verse['surah']}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="quran")
    async def quran(self, ctx, reference=None):
        """Get a Quran verse
        
        Args:
            reference: Surah and verse reference (e.g., 2:255 for Ayatul Kursi)
        """
        if not reference:
            embed = discord.Embed(
                title="❓ Quran Reference Required",
                description=f"Please provide a Quran reference in the format `surah:ayah`.\nExample: `{CONFIG['prefix']}quran 2:255` for Ayatul Kursi.",
                color=CONFIG['colors']['warning']
            )
            await ctx.send(embed=embed)
            return
        
        try:
            # Parse reference
            parts = reference.split(':')
            if len(parts) != 2:
                raise ValueError("Invalid format")
                
            surah = int(parts[0])
            ayah = int(parts[1])
            
            # For simplicity and to avoid external API dependency, provide a fallback
            embed = discord.Embed(
                title=f"Surah {surah}, Verse {ayah}",
                description="This is a sample verse display. In a complete implementation, this would fetch the actual verse from an API.",
                color=CONFIG['colors']['default']
            )
            
            embed.add_field(
                name="Note",
                value="Due to the limits of this environment, this command displays a placeholder. In a full implementation, it would fetch the actual verse text from a Quran API.",
                inline=False
            )
            
            await ctx.send(embed=embed)
                    
        except Exception as e:
            logger.error(f"Error processing Quran reference: {e}")
            
            embed = discord.Embed(
                title="⚠️ Could not process verse reference",
                description="Please check your reference format (surah:ayah) and try again.",
                color=CONFIG['colors']['error']
            )
            
            embed.add_field(
                name="Example",
                value=f"`{CONFIG['prefix']}quran 2:255` for Ayatul Kursi (The Throne Verse).",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    @islamic.command(name="calendar")
    async def islamic_calendar(self, ctx):
        """View current Islamic calendar date"""
        try:
            # For simplicity, provide the current date without external API
            # In a full implementation, this would fetch the actual Hijri date
            current_date = datetime.datetime.now()
            
            embed = discord.Embed(
                title="📅 Islamic Calendar",
                description="Islamic date information",
                color=CONFIG['colors']['default']
            )
            
            embed.add_field(
                name="Gregorian Date",
                value=current_date.strftime("%d %B %Y"),
                inline=True
            )
            
            embed.add_field(
                name="Note",
                value="This is a placeholder for the Islamic date. A full implementation would convert or fetch the actual Hijri date.",
                inline=False
            )
            
            await ctx.send(embed=embed)
                
        except Exception as e:
            logger.error(f"Error displaying Islamic calendar: {e}")
            
            embed = discord.Embed(
                title="⚠️ Could not display Islamic calendar",
                description="An error occurred while trying to display the Islamic calendar.",
                color=CONFIG['colors']['error']
            )
            
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(IslamicCommands(bot))