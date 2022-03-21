# `watchcoin.py` API for Crypto from [Coingecko.com](https://www.coingecko.com/)
CoinGecko provides a fundamental analysis of the crypto market. In addition to tracking price, volume and market capitalisation, 
CoinGecko tracks community growth, open-source code development, major events and on-chain metrics.

* [coingecko](https://www.coingecko.com/)
* [API Documentation](https://www.coingecko.com/en/api/documentation)

# Development
Used **Python3.8**
* `pip3` packages 
  * requests
  * pandas

## Installation
Use the script `start.sh`
```console
./start.sh
```

or

Install manually
```console
python3 -m venv .env  # Create virtual environment
source .env/bin/activate  # Active the virtual environment
echo $VIRTUAL_ENV  # Check the virtual environment

pip3 install requests pandas  # Install manually 'requests' and 'pandas'
pip3 install -r requirements.txt  # Install from requirements.txt file
```