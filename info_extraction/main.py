# Third-Party Imports
# Standard Library Imports
# Local Imports
from queries import get_text_cli

if __name__ == "__main__":
    text = get_text_cli("Please enter some text", min_length=1)
    