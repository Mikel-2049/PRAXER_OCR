from fuzzywuzzy import fuzz

def is_similar(actual, expected, threshold=80):
    """Check if the actual string is similar to the expected string."""
    return fuzz.ratio(actual, expected) >= threshold