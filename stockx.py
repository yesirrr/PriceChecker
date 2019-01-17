import discord
from discord.ext import commands
import json
import requests

token = 'YOUR TOKEN HERE'
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')
    
@client.command(pass_context=True)
async def sx(ctx, *args):
    keywords = ''
    for word in args:
        keywords += word + '%20'
    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, 'utf-8')
    x = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", "x-algolia-application-id": "XW7SBCT9V6", "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"}
    with requests.Session() as s:
        r = s.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=x, verify=False, data=byte_payload, timeout=30)
    results = r.json()["hits"][0]

    embed = discord.Embed(title='StockX Checker', color=0x13e79e)
    embed.set_thumbnail(url=results['thumbnail_url'])
    embed.set_footer(text='@kxvxnc#6989')
    embed.add_field(name=results['name'], value='https://stockx.com/' + results['url'], inline=False)
    embed.add_field(name='SKU/PID:', value=results['style_id'], inline=True)
    embed.add_field(name='Colorway:', value=results['colorway'], inline=True)
    for trait in results['traits']:
        if trait['name'] == 'Retail Price':
            embed.add_field(name='Retail Price:', value='$' + str(trait['value']), inline=True)
    embed.add_field(name='Release Date:', value=results['release_date'], inline=True)
    embed.add_field(name='Highest Bid:', value='$' + str(results['highest_bid']), inline=True)
    embed.add_field(name='Lowest Ask:', value='$' + str(results['lowest_ask']), inline=True)
    embed.add_field(name='Sales in the last 72 hrs:', value='$' + str(results['sales_last_72']), inline=True)
    embed.add_field(name='Total Pairs Sold:', value=results['deadstock_sold'], inline=True)
    
    await client.say(embed=embed)

client.run(token)
