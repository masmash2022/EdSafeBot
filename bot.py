import telebot
from telebot import types

ans = []
ans_right = ['1', '2', '2', '4', '3', '2', '1', '2']

theme = [0 for i in range(4)]

bot = telebot.TeleBot('5422552101:AAEulv9Yu7XlwT1s2Y8pYsdrVca8841tf74')

# Начало, 2 кнопки: Старт, Тест
@bot.message_handler(commands=["start"])
def start(message, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton("Старт")
    #forward = types.KeyboardButton("Продолжить")
    test = types.KeyboardButton("Тест")
    help = types.KeyboardButton("Помощь")
    markup.add(start, test, help)
    name = message.chat.first_name
    bot.send_message(message.chat.id, f'Привет, {name}. На связи Safe_bot.')
    bot.send_message(message.chat.id, 'Для начала обучения нажми: Старт, при возникновении вопросов по работе бота, нажми: Помощь, чтобы пройти тестирование и начать обучение, нажми: Тест',  reply_markup=markup)

# Обращение к файлу с ответами
f = open('data.txt', 'r')
answer = f.read().split('\n')
f.close()

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower() == 'старт':
        bot.send_message(message.chat.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, age_user)
    elif message.text.lower() == 'тест':
        bot.send_message(message.chat.id, 'Пройти тест? Да/Нет')
        bot.register_next_step_handler(message, question_1)
    elif message.text.lower() == 'помощь':
        bot.send_message(message.chat.id, 'Нажмите Старт, чтобы начать сначала. Нажмите Тест, чтобы начать тестирование и определить темы, которые вы будете изучать')

# Функция получения возраста пользователя
def age_user(message):
    mes_id = 0
    # Проверяем, ввел ли пользователь число? Если нет, то выводится сообщение про некорректный ответ.
    # Все пользователи разбиты на 3 группы:
    #     - до 10 лет,
    #     - от 10 до 18 лет - основная целевая аудитория,
    #     - старше 18 лет.
    if message.text.isdigit() == True:
        if int(message.text) < 10:
            mes_id = 1
        elif 10 <= int(message.text) <= 18:
            mes_id = 2
        elif 18 <= int(message.text) <= 100:
            mes_id = 3
        bot.send_message(message.chat.id, answer[mes_id])
        bot.register_next_step_handler(message, go_to_test)
    # Ожидаем корректного ответа
    else:
        bot.send_message(message.chat.id, answer[0])
        bot.register_next_step_handler(message, age_user)

# Переход к тесту
def go_to_test(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, answer[5])
        bot.register_next_step_handler(message, question_1)
    # Если "нет" - прощаемся
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, answer[4])
    # Ожидаем корректного ответа
    else:
        bot.send_message(message.chat.id, answer[0])
        bot.register_next_step_handler(message, go_to_test)

# Блок тестирования. Предполагаем, что человек вводит корректный ответ
# Вопрос №1
def question_1(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, answer[8])
        bot.register_next_step_handler(message, question_2)
    # Если "нет" - прощаемся
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, answer[4])
# Вопрос №2
def question_2(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[9])
    bot.register_next_step_handler(message, question_3)
# Вопрос №3
def question_3(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[10])
    bot.register_next_step_handler(message, question_4)
# Вопрос №4
def question_4(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[11])
    bot.register_next_step_handler(message, question_5)
# Вопрос №5
def question_5(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[12])
    bot.register_next_step_handler(message, question_6)
# Вопрос №6
def question_6(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[13])
    bot.register_next_step_handler(message, question_7)
# Вопрос №7
def question_7(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[14])
    bot.register_next_step_handler(message, question_8)
# Вопрос №8
def question_8(message):
    ans.append(message.text)
    bot.send_message(message.chat.id, answer[15])
    bot.register_next_step_handler(message, answers)

# Блок сравнивает ответы пользователя с верными ответами и выстраивает траекторию обучения,
# включая в обучающую программу темы в соответствии с ответами пользователя:
# - если все ответы верные, то theme = [0, 0, 0, 0]
# - вопросы 1 и 2 относятся к теме 1:
#       - если ответы на В1 и В2 верные, то theme[0]  = 0
#       - если ответ на В1 верный, а В2 неверные или наоборот, то theme[0]  = 1
#       - если ответы на В1 и В2 неверные, то theme[0]  = 2
# - вопросы 3 и 4 относятся к теме 2:
#       - если ответы на В3 и В4 верные, то theme[1]  = 0
#       - если ответ на В3 верный, а В4 неверные или наоборот, то theme[1]  = 1
#       - если ответы на В3 и В4 неверные, то theme[1]  = 2
# - вопросы 5 и 6 относятся к теме 3:
#       - если ответы на В5 и В6 верные, то theme[2]  = 0
#       - если ответ на В5 верный, а В6 неверные или наоборот, то theme[2]  = 1
#       - если ответы на В5 и В6 неверные, то theme[2]  = 2
# - вопросы 7 и 8 относятся к теме 3:
#       - если ответы на В7 и В8 верные, то theme[3]  = 0
#       - если ответ на В7 верный, а В8 неверные или наоборот, то theme[3]  = 1
#       - если ответы на В7 и В8 неверные, то theme[3]  = 2

def answers(message):
    ans.append(message.text)

    if ans == ans_right:
        bot.send_message(message.chat.id, answer[16])

    if (ans[0] != ans_right[0] and ans[1] == ans_right[1]) or (ans[0] == ans_right[0] and ans[1] != ans_right[1]):
        theme[0] = 1
    elif ans[0] != ans_right[0] and ans[1] != ans_right[1]:
        theme[0] = 2
    else:
        theme[0] = 0

    if (ans[2] != ans_right[2] and ans[3] == ans_right[3]) or (ans[2] == ans_right[2] and ans[3] != ans_right[3]):
        theme[1] = 1
    elif ans[2] != ans_right[2] and ans[3] != ans_right[3]:
        theme[1] = 2
    else:
        theme[1] = 0

    if (ans[4] != ans_right[4] and ans[5] == ans_right[5]) or (ans[4] == ans_right[4] and ans[5] != ans_right[5]):
        theme[2] = 1
    elif ans[4] != ans_right[4] and ans[5] != ans_right[5]:
        theme[2] = 2
    else:
        theme[2] = 0

    if (ans[6] != ans_right[6] and ans[7] == ans_right[7]) or (ans[6] == ans_right[6] and ans[7] != ans_right[7]):
        theme[3] = 1
    elif ans[6] != ans_right[6] and ans[7] != ans_right[7]:
        theme[3] = 2
    else:
        theme[3] = 0

    bot.send_message(message.chat.id, answer[17])
    bot.register_next_step_handler(message, generate_theme)

# Генерируем сообщение с предложением изучить темы
def generate_theme(message):
    if message.text.lower() == 'да':
        menu = types.InlineKeyboardMarkup()
        theme_11 = types.InlineKeyboardButton('Конфиденциальные данные 1', callback_data ='theme_11')
        theme_12 = types.InlineKeyboardButton('Конфиденциальные данные 2', callback_data='theme_12')
        theme_21 = types.InlineKeyboardButton('Безопасность аккаунтов 1', callback_data='theme_21')
        theme_22 = types.InlineKeyboardButton('Безопасность аккаунтов 2', callback_data='theme_22')
        theme_31 = types.InlineKeyboardButton('Мошенники в соц.сетях 1', callback_data='theme_31')
        theme_32 = types.InlineKeyboardButton('Мошенники в соц.сетях 2', callback_data='theme_32')
        theme_41 = types.InlineKeyboardButton('Общение в соц.сетях 1', callback_data='theme_41')
        theme_42 = types.InlineKeyboardButton('Общение в соц.сетях 2', callback_data='theme_42')

    # Добавляем кнопки для изучения темы
        if theme == [0, 0, 0, 0]:
            menu.add(theme_11, theme_21, theme_31, theme_41)
        if theme[0] == 1:
            menu.add(theme_11)
        elif theme[0] == 2:
            menu.add(theme_12)
        if theme[1] == 1:
            menu.add(theme_21)
        elif theme[1] == 2:
            menu.add(theme_22)
        if theme[2] == 1:
            menu.add(theme_31)
        elif theme[2] == 2:
            menu.add(theme_32)
        if theme[3] == 1:
            menu.add(theme_41)
        elif theme[3] == 2:
            menu.add(theme_42)

        bot.send_message(message.chat.id, answer[18], reply_markup=menu)

    # Если "нет" - прощаемся
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, answer[4])
    # Ожидаем корректного ответа
    else:
        bot.send_message(message.chat.id, answer[0])
        bot.register_next_step_handler(message, generate_theme)

# Обработка выбора темы. Выдача темы
@bot.callback_query_handler(func=lambda call: True)
def education(call):
    if call.data == 'theme_11':
        bot.send_message(call.message.chat.id, answer[19])
    elif call.data == 'theme_12':
        bot.send_message(call.message.chat.id, answer[20])
    elif call.data == 'theme_21':
        bot.send_message(call.message.chat.id, answer[21])
    elif call.data == 'theme_22':
        bot.send_message(call.message.chat.id, answer[22])
    elif call.data == 'theme_31':
        bot.send_message(call.message.chat.id, answer[23])
    elif call.data == 'theme_32':
        bot.send_message(call.message.chat.id, answer[24])
    elif call.data == 'theme_41':
        bot.send_message(call.message.chat.id, answer[25])
    elif call.data == 'theme_42':
        bot.send_message(call.message.chat.id, answer[26])

# Запуск бота
bot.polling(none_stop=True, interval=0)