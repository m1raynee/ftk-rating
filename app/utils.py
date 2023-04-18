import re

def parse_tablename(name: str) -> str:
    match = re.findall("[a-zA-Z][^A-Z]*", name)
    if match[-1][-1] == "y":
        match[-1] = match[-1][:-1] + "ies"
    else:
        match[-1] += "s"
    return "_".join(m.lower() for m in match)