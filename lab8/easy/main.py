import telebot
from telebot import types

TOKEN = 'ВАШ_ТОКЕН'


def main():
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def start(m):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🌍 Природа')
        btn2 = types.KeyboardButton('🔧 Технологии')
        markup.add(btn1, btn2)
        bot.send_message(m.chat.id, 'Добро пожаловать! Выберите категорию:', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def handle_text(m):
        try:
            if m.text == '🌍 Природа':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('🐾 Фауна', '🌿 Флора', '⛰️ Геология')
                bot.send_message(m.chat.id, 'Исследуем природу! Что вас интересует?', reply_markup=markup)

            elif m.text == '🔧 Технологии':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('🤖 Робототехника', '🧠 ИИ', '📱 Гаджеты')
                bot.send_message(m.chat.id, 'Технологии будущего! Выберите раздел:', reply_markup=markup)

            # Ветка Природы
            elif m.text == '🐾 Фауна':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('🦁 Млекопитающие', '🦜 Птицы', '🐠 Рыбы')
                bot.send_message(m.chat.id, 'Удивительный мир животных!', reply_markup=markup)

            elif m.text == '🌿 Флора':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('🌳 Деревья', '🌺 Цветы', '🍄 Грибы')
                bot.send_message(m.chat.id, 'Царство растений!', reply_markup=markup)

            elif m.text == '⛰️ Геология':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('💎 Минералы', '🌋 Вулканы', '🪨 Породы')
                bot.send_message(m.chat.id, 'Тайны земной коры!', reply_markup=markup)

            # Ветка Технологий
            elif m.text == '🤖 Робототехника':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('🏭 Промышленные', '🏥 Медицинские', '👨💻 Домашние')
                bot.send_message(m.chat.id, 'Роботы вокруг нас!', reply_markup=markup)

            elif m.text == '🧠 ИИ':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('📈 Аналитика', '🎨 Творчество', '🔒 Безопасность')
                bot.send_message(m.chat.id, 'Искусственный интеллект сегодня!', reply_markup=markup)

            elif m.text == '📱 Гаджеты':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add('📱 Смартфоны', '⌚ Умные часы', '🎧 Наушники')
                bot.send_message(m.chat.id, 'Новейшие устройства!', reply_markup=markup)

            # Конечные ответы
            elif m.text in ['🦁 Млекопитающие', '🦜 Птицы', '🐠 Рыбы',
                            '🌳 Деревья', '🌺 Цветы', '🍄 Грибы',
                            '💎 Минералы', '🌋 Вулканы', '🪨 Породы',
                            '🏭 Промышленные', '🏥 Медицинские', '👨💻 Домашние',
                            '📈 Аналитика', '🎨 Творчество', '🔒 Безопасность',
                            '📱 Смартфоны', '⌚ Умные часы', '🎧 Наушники']:
                responses = {
                    '🦁 Млекопитающие': 'Млекопитающие - теплокровные животные с развитым мозгом!',
                    '🦜 Птицы': 'Птицы - единственные животные с перьями!',
                    '🐠 Рыбы': 'Рыбы дышат через жабры и живут в воде!',
                    '🌳 Деревья': 'Деревья - легкие нашей планеты!',
                    '🌺 Цветы': 'Цветы - репродуктивные органы растений!',
                    '🍄 Грибы': 'Грибы - отдельное царство живой природы!',
                    '💎 Минералы': 'Минералы - природные твердые вещества!',
                    '🌋 Вулканы': 'Вулканы - окна в недра Земли!',
                    '🪨 Породы': 'Горные породы слагают земную кору!',
                    '🏭 Промышленные': 'Промышленные роботы на заводах!',
                    '🏥 Медицинские': 'Медицинские роботы спасают жизни!',
                    '👨💻 Домашние': 'Домашние роботы помогают в быту!',
                    '📈 Аналитика': 'ИИ анализирует большие данные!',
                    '🎨 Творчество': 'ИИ создает музыку и картины!',
                    '🔒 Безопасность': 'ИИ в кибербезопасности!',
                    '📱 Смартфоны': 'Новейшие модели смартфонов 2025!',
                    '⌚ Умные часы': 'Умные часы с функцией ЭКГ!',
                    '🎧 Наушники': 'Беспроводные наушники с шумоподавлением!'
                }
                bot.send_message(m.chat.id, responses[m.text])

        except Exception as e:
            bot.reply_to(m, 'Ошибка обработки запроса')

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
