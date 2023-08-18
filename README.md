## Discord sidebar - crypto pricebots
Discord sidebar price bots for crypto. Will show latest price, volume, market cap, percentage of change for 24h and 1h. 

## Environmental Variables

**discord_token** - Your discord bot token. https://discord.com/developers/applications <br>
**discord_bot_user_id** - Your discord's user ID<br>
**cryptocompare_api_key** - Cryptocompare api key. https://www.cryptocompare.com/cryptopian/api-keys<br>
**crypto_coin** - Crypto ticker to check for. Please use coin ticker, and not full name example: LTC <br>
**nickname_refresh_period** - How often to update stats, in seconds. Do not set lower than 45 seconds or there might be throttling issues.<br>
**enable_healthchecksio_monitoring** - Enable with 1, disable with 0. https://healthchecks.io/docs<br>
**healthchecks_fail_url** - Healthchecks.io error url<br>
**healthchecks_okcheck_url** - Healthchecks.io success url<br>

You can specify these environment variables when starting the container using the `-e` command-line option as documented
[here](https://docs.docker.com/engine/reference/run/#env-environment-variables):
```bash
docker run -e "discord_token=yyyy"
```

## Building the container

After having cloned this repository, you can run
```bash
docker build -t crypto-sidebar-pricebot .
```

## Running the container

```bash
docker run -d -e "discord_token=yyy" -e "discord_bot_user_id=yyy" -e "cryptocompare_api_key=yyyy" -e "crypto_coin=yyy" crypto-sidebar-pricebot

```

![](https://github.com/TivenTux/crypto-sidebar-pricebot/blob/main/pricebots_demo.gif)