import requests

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url)
            data = response.json()
            if quote in data["rates"]:
                return data["rates"][quote] * amount
            else:
                raise APIException(f"Currency '{quote}' is not available.")
        except Exception as e:
            raise APIException(str(e))
