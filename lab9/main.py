import telebot
from telebot import types
import time

from tqdm import tqdm

TOKEN = 'TG_TOKEN'
ADMIN_ID = 11111111
bot = telebot.TeleBot(TOKEN)

poll_data = {
    'question': "Тестовое голосование:",
    'options': ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4", "Вариант 5"]
}
votes = {option: 0 for option in poll_data['options']}
voted_users = {}
subscribers = set()


def make_keyboard(user_id=None):
    markup = types.InlineKeyboardMarkup()
    for option in poll_data['options']:
        count = votes[option]

        status = "✅" if user_id and voted_users.get(user_id) == option else ""
        btn = types.InlineKeyboardButton(
            text=f"{option} ({count}) {status}",
            callback_data=option
        )
        markup.add(btn)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    subscribers.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"📊 {poll_data['question']}\n\n⚠️ Можно голосовать только 1 раз!",
        reply_markup=make_keyboard(message.from_user.id)
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_vote(call):
    if call.from_user.id in voted_users:
        bot.answer_callback_query(call.id, "❌ Вы уже проголосовали!", show_alert=True)
        return

    chosen_option = call.data
    votes[chosen_option] += 1
    voted_users[call.from_user.id] = chosen_option

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📊 {poll_data['question']}\n\n✅ Ваш выбор: {chosen_option}",
        reply_markup=make_keyboard(call.from_user.id)
    )


@bot.message_handler(commands=['setpoll'])
def set_poll(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Команда только для администратора!")
        return

    try:
        _, question, *options = message.text.split(';')
        if len(options) < 5:
            raise ValueError

        poll_data['question'] = question.strip()
        poll_data['options'] = [o.strip() for o in options]
        votes.clear()
        votes.update({option: 0 for option in poll_data['options']})
        voted_users.clear()

        bot.reply_to(message,
                     f"✅ Опрос обновлен!\nВопрос: {poll_data['question']}\nВарианты: {', '.join(poll_data['options'])}")
    except Exception as e:
        print(f"Ошибка setpoll: {e}")
        bot.reply_to(message,
                     "❌ Неверный формат! Используй:\n/setpoll ; Вопрос ; Вариант 1 ; Вариант 2 ; ... ; Вариант 5")


@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return

    success = 0
    print("Sending direct messages to users")
    for user in tqdm(subscribers, ncols=40):
        try:
            bot.send_message(user,
                             f"📢 Новое голосование!\n\n{poll_data['question']}",
                             reply_markup=make_keyboard())
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"Ошибка broadcast: {e}")
    bot.reply_to(message, f"✅ Рассылка завершена! Получили {success} пользователей")


bot.infinity_polling()
