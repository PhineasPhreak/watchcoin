#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import pandas as pd
from timeit import timeit

# LISTING POSSIBLE ERROR:
# requests.exceptions.ConnectionError
# socket.gaierror


class DataFrameCustom:
    """
    Modification of a pandas array for rows and columns option
    """
    def __init__(self, rows, max_columns):
        """Initialization"""
        self.rows = rows
        self.max_columns = max_columns

    def show_table(self):
        # Reset display to the defaults
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
        pd.reset_option('display.float_format')
        pd.reset_option('display.max_colwidth')

        # Config for display for DataFrame
        # https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
        pd.set_option('display.max_rows', int(self.rows))
        pd.set_option('display.max_columns', int(self.max_columns))
        pd.set_option('display.width', 2000)
        pd.set_option('display.float_format', '{:20,.2f}'.format)
        pd.set_option('display.max_colwidth', None)


class Utils:
    # Single requests URL from CoinGecko API
    requests_ping = 'https://api.coingecko.com/api/v3/ping'
    requests_sp = 'https://api.coingecko.com/api/v3/simple/supported_vs_currencies'
    requests_sl = 'https://api.coingecko.com/api/v3/coins/categories/list'

    @staticmethod
    def check_args(args_str, args_int):
        """
        Inspect each argument and warn if it should be a string
        or a numeric value
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

    @staticmethod
    def check_api(visibility='quiet'):
        """
        Check API server status
        """
        cg_ping = Utils.requests_ping
        answer_ping = requests.get(cg_ping).status_code
        tmp_execution = timeit() * 60
        tmp_second = "{:,.2f}sec".format(tmp_execution)

        if visibility == 'quiet':
            return f'Status : {answer_ping} in {tmp_second}'
        elif visibility == 'verbose':
            return f'Check API server Status : {answer_ping} ' \
                   f'in {tmp_execution}'

    @staticmethod
    def supported_currencies():
        """
        Get list of supported_vs_currencies
        """
        cg_sp = Utils.requests_sp
        answer_sp = requests.get(cg_sp).json()
        return answer_sp

    @staticmethod
    def categories_list(output_format):
        """
        List all categories
        """
        if output_format == 'table':
            cg_sl = Utils.requests_sl
            # pd.set_option('display.max_rows', None)
            pd_categories = pd.read_json(cg_sl, orient='records')
            pd_categories_df = pd.DataFrame(data=pd_categories,
                                            columns=['category_id',
                                                     'name'])
            pd_markets_df_index = pd_categories_df.set_index('name')
            return pd_markets_df_index

        elif output_format == 'json':
            cg_sl = Utils.requests_sl
            answer_sl = requests.get(cg_sl).json()
            return answer_sl

    @staticmethod
    def markets(category, rows, columns, vs_currencies='usd',
                order='market_cap_desc', per_page='250', page='1',
                sparkline='false'):
        """
        List all supported coins price, market cap, volume,
        and market related data
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
            dfc = DataFrameCustom(rows=rows, max_columns=columns)
            dfc.show_table()

            # with pandas.option_context('display.max_rows', int(rows),
            #                            'display.max_columns', int(columns)):
            #     pass

        # Convert json format on DataFrame in pandas
        pd_markets = pd.read_json(cg_markets, orient='records')

        # For delete column in DataFrame
        # https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
        #
        # Create pandas DataFrame
        pd_markets_df = pd.DataFrame(data=pd_markets,
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
                                             'last_updated'
                                         ])

        # Sets the 'market_cap_rank' column as an index of the my_df DataFrame
        pd_markets_df_rank = pd_markets_df.set_index('market_cap_rank')

        # Delete 'image' column in the data Frame
        # pd_markets_df_rank.drop('image', axis=1, inplace=True)

        return pd_markets_df_rank

    @staticmethod
    def price(include_market_cap, include_24hr_vol, include_24hr_change,
              include_last_updated_at, ids='bitcoin', vs_currencies='usd'):
        """
        Get the current price of any cryptocurrencies in any other supported
        currencies that you need.
        """
        cg_price = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&' \
                   f'vs_currencies={vs_currencies}&' \
                   f'include_market_cap={include_market_cap}&' \
                   f'include_24hr_vol={include_24hr_vol}&' \
                   f'include_24hr_change={include_24hr_change}&' \
                   f'include_last_updated_at={include_last_updated_at}'

        # Reset display to the defaults
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
        pd.reset_option('display.float_format')
        pd.reset_option('display.max_colwidth')

        # Config for display for DataFrame
        # https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 2000)
        pd.set_option('display.float_format', '{:20,.2f}'.format)
        pd.set_option('display.max_colwidth', None)

        pd_price = pd.read_json(cg_price, orient='records')
        pd_price_df = pd.DataFrame(data=pd_price,
                                   columns=[
                                           f'{ids}',
                                           # f'{vs_currencies}',
                                           # 'include_market_cap',
                                           # 'include_24hr_vol',
                                           # 'include_24hr_change',
                                           # 'include_last_updated_at'
                                       ])

        # pd_price_df_rank = pd_price_df.set_index(f'{ids}')

        return pd_price_df
