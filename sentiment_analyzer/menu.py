"""Variables and functions for I/O tasks"""

import os

# VARIABLES

DATA_PATH = 'data'
INPUT_FILE = 'twitter_reduced.csv'
INPUT_FILE_URL = 'https://eimtgit.uoc.edu/prog_datasci_2/activities/activity_4/-/blob/master/data/twitter_reduced.zip'
PROCESSED_FILE = 'twitter_processed.csv'

MENU = """
Start execution PEC 4 - Ana Blanco - Twitter NLP

Select one option
-----------------
[1] Run all PEC
[2] Run all PEC step by step
[3] Run PEC starting on Data Analysis (Ex. 5)
[4] Run PEC starting on Data Analysis (Ex. 5) step by step
[0] Exit
"""


# FUNCTIONS

def file_exists(filename: str, path: str = DATA_PATH) -> bool:
    """
    Checks if a file path exists
    :param filename: name of the file
    :param path: path of the file
    :return: boolean whether the file path exists
    """
    file_path = os.path.join(path, filename)
    return os.path.exists(file_path)


def stop_between_steps(opt: int, step: int) -> int:
    """
    Stop the program's execution until a key is pressed by the user and return the next step number
    :param opt: option selected by user from menu
    :param step: the number of the last step executed
    :return: next step number
    """
    step += 1
    if opt in [2, 4]:
        input(f'Press any key to continue the EX {step}: ')
    return step
