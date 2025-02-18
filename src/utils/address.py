from pytoniq_core import Address, AddressError


def validate_address(wallet: str) -> bool:
    try:
        Address(wallet)
    except AddressError:
        return False
    return True
