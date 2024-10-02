import os
import sys
import importlib.util

""" 
    Description
    -----------

    This is a general component for working with the VIX. It can be used to check the 
    VIX, VIX 1D, VIX RSI, VIX percentile values and more.
"""

class ConfigsHelper:
    def __init__(self, configs_folder: str = "configurations"):
        """ 
            Initialize the ConfigsHelper class.

            Parameters
            ----------
            configs_folder : str
                The folder where the configs are stored. Default is "configurations".

            Returns
            -------
            None
        """

        # Get the current directory of where the script is running (the original script that is calling this class)
        current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        # Create the full parameters directory
        configs_dir = f'{current_dir}/{configs_folder}'

        # Check if the parameters directory exists
        if not os.path.exists(configs_dir):
            # If it doesnt exist, throw an error
            raise Exception(f"Configs directory {configs_dir} does not exist")

        # Set the configs directory
        self.configs_dir = configs_dir

    def load_config(self, config_name: str):
        """ 
            Load the parameters from a configuration file.

            Parameters
            ----------
            config_name : str
                The name of the configuration file.

            Returns
            -------
            dict
                The parameters from the configuration file
        """

        # Get the configuration file
        spec = importlib.util.spec_from_file_location(config_name, f"{self.configs_dir}/{config_name.lower()}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # If the configuration file does not have a parameters attribute, throw an error
        if not hasattr(module, 'parameters'):
            raise Exception(f"Configuration file {config_name} does not have a parameters attribute")

        # Get the parameters from the configuration file
        parameters = module.parameters

        # Print in green that we have loaded the configuration file
        print(f"\033[92mLoaded configuration file {config_name}\033[0m")

        return parameters

        
