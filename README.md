# `watchcoin.py` API for Crypto from [Coingecko.com](https://www.coingecko.com/)

# About The Project
CoinGecko provides a fundamental analysis of the crypto market. In addition to tracking price, volume and market capitalisation, 
CoinGecko tracks community growth, open-source code development, major events and on-chain metrics.

* [coingecko](https://www.coingecko.com/)
* [API Documentation](https://www.coingecko.com/en/api/documentation)

Use this `README.md` to get started.

# Getting Started
## Prerequisites
This project was written in python. To be able to run this you must have Python 3 installed. 
To install the required packages you also need to have **pip** or **pip3** installed.

## Installation Prerequisites
Used prerequisites `requests`, `pandas`
```shell
pip3 install -r requirements.txt
```

**OR**, Use the script `start.sh`
```shell
./start.sh
```

---

Installation of the python virtual environment, and the 'requests' and 'pandas' packages
```shell
python3 -m venv .env  # Create virtual environment
source .env/bin/activate  # Active the virtual environment
echo $VIRTUAL_ENV  # Check the virtual environment

pip3 install requests pandas  # Install manually 'requests' and 'pandas'
```

# Usage
To start the program simply run
```shell
python3 watchcoin.py
```
```shell
./watchcoin.py
```