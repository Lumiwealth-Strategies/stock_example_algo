import os 

parameters = {
    "config_file_name": os.path.basename(__file__).split(".")[0], # The name of the file
    "symbols": ["TQQQ", "SPY"], # The stock symbol we are using
}