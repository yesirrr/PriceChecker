import discord
from discord.ext import commands
import json
import requests
from tabulate import tabulate
import asyncio

token = 'YOUR TOKEN HERE'
client = commands.Bot(command_prefix = '.')
selected = 0
numResults = 0

async def lookup(selection, keywords, ctx):
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, 'utf-8')
    algolia = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", 
        "x-algolia-application-id": "XW7SBCT9V6", 
        "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"
    }
    header = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6',
        'appos': 'web',
        'appversion': '0.1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    with requests.Session() as session:
        r = session.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=algolia, verify=False, data=byte_payload, timeout=30)
        results = r.json()["hits"][selection]
        apiurl = f"https://stockx.com/api/products/{results['url']}?includes=market,360&currency=USD"

    response = requests.get(apiurl, verify=False, headers=header)
    prices = response.json()
    general = prices['Product']
    market = prices['Product']['market']
    sizes = prices['Product']['children']
   
    table = []
    table.append(['Size', 'Lowest Ask', 'Highest Bid'])
    for size in sizes:
        table.append([sizes[size]['shoeSize'], f"${sizes[size]['market']['lowestAsk']}", f"${sizes[size]['market']['highestBid']}"])

    tabulated = "```" + tabulate(table, headers="firstrow", numalign="center", stralign="center", tablefmt="simple") + "```"

    embed = discord.Embed(title='StockX Checker', color=0x13e79e)
    embed.set_thumbnail(url=results['thumbnail_url'])
    embed.set_footer(text='https://github.com/kxvxnc')
    embed.add_field(name='Product Name', value=f"[{general['title']}](https://stockx.com/{general['urlKey']})", inline=False)
    if 'styleId' in general:
        embed.add_field(name='SKU:', value=general['styleId'], inline=True)
    else:
        embed.add_field(name='SKU:', value='N/A', inline=True)
    if 'colorway' in general:
        embed.add_field(name='Colorway:', value=general['colorway'], inline=True)
    else:
        embed.add_field(name='Colorway:', value='N/A', inline=True)
    if 'retailPrice' in general:
        embed.add_field(name='Retail Price:', value=f"${general['retailPrice']}", inline=True)
    else:
        embed.add_field(name='Retail Price:', value="N/A")
    if 'releaseDate' in general:
        embed.add_field(name='Release Date:', value=general['releaseDate'], inline=True)
    else:
        embed.add_field(name='Release Date:', value="N/A", inline=True)
    embed.add_field(name='Highest Bid:', value=f"${market['highestBid']}", inline=True)
    embed.add_field(name='Lowest Ask:', value=f"${market['lowestAsk']}", inline=True)
    embed.add_field(name='Total Asks:', value=market['numberOfAsks'], inline=True)
    embed.add_field(name='Total Bids:', value=market['numberOfBids'], inline=True)
    embed.add_field(name='Total Sold:', value=market['deadstockSold'], inline=True)
    embed.add_field(name='Sales last 72 hrs:', value=market['salesLast72Hours'], inline=True)
    embed.add_field(name='Last Sale:', value=f"Size {market['lastSaleSize']} ${market['lastSale']} {market['lastSaleDate'].split('T')[0]}", inline=True)
    embed.add_field(name='Sizes:', value=tabulated, inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print('StockX Discord Bot is ready.')

@client.command(pass_context=True)
async def logout(ctx):
    await client.logout()

@client.command(pass_context=True)
async def sx(ctx, *args):
    keywords = ''
    for word in args:
        keywords += word + '%20'
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, 'utf-8')
    params = {
        "x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", 
        "x-algolia-application-id": "XW7SBCT9V6", 
        "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"
    }
    with requests.Session() as session:
        r = session.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=params, verify=False, data=byte_payload, timeout=30)
        numResults = len(r.json()["hits"])
        results = r.json()["hits"]
    
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    def check(reaction, user):
        if str(reaction.emoji) in emojis: 
            global selected 
            selected = emojis.index(str(reaction.emoji))
        return user == ctx.author and str(reaction.emoji) in emojis

    if numResults == 1:
        await lookup(0, keywords, ctx)
    elif numResults >= 2 and numResults <= 10:
        resultsText = ""
        for i in range(numResults):
            resultsText += f"{i + 1}. {results[i]['name']}\n"
        msg = await ctx.send('Multiple products found. React to select the correct product:\n' + "```" + resultsText + "```")
        for i in range(len(results)):
            await msg.add_reaction(emojis[i])
        try:
            await client.wait_for('reaction_add', timeout=30.0, check=check)
            await lookup(selected, keywords, ctx)
            # This automatically deletes the selection message
            # await msg.delete()
        except asyncio.TimeoutError:
            await ctx.send('Took too long to select an option. Please try again.')
    elif numResults == 0:
        await ctx.send('No products found. Please try again.')
    elif numResults > 10:
        await ctx.send('Too many products found. Please try again.')

# .portfolio command removed due to login requiring javascript
    
if __name__ == "__main__":
    client.run(token)
