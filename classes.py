import toml
import datetime
import discord

class Configs:
    with open("./config.toml", "r", encoding='utf-8') as f:
        Data = toml.load(f)

    Token = Data["bot"]["token"]
    Prefix = Data["bot"]["prefix"]
    Github = Data["bot"]["github"]
    Regexs = Data["regexs"]

class Embeds:
    def Error():
        embed = discord.Embed()
        embed.color = discord.Colour.red()
        embed.title = "Error"
        embed.timestamp = datetime.datetime.utcnow()
        
        return embed
    def Success(con):
        embed = discord.Embed()
        embed.color = discord.Colour.teal()
        embed.title = "Converted"
        embed.timestamp = datetime.datetime.utcnow()
        embed.description = "```toml\n{0}```".format(con)
        
        return embed
    def Loading():
        embed = discord.Embed()
        embed.color = discord.Colour.darker_gray()
        embed.title = "Uploading"
        embed.timestamp = datetime.datetime.utcnow()
        embed.description = "Please Wait..."
        
        return embed