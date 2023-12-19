import requests
import matplotlib.pyplot as plt
import time


# function to get the prices of cryptocurrencies
def get_prices(cryptos):
    prices = {}
    for crypto in cryptos:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd')
        prices[crypto] = response.json()[crypto]['usd']
    return prices


def get_crypto_data(crypto_name):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_name}'
    response = requests.get(url)
    data = response.json()
    return data


# Example usage
bitcoin_data = get_crypto_data('bitcoin')
if bitcoin_data:
    name = bitcoin_data['name']
    market_cap = bitcoin_data['market_data']['market_cap']['usd']
    current_price = bitcoin_data['market_data']['current_price']['usd']
    total_volume = bitcoin_data['market_data']['total_volume']['usd']

    print(f"Name: {name}")
    print(f"Market Cap: ${market_cap}")
    print(f"Current Price: ${current_price}")
    print(f"Total Volume: ${total_volume}")
else:
    print("Failed to retrieve cryptocurrency data")


# function to monitor cryptocurrencies
def monitor_cryptos(cryptos, interval, duration):
    times = {crypto: [] for crypto in cryptos}
    prices = {crypto: [] for crypto in cryptos}

    for _ in range(duration):
        current_prices = get_prices(cryptos)
        for crypto in cryptos:
            price = current_prices[crypto]
            print(f'The current price of {crypto} is: {price} USD')
            prices[crypto].append(price)
            times[crypto].append(time.time())
        time.sleep(interval)

    for crypto in cryptos:
        plt.plot(times[crypto], prices[crypto], label=crypto)

    plt.title('Cryptocurrency prices over time')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()


# monitor the price of bitcoin and ethereum every 60 seconds for 10 minutes
monitor_cryptos(['bitcoin', 'ethereum'], 60, 10)
