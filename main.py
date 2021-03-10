import discord
import re
import toml
import json
import aiohttp
import functools
import asyncio

from github import Github
from classes import Configs, Embeds
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix=Configs.Prefix)
git = Github(Configs.Github)
repo = git.get_repo("DelfinBot/Pastes")

@bot.event
async def on_ready():
    selfUp.start()
    print("Im Ready!")

@bot.command(
    name="ping", 
    description="Calculate bot ping",
    brief="Calculate bot ping"
)
async def _ping(ctx):
    await ctx.send(f"Pong: **{round(bot.latency * 1000)}**ms")

@bot.command(
    name="convert", 
    description="Convert JSON file to TOML file",
    brief="Convert JSON file to TOML file"
)
            
async def _conv(ctx, *, content):
    pastebin = re.findall(Configs.Regexs["pastebin"], content)
    if len(pastebin) > 0:
        await ctx.send(embed=Embeds.Loading())
        async with aiohttp.ClientSession() as session:
            async with session.get(pastebin[0]) as response:
                content = await response.text()

        try:
            jsonConv = json.loads(content)
        except:
            error = Embeds.Error()
            error.description = ":x: Invalid JSON. (Parse Error)"
            return await ctx.send(embed=error)

        try:
            tomlConv = toml.dumps(jsonConv)
        except:
            error = Embeds.Error()
            error.description = ":x: This JSON can't converted. (Dump Error)"
            return await ctx.send(embed=error)

        if len(tomlConv) > 1500:
            await ctx.send("TOML Version is too big for send here. please type `yes` if you want to upload this file to github repo *(everyone can see the file)*, type `no` if you don't.")
            try:
                mesaj = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no"], timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("Process canceled.")
            else:
                if mesaj.content.lower() == "no":
                    return await ctx.send("Process canceled.")

                def CreateFile(data):
                    filename = f"{ctx.message.id}.toml"
                    repo.create_file(path=f"{filename}", message=f"For User >>> {ctx.author.id}", content=data)

                    return "https://github.com/DelfinBot/Pastes/blob/main/{0}".format(repo.get_contents(f"{filename}").path)

                asyncfunc = functools.partial(CreateFile, tomlConv)
                runasync = await bot.loop.run_in_executor(None, asyncfunc)

                success = Embeds.Success(f"URL = {runasync}")
                await ctx.send(embed=success)
        else:
            success = Embeds.Success(tomlConv)
            await ctx.send(embed=success)
    else:
        block_regex = re.search(Configs.Regexs["block"], content, re.DOTALL)
        if not block_regex or not block_regex.group(2):
            error = Embeds.Error()
            error.description = ":x: Invalid Text-Block."
            return await ctx.send(embed=error)

        try:
            jsonConv = json.loads(block_regex.group(2))
        except:
            error = Embeds.Error()
            error.description = ":x: Invalid JSON. (Parse Error)"
            return await ctx.send(embed=error)

        try:
            tomlConv = toml.dumps(jsonConv)
        except:
            error = Embeds.Error()
            error.description = ":x: This JSON can't converted. (Dump Error)"
            return await ctx.send(embed=error)

        if len(tomlConv) > 1500:
            await ctx.send("TOML Version is too big for send here. please type `yes` if you want to upload this file to github repo *(everyone can see the file)*, type `no` if you don't.")
            try:
                mesaj = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no"], timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.send("Process canceled.")
            else:
                if mesaj.content.lower() == "no":
                    return await ctx.send("Process canceled.")

                def CreateFile(data):
                    filename = f"{ctx.message.id}.toml"
                    repo.create_file(path=f"{filename}", message=f"For User >>> {ctx.author.id}", content=data)

                    return "https://github.com/DelfinBot/Pastes/blob/main/{0}".format(repo.get_contents(f"{filename}").path)

                asyncfunc = functools.partial(CreateFile, tomlConv)
                runasync = await bot.loop.run_in_executor(None, asyncfunc)

                success = Embeds.Success(f"URL = {runasync}")
                await ctx.send(embed=success)
        else:
            success = Embeds.Success(tomlConv)
            await ctx.send(embed=success)

@bot.event         
async def on_command_error(ctx, error):
    print(error)
    
@tasks.loop(seconds=60)
async def selfUp():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pytoml.herokuapp.com/") as response:
            print("Uptimed!")

bot.run(Configs.Token)