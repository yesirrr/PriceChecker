# Stockx-Discord-Bot

Stockx Discord Bot that shows product information based on user keywords.

Command: sx

It returns an embed with:
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

I recommend using this only for a personal/small server. I don't know if it can handle a very large server.
Make sure to edit stockx.py with your discord bot token and command prefix.

![image](https://user-images.githubusercontent.com/30479452/51453205-1a537180-1d0c-11e9-9904-8eaf6cd61dcb.png)
![image](https://user-images.githubusercontent.com/30479452/51453228-2fc89b80-1d0c-11e9-9bec-bb72d7e1193b.png)
