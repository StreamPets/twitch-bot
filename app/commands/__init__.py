from .pet_commands import PetCommands

def prepare(bot):
  bot.add_cog(PetCommands(bot))
