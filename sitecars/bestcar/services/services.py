import random
import string


def generate_slug(length:int):
    """
        јвтоматическо¤ генераци¤ slug,
        если он отсутствует
    """
    all_symbols = string.ascii_uppercase + string.digits
    return "".join(random.choice(all_symbols) for i in range(length))