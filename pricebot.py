import discord, time, os, random, requests, json, subprocess, asyncio, urllib.request
from discord.ext.commands import Bot
from discord.ext import commands


discord_token = 'xxxxxxxxxx' #https://discord.com/developers/applications
discord_bot_user_id = 'xxxxxxxxxx' #right click your bot in discord and select Copy ID
cryptocompare_api_key = 'xxxxxxxx' #get one here https://www.cryptocompare.com/cryptopian/api-keys
crypto_coin = 'LTC' #crypto coin to check for. Default is LTC (litecoin). Please use coin ticker, and not full name.
#how often the bot will change nickname and presence data (price, data, etc) on the sidebar. Do not set this too low or there might be issues and throttling by discord.
nickname_refresh_period = 55 #seconds

# healthchecks.io alerts. Disabled by default
# https://healthchecks.io/docs/
# Use 1 to enable or 0 to disable
enable_healthchecksio_monitoring = 0
#alert that gets pinged on error
healthchecks_fail_url = 'https://hc-ping.com/yyyyy/fail'
#success ping
healthchecks_okcheck_url = 'https://hc-ping.com/yyyyy'


#init some discord stuff
intents = discord.Intents.default() 
intents.members = True
client = discord.Client(intents=intents)

#wait for client to be ready then launch the loop
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    await background_loop()

#cryptowatch api, replaced by cryptocompare
def get_latest_cryptowatch_price():
    #convert to lowercase for gdax
    ticker = crypto_coin.lower()
    cryptowatch_request = 'https://api.cryptowat.ch/markets/coinbase-pro/' + str(ticker) + 'usd/price'
    response = requests.get(cryptowatch_request)
    json_data2 = json.loads(response.text)
    return int(json_data2['result']['price'])   

#fetch latest crypto data from cryptocompare api
def get_latest_crypto_data():
    cryptocompare_api_call = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + str(crypto_coin) + '&tsyms=USD&api_key=' + str(cryptocompare_api_key)
    response = requests.get(cryptocompare_api_call)
    json_data2 = json.loads(response.text)
    #fetch volume, market cap, change % 24h and hourly, price
    coin_volume24h = json_data2['RAW'][str(crypto_coin)]['USD']['TOTALVOLUME24HTO']
    btcglbb = json_data2['RAW'][str(crypto_coin)]['USD']['MKTCAP']
    btcglcc = json_data2['RAW'][str(crypto_coin)]['USD']['CHANGEPCT24HOUR']
    btcgldd = json_data2['RAW'][str(crypto_coin)]['USD']['CHANGEPCTHOUR']
    btcglee = json_data2['RAW'][str(crypto_coin)]['USD']['PRICE']
    #convert values
    coin_price = float(btcglee)
    coin_marketcap = int(btcglbb)
    coin_volume24h = int(coin_volume24h)
    coin_change_pct24h = float(btcglcc)
    coin_change_pct1h = float(btcgldd)
    return coin_volume24h, coin_marketcap, coin_change_pct24h, coin_change_pct1h, coin_price

#healthcheck pings
#error ping
def healthcheck_error():
    urllib.request.urlopen(healthchecks_fail_url)
    return
#success ping
def healthcheck_okcheck():
    urllib.request.urlopen(healthchecks_okcheck_url)
    return  

#background timer loop
@client.event
async def background_loop():
    #initiating
    keeprunning = 1
    data_counter = 0 #keeps track of data order under activity presence
    #run forever if discord client is ready
    while keeprunning == 1:
        try:
            data_counter += 1
            await client.wait_until_ready()
            #fetch crypto data
            coin_volume24h, coin_marketcap, coin_change_pct24h, coin_change_pct1h, coin_price = get_latest_crypto_data()
            #change bot nickname value
            nickname_price = str(crypto_coin) + " ${:.2f}".format(coin_price)
            #edit data that appears according to each phase, under discord user activity section                      
            if data_counter == 1:
                if len(str(coin_volume24h)) < 6:
                    activity_data = "Vol: ${:.}".format(coin_volume24h)

                #convert values to millions and billions
                elif len(str(coin_volume24h)) > 9:
                    coin_volume24h = coin_volume24h / 1000000000
                    activity_data = "Vol: ${:.2f} bil".format(coin_volume24h)
                elif len(str(coin_volume24h)) > 6:
                    coin_volume24h = coin_volume24h / 1000000
                    activity_data = "Vol: ${:.2f} mil".format(coin_volume24h)
            elif data_counter == 2:
                if len(str(coin_marketcap)) < 6:
                    activity_data = "MCAP: ${:f}".format(coin_marketcap)
                elif len(str(coin_marketcap)) > 9:
                    coin_marketcap = coin_marketcap / 1000000000
                    activity_data = "MCAP: ${:.2f} bil".format(coin_marketcap)
                elif len(str(coin_marketcap)) > 6:
                    coin_marketcap = coin_marketcap / 1000000
                    activity_data = "MCAP: ${:.2f} mil".format(coin_marketcap) 

            elif data_counter == 3:
                activity_data = "Change 24h: " + "%.2f" % coin_change_pct24h + '%'
            elif data_counter == 4:
                activity_data = "Change 1h: " + "%.2f" % coin_change_pct1h + '%'      
                #last value, reset counter          
                data_counter = 0

            #change activity presence
            await client.change_presence(activity=discord.Game(name=activity_data, type=0, url=''))
            #go through each server the bot is currently in, then edit its own nickname to project the price changes
            for g in client.guilds:
                try:
                    #Remember to set this on conf section.
                    member = g.get_member(int(discord_bot_user_id))
                    #edit bot nickname
                    await member.edit(nick=nickname_price) 
                except Exception as e: 
                    print(e) 
            if enable_healthchecksio_monitoring == 1:
            #healthcheck ping         
                healthcheck_okcheck()     
            #wait sleep seconds, set in conf
            await asyncio.sleep(nickname_refresh_period)
        except Exception as e: 
            print(e)
            if enable_healthchecksio_monitoring == 1:
            #healthcheck fail ping
                healthcheck_error()
            #timeout 3 minutes on error
            await asyncio.sleep(180)            
    return

def Main():
    # log in as bot
    #client.loop.create_task(background_loop())
    client.run(discord_token)   

if __name__ == "__main__":

    Main()
