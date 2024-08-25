import configparser
from pathlib import Path
from utils.app_root_dir import app_root_dir
from utils.print_error import print_error


def parse_ini_file(filename, process_sections=False):
    """
    A function for parsing ini files similar to the one in PHP.

    :param filename: Path to ini file
    :param process_sections: Determines whether sections should be processed
    :return: A dictionary containing the parsed values from the ini file or False in case of failure
    """
    if not Path(filename).is_absolute():
        filename = app_root_dir() / filename

    config = configparser.ConfigParser()
    config.optionxform = str.lower  # Setting behavior regarding the case sensitivity of keys

    try:
        if not Path(filename).exists():
            print_error("Error: The specified ini file does not exist.\n")
            return None

        config.read(filename)
        if len(config.sections()) == 1 and not process_sections:
            default_section = config.sections()[0]
            if len(config[default_section]) == 1:
                key, value = next(iter(config[default_section].items()))
                return {key.lower(): value}
            else:
                raise ValueError("In the ini file, there is more than one section. Please provide the second argument.")
        elif process_sections:
            parsed_data = {}
            for section in config.sections():
                parsed_data[section.lower()] = {}
                for key, value in config.items(section):
                    parsed_data[section.lower()][key.lower()] = value
            return parsed_data if parsed_data else False
        else:
            raise ValueError(
                "Provide the second argument (process_sections=True) if the ini file contains more than one section.")
    except (configparser.Error, FileNotFoundError, ValueError) as e:
        print_error("Error parsing the ini file:", e)
        return False
