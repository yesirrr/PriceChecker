import discord
from discord.ext import commands
import json
import requests

token = 'YOUR TOKEN HERE'
# Change the prefix if you want
client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')

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
    algolia = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", "x-algolia-application-id": "XW7SBCT9V6", "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"}
    with requests.Session() as session:
        r = session.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=algolia, verify=False, data=byte_payload, timeout=30)
        results = r.json()["hits"][0]
        apiurl = f"https://stockx.com/api/products/{results['url']}?includes=market,360&currency=USD"
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6',
            'appos': 'web',
            'appversion': '0.1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(apiurl, verify=False, headers=header)

    prices = response.json()
    general = prices['Product']
    market = prices['Product']['market']
    sizes = prices['Product']['children']
   
    bidasks = ''
    for size in sizes:
        bidasks +=f"Size {sizes[size]['shoeSize']} | Low Ask ${sizes[size]['market']['lowestAsk']} | High Bid ${sizes[size]['market']['highestBid']}\n"

    embed = discord.Embed(title='StockX Checker', color=0x13e79e)
    embed.set_thumbnail(url=results['thumbnail_url'])
    embed.set_footer(text='@kxvxnc#6989')
    embed.add_field(name=general['title'], value='https://stockx.com/' + general['urlKey'], inline=False)
    if 'styleId' in general:
        embed.add_field(name='SKU/PID:', value=general['styleId'], inline=True)
    else:
        embed.add_field(name='SKU/PID:', value='None', inline=True)
    if 'colorway' in general:
        embed.add_field(name='Colorway:', value=general['colorway'], inline=True)
    else:
        embed.add_field(name='Colorway:', value='None', inline=True)
    if 'retailPrice' in general:
        embed.add_field(name='Retail Price:', value=f"${general['retailPrice']}", inline=True)
    else:
        for trait in general['traits']:
            try:
                embed.add_field(name='Retail Price:', value=f"${int(trait['value'])}")
            except:
                pass
    embed.add_field(name='Release Date:', value=general['releaseDate'], inline=True)
    embed.add_field(name='Highest Bid:', value=f"${market['highestBid']} Size {market['highestBidSize']}", inline=True)
    embed.add_field(name='Lowest Ask:', value=f"${market['lowestAsk']} Size {market['lowestAskSize']}", inline=True)
    embed.add_field(name='Total Asks:', value=market['numberOfAsks'], inline=True)
    embed.add_field(name='Total Bids:', value=market['numberOfBids'], inline=True)
    embed.add_field(name='Total Sold:', value=market['deadstockSold'], inline=True)
    embed.add_field(name='Sales last 72 hrs:', value=market['salesLast72Hours'], inline=True)
    embed.add_field(name='Last Sale:', value=f"${market['lastSale']} Size {market['lastSaleSize']} {market['lastSaleDate'].split('T')[0]} {market['lastSaleDate'].split('T')[1].split('+')[0]}", inline=True)
    embed.add_field(name='Sizes:', value=bidasks, inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def portfolio(ctx, *args):
    author = ctx.message.author
    login = {
        'email': args[0],
        'password': args[1]
    }
    try:
        await client.delete_message(ctx.message)
    except:
        pass
    with requests.Session() as session:
        user = session.post('https://stockx.com/api/login', data=login, verify=False)
        userinfo = user.json()['Customer']
        portgeneral = f"https://stockx.com/api/customers/{userinfo['id']}/collection/stats?currency=USD"
        general = session.get(portgeneral, verify=False).json()
        portfolio = f"https://stockx.com/api/customers/{userinfo['id']}/collection?limit=54"
        port = session.get(portfolio, verify=False).json()
        portformat = ''
        for item in port['PortfolioItems']:
            try:
                portformat += f"{item['product']['shoeSize']} {item['product']['title']}\n"
            except:
                try:
                    portformat += f"{item['product']['title']}\n"
                except:
                    pass

    embed = discord.Embed(title= f"{userinfo['username']}'s' Portfolio", color=0x13e79e)
    embed.set_footer(text='made by @kxvxnc#6989')
    embed.add_field(name='Total Items:', value=general['Statistics']['Summary']['sneakers'], inline=True)
    embed.add_field(name='Total Market Value:', value=f"${general['Statistics']['Summary']['marketValue']}")
    embed.add_field(name='Items:', value=portformat, inline=False)
    await client.send_message(author, embed=embed)
    
if __name__ == "__main__":
    client.run(token)
