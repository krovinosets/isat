from pprint import pprint
import telebot
import requests

# Конфигурация
TELEGRAM_TOKEN: str = ''
# где client_id - поменять на app id от vk api
# https://oauth.vk.com/authorize?client_id=APP_ID_INSERT_HERE&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,offline&response_type=token&v=5.131
VK_ACCESS_TOKEN: str = ''
VK_USER_ID: str = ''  # Числовой идентификатор пользователя

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_last_post_id():
    """Получаем ID последнего поста на стене"""
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': VK_USER_ID,
        'count': 1,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()
    print(response)
    return response['response']['items'][0]['id']


def send_to_vk_comment(message_text):
    """Отправка комментария к последнему посту"""
    post_id = get_last_post_id()
    print(post_id)
    url = 'https://api.vk.com/method/wall.createComment'
    params = {
        'owner_id': VK_USER_ID,
        'post_id': post_id,
        'message': message_text,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.131'
    }
    pprint(params)
    resp = requests.post(url, params=params)
    print(resp.status_code, resp.text)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        send_to_vk_comment(message.text)
        bot.reply_to(message, '✅ Комментарий успешно добавлен!')
    except Exception as e:
        bot.reply_to(message, f'❌ Ошибка: {str(e)}')


if __name__ == "__main__":
    bot.polling(none_stop=True)
