from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from lumibot.entities import Asset, TradingFee, Order
from sqlalchemy import create_engine
import pandas as pd
import os
import importlib.util
import termcolor
import requests
from datetime import datetime

from lumibot.credentials import IS_BACKTESTING, DB_CONNECTION_STR

from components.configs_helper import ConfigsHelper

# Set the backtesting config file to use
BACKTESTING_CONFIG = "tqqq_spy"
BACKTESTING_START = datetime(2014, 1, 1)
BACKTESTING_END = datetime(2024, 10, 1)

"""
Strategy Description


"""

###################
# Configuration
###################

class StockExampleAlgo(Strategy):
    # =====Overloading lifecycle methods=============

    parameters = {
        # Example of parameters that can be set in the strategy, see teh configurations folder for working examples
        # "symbols": ["AAPL"], # The stock symbols we are using
    }

    def initialize(self):
        # Setting the sleep time (in days) - this is the time between each trading iteration
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        # Get the parameters
        symbols = self.parameters.get("symbols")

        # Check if it's the first iteration
        if self.first_iteration:
            # Get the cash available
            cash = self.get_cash()

            # Calculate the cash per asset
            cash_per_asset = cash / len(symbols)

            # Loop through the symbols
            for symbol in symbols:
                # Get the price of the asset
                price = self.get_last_price(symbol)

                # Calculate the number of shares to buy
                shares_to_buy = int(cash_per_asset / price)

                # Create the order
                order = self.create_order(symbol, shares_to_buy, Order.OrderSide.BUY)

                # Submit the order
                self.submit_order(order)


if __name__ == "__main__":
    if IS_BACKTESTING:
        ####
        # Backtesting
        ####

        from lumibot.backtesting import YahooDataBacktesting

        # 0.1% fee
        trading_fee = TradingFee(percent_fee=0.001)

        # Create the configs helper
        configs_helper = ConfigsHelper()

        # Load the live config
        params = configs_helper.load_config(BACKTESTING_CONFIG)

        # Set the parameters for the strategy
        StockExampleAlgo.parameters = params

        # Backtesting
        result = StockExampleAlgo.backtest(
            YahooDataBacktesting,
            BACKTESTING_START,
            BACKTESTING_END,
            buy_trading_fees=[trading_fee],
            sell_trading_fees=[trading_fee],
        )
    else:
        ####
        # Live Trading
        ####
        from lumibot.credentials import broker, LIVE_CONFIG

        # Check if the LIVE_CONFIG environment variable is set
        if not LIVE_CONFIG:
            raise ValueError("Please specify the LIVE_CONFIG environment variable")

        # Create the configs helper
        configs_helper = ConfigsHelper()

        # Load the live config
        params = configs_helper.load_config(LIVE_CONFIG)

        trader = Trader()
        strategy = StockExampleAlgo(
            broker=broker,
            parameters=params,
            discord_account_summary_footer=
        "Positions and trades are hidden for this algorithm for legal reasons. To access this algorithm you will need a subscription to Alpha Picks [seekingalpha.com/alpha-picks](https://seekingalpha.com/alpha-picks)\n"
        "This strategy code is available as part of the [**Pro Plan**](<https://lumiwealth.com/pro-plan/>)\n"
        "If you have the Starter Plan or higher [**Click Here To Run This Strategy**](<https://github.com/Lumiwealth-Strategies/stock_alpha_picks>)\n"
        "**IMPORTANT:** Access to this algorithm is not automatic. If you get a 404 Error then please contact <@479785401209323535> for us to give you access. Also, make sure you are logged into GitHub.",
            )

        trader.add_strategy(strategy)
        strategies = trader.run_all()