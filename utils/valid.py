from utils.config import ALLOW_SYMBOL_EN, ALLOW_SYMBOL_RU

from db.base import AppTable

def valid_symbol(string : str, symbols : str) -> bool:
    """
    Check valud symbol
    """
    for s in string.lower():
        if s in symbols:
            continue

        return False 
    return True


def valid_name(name : str) -> bool:
    """
    validation for name
    """
    if len(name) > 15:
        return False
    
    return valid_symbol(
        name, 
        ALLOW_SYMBOL_RU + ALLOW_SYMBOL_EN
    )


def valid_city(city : str) -> bool: 
    """
    validation for city
    """
    if len(city) > 15:
        return False
    
    return valid_symbol(
        city, 
        ALLOW_SYMBOL_RU + ALLOW_SYMBOL_EN
    )


def valid_years(years : int) -> bool:
    """
    validation for years
    """
    try:
        number = int(years)
    except ValueError:
        return False

    if 18 <= number < 65:
        return True

    return False


def valid_usr(usr : str) -> bool:
    """
    validation for usr
    """
    if not usr.startswith("@"):
        return False

    if not (5 <= len(usr[1:]) < 32):
        return False

    return valid_symbol(
        usr[1:],
        ALLOW_SYMBOL_EN
    )


def valid_non_anon(app : AppTable) -> bool:
    
    if app.photo_id is None:
        return False
    return True