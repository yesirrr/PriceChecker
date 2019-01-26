# Stockx-Discord-Bot

Stockx Discord Bot that shows product information based on user keywords.

Commands: 
- .sx [keywords]
- .portfolio [email] [password]

.sx returns an embed with:
- Product Name and StockX link
- Thumbnail Picture
- SKU/PID
- Colorway
- Retail Price
- Release Date (yyyy-mm-dd)
- Highest Bid and corresponding size
- Lowest Ask and corresponding size
- Total Asks
- Total Bids
- Total Pairs Sold
- Sales in the last 72 hrs
- Lowest Ask and Highest Bid for every size

Uses StockX search API to use user keywords to find the product url. Url is then used in the official API which has more data about the product.

.portfolio returns an embed with:
- Username's Portfolio
- Total Items
- Total market value
- List of your portfolio

Due to discord's character limits, I had to sacrifice extra information for the ability to show more items in the portfolio.
This command will message the author only. If you accidently send the command in a public channel, the bot will delete it and send the embed to your dm's.

I recommend using this only for a personal/small server. I don't know if it can handle a very large server.
Make sure to edit stockx.py with your discord bot token and command prefix.

![image](https://user-images.githubusercontent.com/30479452/51453205-1a537180-1d0c-11e9-9904-8eaf6cd61dcb.png)
![image](https://user-images.githubusercontent.com/30479452/51453228-2fc89b80-1d0c-11e9-9bec-bb72d7e1193b.png)
![image](https://user-images.githubusercontent.com/30479452/51791573-35423d80-2173-11e9-9e53-77870f7193a9.png)
