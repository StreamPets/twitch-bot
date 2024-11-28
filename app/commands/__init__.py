from .pet_commands import PetCommands
from .social_commands import SocialCommands

def prepare(bot):
  bot.add_cog(PetCommands(bot))
  bot.add_cog(SocialCommands(bot))
