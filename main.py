import discord
from discord.ext import commands
import json
import requests
import asyncio

token = "NzY0NTIyMzk2OTUzNjA4MjAz.X4He9w.FgfgSSIgmk2zbhsYExcIMxjDzCI"
client = commands.Bot(command_prefix="!")
selected = 0
numResults = 0


async def lookup(selection, keywords, ctx):
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    algolia = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0",
        "x-algolia-application-id": "XW7SBCT9V6",
        "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3",
    }
    header = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6",
        "appos": "web",
        "appversion": "0.1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    with requests.Session() as session:
        r = session.post(
            "https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query",
            params=algolia,
            verify=False,
            data=byte_payload,
            timeout=30,
        )
        results = r.json()["hits"][selection]
        apiurl = f"https://stockx.com/api/products/{results['url']}?includes=market,360&currency=USD"

    response = requests.get(apiurl, verify=False, headers=header)
    prices = response.json()
    general = prices["Product"]
    sizes = prices["Product"]["children"]

    embed = discord.Embed(
        title=f"{general['title']}",
        url=f"https://stockx.com/{general['urlKey']}",
        color=0x099F5F,
    )
    embed.set_thumbnail(url=results["thumbnail_url"])
    if "styleId" in general:
        embed.add_field(name="SKU:", value=general["styleId"], inline=True)
    else:
        embed.add_field(name="SKU:", value="N/A", inline=True)
    if "retailPrice" in general:
        embed.add_field(
            name="Retail Price:", value=f"${general['retailPrice']}", inline=True
        )
    else:
        embed.add_field(name="Retail Price:", value="N/A")
    embed.add_field(name="‎⠀", value="⠀", inline=False)
    for size in sizes:
        embed.add_field(
            name=sizes[size]["shoeSize"],
            value=f"Lowest Ask: ${sizes[size]['market']['lowestAsk']}\nHighest Bid: ${sizes[size]['market']['highestBid']}",
            inline=True,
        )
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def logout(ctx):
    await client.logout()


@client.command(pass_context=True)
async def pc(ctx, *args):
    keywords = ""
    for word in args:
        keywords += word + "%20"
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    params = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0",
        "x-algolia-application-id": "XW7SBCT9V6",
        "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3",
    }
    with requests.Session() as session:
        r = session.post(
            "https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query",
            params=params,
            verify=False,
            data=byte_payload,
            timeout=30,
        )
        numResults = len(r.json()["hits"])

    if numResults != 0:
        await lookup(0, keywords, ctx)
    else:
        await ctx.send("No products found. Please try again.")


client.run(token)
