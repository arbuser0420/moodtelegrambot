from datetime import datetime
from database import create_table, save_mood, get_moods
import telebot;
from telebot import types
from random import choice

jokes = [ 
    "Почему у Python нет лапок? Чтобы не писали 'ноги'.",
    "Программист заходит в бар, заказывает 1 пиво. Потом заказывает 10 пива, потом 100 пива... Ошибка сегментации.",
    "Баг-репорты — как золото. Но нам платят, чтобы мы его игнорировали.",
    "Программисты не умирают, они просто выходят из цикла.",
    "Сидят как-то два дракона в бане:  \n — Что-то жарко стало! \n — А ты пасть закрой!",
    "Нашедшего мой паспорт прошу по-человечески, не смейтесь над фотографией.",
    "Жизнь слишком коротка, чтобы давать названия слоям в фотошопе...",
    "Вчера смотрел Петросяна. Два часа ржал, пока мама фотографию не порвала.",
    "В первую очередь, ты для нее должен стать хорошим фотографом, а уж потом - поддержкой и опорой.",
    "По берегу идет мужчина с фотоаппаратом. К нему подбегает женщина:\n- Идите скорее, моя подруга тонет!\n- Увы, у меня уже кончилась пленка..."
]

recommendations = {
    "1": [
        "Погуляйте на свежем воздухе. Это поможет вам почувствовать себя лучше.",
        "Попробуйте короткую медитацию или глубокое дыхание, чтобы успокоиться.",
        "Послушайте любимую музыку или посмотрите что-нибудь приятное."
    ],
    "2": [
        "Выпейте чашку чая или кофе в спокойной обстановке.",
        "Поговорите с другом или близким человеком.",
        "Сделайте что-то небольшое, что вам нравится: рисование, чтение или просмотр фильма."
    ],
    "3": [
        "Продолжайте в том же духе! Возможно, попробуйте что-то новое, чтобы разнообразить день.",
        "Найдите время для небольших физических упражнений — это поднимет настроение ещё выше.",
        "Поставьте себе небольшую цель и достигните её."
    ],
    "4": [
        "Отличное настроение! Сделайте что-то, что давно откладывали — у вас точно всё получится!",
        "Поделитесь своим настроением с близкими.",
        "Составьте планы на будущее или подумайте о новых целях."
    ],
    "5": [
        "Вы на высоте! Празднуйте успехи, и не забывайте делиться счастьем с окружающими.",
        "Попробуйте что-то новое, это не обязательно должны быть сложные занятия, можно, например, начать читать книги, если давно не читали, или впервые посетить новое место/ поиграть в игру и так далее",
        "Отдохните или займитесь любимым хобби, чтобы сохранить это состояние."
    ]
}


bot = telebot.TeleBot('7746589967:AAHCtO4l5WNNhiIVsolXjS5ler2It-lcFpY')

create_table()

menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
trackmood = types.KeyboardButton("Отследить настроение")
statistic = types.KeyboardButton("Моя статистика")
recommend = types.KeyboardButton("Рекомендации")
joke = types.KeyboardButton("Анекдот для вас")
advices = types.KeyboardButton("Ваши предложения и жалобы")
menu.add(trackmood, statistic, recommend, joke, advices)

back = types.ReplyKeyboardMarkup(resize_keyboard = True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, "Привет! Здесь ты можешь отслеживать своё настроение", reply_markup = menu)

@bot.message_handler(content_types = ['text'])
def text_message(message):
  if message.text == "Назад":
    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup = menu)
  elif message.text == "Отследить настроение":
    bot.send_message(message.chat.id, "Как вы себя сегодня чувствуете? Оцените ваше состояние от 1  до 5 ", reply_markup = back)
    bot.register_next_step_handler(message, mood_input)
  elif message.text == "Моя статистика":
    moods = get_moods(message.chat.id)
    if moods:
      stats = "\n".join([f"{date}: Ваше настроение на тот момент было на {mood}" for date, mood in moods])
      bot.send_message(message.chat.id, f"Статистика вашего самочуствия такова: \n{stats}", reply_markup = back)
    else:
      bot.send_message(message.chat.id, "poka dannih net", reply_markup = back)
  elif message.text == "Рекомендации":
    bot.send_message(message.chat.id, "Выберите состояние, для которого нужны рекомендации (1 - Плохое, 2 - Так себе, 3 - Среднее, 4 - Хорошее, 5 - Отличное):", reply_markup = back)
    bot.register_next_step_handler(message, show_recommendation)
  elif message.text == "Анекдот для вас":
    bot.send_message(message.chat.id, choice(jokes), reply_markup = back)
  elif message.text == "Ваши предложения и жалобы":
    bot.send_message(
        message.chat.id,
        "Что вам хотелось бы видеть в боте? Вы также можете просто выговориться. Слушаем вас!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, forward)


def forward(message):
  bot.forward_message(chat_id='-1002392117833', from_chat_id = message.chat.id, message_id = message.id)
  bot.send_message(message.chat.id, "Спасибо!", reply_markup = menu)


def mood_input(message):
  try:
    mood_rating = int(message.text)
    if 1 <= mood_rating <= 5:
      date = datetime.now().strftime('%Y - %m - %d')
      save_mood(message.chat.id, date, mood_rating)
      if mood_rating == 1:
        bot.send_message(message.chat.id, "Сегодня совсем плохо? Не волнуйся, прорвёшься", reply_markup=back)
      elif mood_rating == 2:
        bot.send_message(message.chat.id, "Не самый лучший день. Но дни меняются :)", reply_markup=back)
      elif mood_rating == 3:
        bot.send_message(message.chat.id, "Стабильность тоже важна.", reply_markup=back)
      elif mood_rating == 4:
        bot.send_message(message.chat.id, "Хорошее настроение. Рады, что вы справляетесь! :)", reply_markup=back)
      elif mood_rating == 5:
        bot.send_message(message.chat.id, "Сегодня вы на высоте", reply_markup=back)
      else:
        bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 5", reply_markup=back)
        bot.register_next_step_handler(message, mood_input)
  except ValueError:
    bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 5", reply_markup=back)
    bot.register_next_step_handler(message, mood_input)

def show_recommendation(message):
  state = message.text.strip()
  if state in recommendations:
    advice ="\n\n".join(recommendations[state])
    bot.send_message(
      message.chat.id,
      f"Рекомендации для состояния {state}:\n\n{advice}",
      reply_markup=back
    )
  else:
    bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 5.", reply_markup=back)
    bot.register_next_step_handler(message, show_recommendation)

bot.infinity_polling()