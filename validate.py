from difflib import SequenceMatcher

def find_id(data):
    index = 0
    for item in data:
        if ((len(str(item)) == 8) and 
            (item[0] == "5") and 
            (item[1] == "8")):
            break
        index += 1 
    if (index >= len(data)):
        return -1
    return index


def university_name_validate(a, b):
    ratio = SequenceMatcher(None, a, b).ratio()
    if (ratio > 0.7):
        return True
    return False