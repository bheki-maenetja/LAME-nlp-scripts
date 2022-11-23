# Third-Party Imports
# Standard Library Imports
from math import inf
# Local Imports

## Query Input
def get_text_cli(
    input_prompt, 
    error_prompt="Please enter a valid input", 
    max_length=inf, 
    min_length=0, 
    accept_values=None):

    user_error = False
    while True:
        try:
            string = input(
                f"{input_prompt if not user_error else error_prompt}: "
            ).lower()
            if accept_values != None and string not in accept_values: 
                raise ValueError
            if len(string) > max_length or len(string) < min_length: 
                raise ValueError
        except ValueError:
            user_error = True
        else:
            break
    
    return string