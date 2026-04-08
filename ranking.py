import re

def get_experience(text):

    text = text.lower()

    match = re.search(r'(\d+)\s+year', text)

    if match:
        return int(match.group(1))

    return 0