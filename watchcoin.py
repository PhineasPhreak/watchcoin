#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Docs : https://www.coingecko.com/en/api/documentation
# Our Free API* has a rate limit of 50 calls/minute.


import argparse
import textwrap
import sourceapi


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
sc.add_argument('-s', '--supported-currencies', action='store_true',
                help='Get list of supported_vs_currencies')

# Command for categories_list
sl = parser.add_argument_group('View categories lists')
sl.add_argument('-l', '--categories-list', action='store_true',
                help='List all categories')
sl.add_argument('-f', '--format', choices=['table', 'json'], default='table',
                help='The format is "json", "table" default is "table"')

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
mo = markets.add_argument_group('Markets Options',
                                'Use this to obtain all the coins market data'
                                ' (price, market cap, volume)')
mo.add_argument('-c', '--vs_currencies',
                default='usd',
                metavar='usd',
                help='The target currency of '
                     'market data (usd, eur, jpy, etc.) default is usd')
mo.add_argument('-C', '--category',
                default='false',
                metavar='None',
                help='filter by coin category. '
                     'Refer to (/coin/categories/list) default is None')
mo.add_argument('-o', '--order',
                default='market_cap_desc',
                metavar='market_cap_desc',
                help='''valid values: market_cap_desc, gecko_desc, gecko_asc,
                market_cap_asc, market_cap_desc, volume_asc, volume_desc,
                id_asc, id_desc''')
mo.add_argument('-p', '--per-page',
                default='250',
                metavar='250',
                help='''valid values: 1..250 Total results per page''')
mo.add_argument('-P', '--page',
                default='1',
                metavar='1',
                help='Page through results defaults is 1')
mo.add_argument('-s', '--sparkline',
                default='false',
                metavar='false',
                help='Include sparkline 7 days data '
                     '(eg.true, false) default is false')

out_o = markets.add_argument_group('Output Options',
                                   'Configuration of the output display')
out_o.add_argument('-r', '--rows',
                   default='10',
                   metavar='numbers',
                   help='Show the numbers of line for the table')

out_o.add_argument('-m', '--max-columns',
                   default='0',
                   metavar='numbers',
                   help='Show the max columns for the table')


# Option PRICE
price = subparser.add_parser('price',
                             help='Get the current price of any '
                                  'cryptocurrencies in any other supported '
                                  'currencies that you need.')
p_cmd = price.add_argument_group('Price Options')
p_cmd.add_argument('-id', '--ids')


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
        print(sourceapi.check_api(visibility='verbose'))

else:
    if args.ping:
        print(sourceapi.check_api())

    elif args.supported_currencies:
        print(sourceapi.supported_currencies())

    elif args.categories_list:
        print(sourceapi.categories_list(output_format=args.format))

    elif args.command == 'markets':
        sourceapi.check_args(args_str=[args.vs_currencies, args.category,
                                       args.order, args.sparkline],
                             args_int=[args.per_page, args.page, args.rows,
                                       args.max_columns])
        try:
            print(sourceapi.markets(vs_currencies=args.vs_currencies,
                                    category=args.category,
                                    rows=args.rows,
                                    columns=args.max_columns,
                                    order=args.order,
                                    per_page=args.per_page,
                                    page=args.page,
                                    sparkline=args.sparkline))

        except Exception as error:
            print(f'\nWrong request, check the completeness '
                  f'of the arguments and start again\n'
                  f'Error Message : {error}')
