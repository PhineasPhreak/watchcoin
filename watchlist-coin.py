#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Docs : https://www.coingecko.com/en/api/documentation
# Our Free API* has a rate limit of 50 calls/minute.
#


import argparse
import textwrap

import requests


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description=textwrap.dedent('''\
The Most Comprehensive Cryptocurrency API
Powered by the world’s largest independent crypto data aggregator'''))


parser.add_argument('-p', '--ping', action='store_true',
                    help='Check API server status (defaults)',)
parser.add_argument('-s', '--supported_currencies', action='store_true',
                    help='Get list of supported_vs_currencies')

parser.add_argument('--markets', nargs=5, metavar=('vs_currencies', 'order', 'per_page', 'page', 'sparkilne'),
                    help='''\
Use this to obtain all the coins market data (price, market cap, volume)''')



# Group for verbose or quiet
output = parser.add_mutually_exclusive_group()
# output.add_argument('-q', '--quiet', action='store_true', help='print quiet')
output.add_argument('-v', '--verbose', action='store_true',
                    help='Increase output visibility')
args = parser.parse_args()


# Requests URL server Coingecko
requests_ping = 'https://api.coingecko.com/api/v3/ping'
requests_sp = 'https://api.coingecko.com/api/v3/simple/supported_vs_currencies'


def check_api(visibility='quiet'):
    """Check API server status"""
    cg_ping = requests_ping
    answer_ping = requests.get(cg_ping).status_code
    if visibility == 'quiet':
        return answer_ping
    elif visibility == 'verbose':
        return f'Check API server status : {answer_ping}'


def supported_currencies():
    """Get list of supported_vs_currencies"""
    cg_sp = requests_sp
    answer_sp = requests.get(cg_sp).json()
    return answer_sp


def markets(vs_currencies='usd', order='market_cap_desc', per_page='250', page='1', sparkline='false'):
    """List all supported coins price, market cap, volume, and market related data"""

    # vs_currencies = 'usd'
    # order = 'market_cap_desc'
    # per_page = '250'
    # page = '1'
    # sparkline = 'false'

    cg_markets = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currencies}' \
                 f'&order={order}&per_page={per_page}&page={page}&sparkline={sparkline}'
    answer_markets = requests.get(cg_markets).json()
    return answer_markets


# Only if i use the 'quiet' argument
#################################################################
# if args.quiet:
#     if args.ping:
#         print(check_api(visibility='quiet'))
#
#     elif args.supported_vs_currencies:
#         print(supported_currencies(visibility='quiet'))
#################################################################


if args.verbose:
    if args.ping:
        print(check_api(visibility='verbose'))

else:
    if args.ping:
        print(check_api())

    elif args.supported_currencies:
        print(supported_currencies())

    elif args.markets:
        print(markets(vs_currencies=args.markets[0],
                      order=args.markets[1],
                      per_page=args.markets[2],
                      page=args.markets[3],
                      sparkline=args.markets[4]
                      ))
