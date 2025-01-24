from twitchio.ext import commands


class SocialComponent(commands.Component):
  @commands.command(name='discord')
  async def command_discord(self, ctx: commands.Context):
    await ctx.send("https://discord.gg/S2MDMqk")

async def setup(bot: commands.Bot):
  await bot.add_component(SocialComponent())
