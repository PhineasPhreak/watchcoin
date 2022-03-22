#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Docs : https://www.coingecko.com/en/api/documentation
# Our Free API* has a rate limit of 50 calls/minute.


import argparse
import textwrap
import requests
import pandas


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description=textwrap.dedent('''\
The Most Comprehensive Cryptocurrency API
Powered by the world’s largest independent crypto data aggregator'''))

# Command for PING
ping = parser.add_argument_group()
ping.add_argument('-p', '--ping', action='store_true',
                  help='Check API server status',)

# Command for SUPPORTED_VS_CURRENCIES
sc = parser.add_argument_group()
sc.add_argument('-s', '--supported_currencies', action='store_true',
                help='Get list of supported_vs_currencies')


# For grouping subparser arguments
# https://stackoverflow.com/questions/32017020/grouping-argparse-subparser-arguments
subparser = parser.add_subparsers(
    dest='command',
    title='All Options',
    description='All the commands you can use',
    help='[%(prog)s markets -h] for more help')

# Option MARKETS
markets = subparser.add_parser('markets',
                               help='List all supported coins price, market '
                                    'cap, volume, and market related data')
cmd = markets.add_argument_group('Markets Options',
                                 'Use this to obtain all the coins market data'
                                 ' (price, market cap, volume)')
cmd.add_argument('-c', '--vs_currencies',
                 default='usd',
                 metavar='usd',
                 help='The target currency of '
                      'market data (usd, eur, jpy, etc.) default is usd')
cmd.add_argument('-C', '--category',
                 default='false',
                 metavar='None',
                 help='filter by coin category. '
                      'Refer to (/coin/categories/list) default is None')
cmd.add_argument('-o', '--order',
                 default='market_cap_desc',
                 metavar='market_cap_desc',
                 help='''valid values: market_cap_desc, gecko_desc, gecko_asc,
                 market_cap_asc, market_cap_desc, volume_asc, volume_desc,
                 id_asc, id_desc''')
cmd.add_argument('-p', '--per-page',
                 default='250',
                 metavar='250',
                 help='''valid values: 1..250 Total results per page''')
cmd.add_argument('-P', '--page',
                 default='1',
                 metavar='1',
                 help='Page through results defaults is 1')
cmd.add_argument('-s', '--sparkline',
                 default='false',
                 metavar='false',
                 help='Include sparkline 7 days data '
                      '(eg.true, false) default is false')


# Option PRICE
price = subparser.add_parser('price',
                             help='Get the current price of any '
                                  'cryptocurrencies in any other supported '
                                  'currencies that you need.')
cmd = price.add_argument_group('Price Options')
cmd.add_argument('-id', '--ids')


# Information version of the python file
parser.add_argument('-V', '--version',
                    action='version',
                    version='%(prog)s version 0.1')

# Group for verbose or quiet
output = parser.add_mutually_exclusive_group()

# output.add_argument('-q', '--quiet', action='store_true', help='print quiet')
output.add_argument('-v', '--verbose',
                    action='store_true',
                    help='increase output visibility')
args = parser.parse_args()


# Requests URL from CoinGecko server
requests_ping = 'https://api.coingecko.com/api/v3/ping'
requests_sp = 'https://api.coingecko.com/api/v3/simple/supported_vs_currencies'


def check_args(args_str, args_int):
    """
    Inspect each argument and warn if it should be a string or a numeric value
    :param args_str: List of arguments that must be a string
    :param args_int: List of arguments that must be a numerical value
    """
    for argument_str in args_str:
        if argument_str.isnumeric():
            print(f"'{argument_str}' is decimal and must be a string, "
                  f"see the help for more information")

    for argument_int in args_int:
        if not argument_int.isnumeric():
            print(f"'{argument_int}' is a string and must be a number, "
                  f"see the help for more information")

    # return print(f"'{argument_str_re}' is decimal and must be a string, "
    #              f"see the help for more information\n"
    #              f"'{argument_int_re}' is a string and must be a number, "
    #              f"see the help for more information")
    return None


def check_api(visibility='quiet'):
    """
    Check API server status
    """
    cg_ping = requests_ping
    answer_ping = requests.get(cg_ping).status_code
    if visibility == 'quiet':
        return answer_ping
    elif visibility == 'verbose':
        return f'Check API server status : {answer_ping}'


def supported_currencies():
    """
    Get list of supported_vs_currencies
    """
    cg_sp = requests_sp
    answer_sp = requests.get(cg_sp).json()
    return answer_sp


def markets(category, vs_currencies='usd', order='market_cap_desc',
            per_page='250', page='1', sparkline='false'):
    """
    List all supported coins price, market cap, volume, and market related data
    https://www.delftstack.com/howto/python-pandas/
    """

    if category == 'false':
        cg_markets = f'https://api.coingecko.com/api/v3/coins/' \
                     f'markets?vs_currency={vs_currencies}&' \
                     f'order={order}&' \
                     f'per_page={per_page}&' \
                     f'page={page}&' \
                     f'sparkline={sparkline}'
    else:
        cg_markets = f'https://api.coingecko.com/api/v3/coins/' \
                     f'markets?vs_currency={vs_currencies}&' \
                     f'category={category}&' \
                     f'order={order}&' \
                     f'per_page={per_page}&' \
                     f'page={page}&' \
                     f'sparkline={sparkline}'

    # Source all data in terminal
    # answer_markets = requests.get(cg_markets).json()

    # Config for display for DataFrame
    # https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
    # pandas.set_option('display.max_rows', None)
    # pandas.set_option('display.max_columns', None)
    # pandas.set_option('display.width', 2000)
    # pandas.set_option('display.float_format', '{:20,.2f}'.format)
    # pandas.set_option('display.max_colwidth', None)

    # Reset display to the defaults
    # pandas.reset_option('display.max_rows')
    # pandas.reset_option('display.max_columns')
    # pandas.reset_option('display.width')
    # pandas.reset_option('display.float_format')
    # pandas.reset_option('display.max_colwidth')

    # Convert json format on DataFrame in pandas
    pd_markets = pandas.read_json(cg_markets, orient='records')

    # For delete column in DataFrame
    # https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
    #
    # Create pandas DataFrame
    pd_markets_df = pandas.DataFrame(data=pd_markets,
                                     columns=[
                                         'id',
                                         'symbol',
                                         'name',
                                         'current_price',
                                         'market_cap',
                                         'market_cap_rank',
                                         'fully_diluted_valuation',
                                         'total_volume',
                                         'high_24h',
                                         'low_24h',
                                         'price_change_24h',
                                         'price_change_percentage_24h',
                                         'market_cap_change_24h',
                                         'market_cap_change_percentage_24h',
                                         'circulating_supply',
                                         'total_supply',
                                         'max_supply',
                                         'last_updated'])

    # Sets the 'market_cap_rank' column as an index of the my_df DataFrame
    pd_markets_df_rank = pd_markets_df.set_index('market_cap_rank')

    # Delete 'image' column in the data Frame
    # pd_markets_df_rank.drop('image', axis=1, inplace=True)

    return pd_markets_df_rank

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

    elif args.command == 'markets':
        check_args(args_str=[args.vs_currencies, args.category,
                             args.order, args.sparkline],
                   args_int=[args.per_page, args.page])
        try:
            print(markets(vs_currencies=args.vs_currencies,
                          category=args.category,
                          order=args.order,
                          per_page=args.per_page,
                          page=args.page,
                          sparkline=args.sparkline))

        except Exception as error:
            print(f'\nWrong request, check the completeness '
                  f'of the arguments and start again\n'
                  f'Error Message : {error}')
