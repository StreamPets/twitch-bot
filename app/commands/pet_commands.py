from typing import TYPE_CHECKING

from twitchio.ext import commands

if TYPE_CHECKING:
  from bot import ChatBot


class PetCommands(commands.Cog):

  def __init__(self, bot: commands.Bot) -> None:
    self.bot: 'ChatBot' = bot

  @commands.command(name='jump')
  async def command_jump(self, ctx: commands.Context):
    channel_name = ctx.channel.name
    user_id = ctx.author.id
    self.bot.api.announce_jump(channel_name, user_id)

  @commands.command(name='color', aliases=['colour'])
  async def command_color(self, ctx: commands.Context, color: str):
    channel_name = ctx.channel.name
    user_id = ctx.author.id
    self.bot.api.announce_color(channel_name, user_id, color)
