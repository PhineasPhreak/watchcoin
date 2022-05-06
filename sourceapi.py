#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import pandas


# Single requests URL from CoinGecko API
requests_ping = 'https://api.coingecko.com/api/v3/ping'
requests_sp = 'https://api.coingecko.com/api/v3/simple/supported_vs_currencies'
requests_sl = 'https://api.coingecko.com/api/v3/coins/categories/list'


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


def categories_list(output_format):
    """
    List all categories
    """
    if output_format == 'table':
        cg_sl = requests_sl
        pandas.set_option('display.max_rows', None)
        pd_categories = pandas.read_json(cg_sl, orient='records')
        pd_categories_df = pandas.DataFrame(data=pd_categories,
                                            columns=['category_id', 'name'])
        pd_markets_df_index = pd_categories_df.set_index('name')
        return pd_markets_df_index

    elif output_format == 'json':
        cg_sl = requests_sl
        answer_sl = requests.get(cg_sl).json()
        return answer_sl


def markets(category, rows, columns, vs_currencies='usd',
            order='market_cap_desc', per_page='250', page='1',
            sparkline='false'):
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

    if rows and columns:
        # Reset display to the defaults
        pandas.reset_option('display.max_rows')
        pandas.reset_option('display.max_columns')
        pandas.reset_option('display.width')
        pandas.reset_option('display.float_format')
        pandas.reset_option('display.max_colwidth')

        # Config for display for DataFrame
        # https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
        pandas.set_option('display.max_rows', int(rows))
        pandas.set_option('display.max_columns', int(columns))
        pandas.set_option('display.width', 2000)
        pandas.set_option('display.float_format', '{:20,.2f}'.format)
        pandas.set_option('display.max_colwidth', None)

        # with pandas.option_context('display.max_rows', int(rows),
        #                            'display.max_columns', int(columns)):
        #     pass

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
