"""Variables and functions for I/O tasks"""

# VARIABLES

DATA_PATH = 'data'
INPUT_FILE = 'twitter_reduced.csv'
PROCESSED_FILE = 'twitter_processed.csv'

MENU = """
Start execution PEC 4 - Ana Blanco - Twitter NLP

Select one option
-----------------
[1] Run all PEC
[2] Run all PEC step by step
[3] Run PEC starting on Data Analysis (Ej 5)
[4] Run PEC starting on Data Analysis (Ej 5) step by step
[0] Exit
"""


# FUNCTIONS

def stop_between_steps(opt, step):
    step += 1
    if opt in [2, 4]:
        input(f'Press any key to continue the EX {step}: ')
    return step
