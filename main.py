import telebot
from telebot import types
from extensions import CurrencyConverter, APIException
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = (
        "Привет! Я бот для получения курса валют. \n\n"
        "Чтобы получить цену на валюту, отправьте сообщение в формате:\n"
        "<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n\n"
        "Пример: EUR USD 100\n\n"
        "Чтобы увидеть список доступных валют, введите /values"
    )
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def send_currency_values(message):
    values = "Доступные валюты: EUR, USD, RUB"
    bot.send_message(message.chat.id, values)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base.upper(), quote.upper(), float(amount))
        bot.reply_to(message, f"{amount} {base.upper()} = {result} {quote.upper()}")
    except ValueError:
        bot.reply_to(message, "Неверный формат. Пожалуйста, используйте формат <валюта1> <валюта2> <количество>")
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Обработчик для запуска бота
if __name__ == "__main__":
    bot.polling()
