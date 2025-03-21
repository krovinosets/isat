import os
import telebot
from telebot import types
from dotenv import load_dotenv

from hard import gpt

load_dotenv()


TOKEN_BOT = os.getenv('TOKEN_TELE')
TOKEN_YA_SERVICE = os.getenv('TOKEN_YA')


def main():
    bot = telebot.TeleBot(TOKEN_BOT)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 'Привет я супер умный ботинок!')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(button_name) for button_name in ['Запрос к гпт', 'Гэмблинг']])

        bot.send_message(message.chat.id, 'Что выбираешь?', reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def response(message):
        if gpt.is_url_valid(message.text):
            title, text = gpt.do(message.text)
            bot.send_message(message.chat.id, f"{title}\n{text}")

        match message.text:
            case "Запрос к гпт":
                bot.send_message(message.chat.id, "отправьте ссылку на страницу, чтобы узнать кратко, что на ней")
            case "Гэмблинг":
                bot.send_dice(message.chat.id, "🎰")
                bot.send_message(message.chat.id, 'Вы выбрали гэмблинг 🤙')

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
