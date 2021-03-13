# source
# https://github.com/kxvxnc/Stockx-Discord-Bot/blob/master/main.py

import discord
from discord.ext import commands
import json
import requests
import asyncio

# actual bot token: NzY0NTIyMzk2OTUzNjA4MjAz.X4He9w.FgfgSSIgmk2zbhsYExcIMxjDzCI
# test bot token: NzcxMDY0MTU2ODQwMzk0NzYy.X5mrdA.jLHF-As5TRaNSV0p2ujq0xMbAMg
token = "NzY0NTIyMzk2OTUzNjA4MjAz.X4He9w.FgfgSSIgmk2zbhsYExcIMxjDzCI"
client = commands.Bot(command_prefix=".")
selected = 0
numResults = 0


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=".s and .g")
    )


async def lookup_stockx(keywords, ctx):
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    algolia = {
        "x-algolia-agent": "Algolia for JavaScript (4.8.4); Browser",
        "x-algolia-application-id": "XW7SBCT9V6",
        "x-algolia-api-key": "6b5e76b49705eb9f51a06d3c82f7acee",
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
        results = r.json()["hits"][0]
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
    embed.set_footer(
        text="StockX",
        icon_url="https://cdn.discordapp.com/attachments/734938642790744097/771078700178866226/stockx.png",
    )
    await ctx.send(embed=embed)


async def lookup_goat(selection, keywords, ctx):
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    algolia = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.25.1",
        "x-algolia-application-id": "2FWOTDVM2O",
        "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a",
    }
    header = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,lt;q=0.8",
        "appos": "web",
        "appversion": "0.1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    }
    with requests.Session() as session:
        r = session.post(
            "https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query",
            params=algolia,
            verify=False,
            data=byte_payload,
            timeout=30,
        )
        results = r.json()["hits"][0]
        apiurl_prices = f"https://www.goat.com/web-api/v1/product_variants?productTemplateId={results['slug']}"
        apiurl_general = (
            f"https://www.goat.com/web-api/v1/product_templates/{results['slug']}"
        )

    response_prices = requests.get(apiurl_prices, verify=False, headers=header)
    response_general = requests.get(apiurl_general, verify=False, headers=header)

    prices = response_prices.json()
    general = response_general.json()
    sizes = []
    for size in prices:
        if (
            size["boxCondition"] == "good_condition"
            and size["shoeCondition"] == "new_no_defects"
        ):
            sizes.append(size)

    embed = discord.Embed(
        title=f"{general['name']}",
        url=f"https://www.goat.com/sneakers/{general['slug']}",
        color=0x099F5F,
    )
    embed.set_thumbnail(url=general["gridPictureUrl"])
    if "sku" in general:
        embed.add_field(name="SKU:", value=general["sku"], inline=True)
    else:
        embed.add_field(name="SKU:", value="N/A", inline=True)
    if "localizedSpecialDisplayPriceCents" in general:
        embed.add_field(
            name="Retail Price:",
            value=f"${int(general['localizedSpecialDisplayPriceCents']['amountUsdCents'] / 100)}",
            inline=True,
        )
    else:
        embed.add_field(name="Retail Price:", value="N/A")
    embed.add_field(name="‎⠀", value="⠀", inline=False)
    for size in sizes:
        lowestPrice = int(size["lowestPriceCents"]["amountUsdCents"] / 100)
        embed.add_field(
            name=size["size"],
            value=f"${lowestPrice}",
            inline=True,
        )
    embed.set_footer(
        text="Goat",
        icon_url="https://cdn.discordapp.com/attachments/734938642790744097/771077292881477632/goat.png",
    )
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def logout(ctx):
    await client.logout()


@client.command(pass_context=True)
async def s(ctx, *args):
    keywords = ""
    for word in args:
        keywords += word + " "
    keywords.rstrip()
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    params = {
        "x-algolia-agent": "Algolia for JavaScript (4.8.4); Browser",
        "x-algolia-application-id": "XW7SBCT9V6",
        "x-algolia-api-key": "6b5e76b49705eb9f51a06d3c82f7acee",
    }
    with requests.Session() as session:
        r = session.post(
            "https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query",
            params=params,
            verify=False,
            data=byte_payload,
            timeout=30,
        )
        # * print the results to a json file to make it easier to read
        # with open("data.json", "w", encoding="utf-8") as f:
        #     json.dump(r.json()["hits"][0], f, ensure_ascii=False, indent=4)
        numResults = len(r.json()["hits"])

    if numResults != 0:
        await lookup_stockx(keywords, ctx)
    else:
        await ctx.send("No products found. Please try again.")


@client.command(pass_context=True)
async def g(ctx, *args):
    keywords = ""
    for word in args:
        keywords += word + "%20"
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, "utf-8")
    algolia = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.25.1",
        "x-algolia-application-id": "2FWOTDVM2O",
        "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a",
    }
    with requests.Session() as session:
        r = session.post(
            "https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query",
            params=algolia,
            verify=False,
            data=byte_payload,
            timeout=30,
        )
        numResults = len(r.json()["hits"])

    if numResults != 0:
        await lookup_goat(0, keywords, ctx)
    else:
        await ctx.send("No products found. Please try again.")


# @client.command(pass_context=True)
# async def ys(ctx, *args):
#     if len(args) == 1:
#         url = (
#             "https://www.yeezysupply.com/hpl/content/availability-v2/yeezy-supply/US/"
#             + args[0]
#             + ".json"
#         )
#         r = requests.get(url)
#         print(r.json())
#     else:
#         await ctx.send("Incorrect usage. Input SKU only.")


client.run(token)
