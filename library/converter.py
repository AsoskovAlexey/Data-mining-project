from currency_converter import CurrencyConverter


def convert(price_USD):
    """
    converts prices in USD into ILS with rates available at the moment of conversion
    :param price_USD: price in USD
    :return: price in ISL
    """
    c = CurrencyConverter(fallback_on_missing_rate=True)
    return round(c.convert(price_USD, "USD", "ILS"), 2)
