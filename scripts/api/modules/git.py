import re
import fnmatch

def name_match_filter(name, filter):
    if filter == "*":
        return True
    sep_filters = [x.strip() for x in filter.split(',')]
    for f in sep_filters:
        if fnmatch.fnmatch(name, f):
            return True
    return False
