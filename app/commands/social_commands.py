from twitchio.ext import commands


class SocialCommands(commands.Cog):

  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.command(name='discord')
  async def command_discord(self, ctx):
    await ctx.send('https://discord.gg/S2MDMqk')
