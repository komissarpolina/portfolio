from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# Токен вашего бота
TOKEN = '_____'

# ID пользователя, которому будем отправлять статистику
SAVEDEC_USER_ID = _____  # Ваш ID пользователя, кому отправляются результаты

# Вопросы и возможные ответы
questions = [
    {
        "question": "Во сколько монет оценили «говорящего осла», когда бабка пришла его продавать?",
        "options": ["5 монет", "10 монет", "15 монет", "20 монет"],
        "right_answer": "10 монет"
    },
    {
        "question": "Что сказал Осел Шреку, когда Шрек накричал на него?",
        "options": ["Иди поспи немного", "Иногда трескай тик-так", "Успокойся и расслабься", "Лучше бы молча ел траву"],
        "right_answer": "Иногда трескай тик-так"
    },
    {
        "question": "Что сказал Осел, когда впервые увидел болото Шрека?",
        "options": ["Красиво тут у тебя", "Страшновато выглядит", "Тут никто жить не станет", "Какой осел поселился здесь"],
        "right_answer": "Какой осел поселился здесь"
    },
    {
        "question": "Что Шрек сделал из ушной серы за ужином?",
        "options": ["Зубочистку", "Свечу", "Закуску", "Горшочек меда"],
        "right_answer": "Свечу"
    },
    {
        "question": "Когда гномы принесли Белоснежку в хижину Шрека, что он сказал?",
        "options": ["Ты живая, иди отсюда", "Девушке здесь уютно", "Дохлой девке здесь не место", "Не мешайте мне отдыхать"],
        "right_answer": "Дохлой девке здесь не место"
    },
    {
        "question": "Кого Лорду Фаркуаду НЕ предлагали в невесты?",
        "options": ["Золушку", "Белоснежку", "Фиону", "Рапунцель"],
        "right_answer": "Рапунцель"
    },
    {
        "question": "Что сказал Шрек, впервые увидев замок Лорда Фаркуада?",
        "options": ["Хороший дворец, богатый хозяин", "Интересно, какие у него комплексы", "Я хочу сюда переехать", "Давненько я такого не видел"],
        "right_answer": "Интересно, какие у него комплексы"
    },
    {
        "question": "Что сказал Шрек, впервые увидев замок, где заточена Фиона?",
        "options": ["Ничего особенного", "Неплохой домик, но район так себе", "Прямо моя мечта", "Прекрасное место для отдыха"],
        "right_answer": "Неплохой домик, но район так себе"
    },
    {
        "question": "Как Шрек попал в башню к Фионе?",
        "options": ["Взобрался по лестнице", "Поднял себя верёвкой", "Подкинула дракониха на хвосте", "Открыли ворота рыцари"],
        "right_answer": "Подкинула дракониха на хвосте"
    },
    {
        "question": "С какими цветами лежала Фиона, когда притворялась спящей в башне?",
        "options": ["Тюльпаны", "Розы", "Ромашки", "Лилии"],
        "right_answer": "Ромашки"
    },
    {
        "question": "Что поцеловала дракониха, когда Осел выпал из её лап?",
        "options": ["Ногу Осла", "Жопу Осла", "Жопу Шрека", "Пятку Шрека"],
        "right_answer": "Жопу Шрека"
    },
    {
        "question": "Какие цветы попросила принести Фиона, когда Шреку попала стрела в зад?",
        "options": ["Красные цветы на зеленой ножке", "Белые цветы на красной ножке", "Синице цветы с зелеными листьями", "Ромашки"],
        "right_answer": "Белые цветы на красной ножке"
    },
    {
        "question": "Из кого Фиона сделала шарик?",
        "options": ["Крыса", "Змея", "Лягушка", "Улитка"],
        "right_answer": "Змея"
    },
    {
        "question": "Каким блюдом Шрек угощал Фиону?",
        "options": ["Шашлык из полевых мышей", "Сорная крыса на вертеле", "Печёная рыба", "Помойные жабы"],
        "right_answer": "Сорная крыса на вертеле"
    },
    {
        "question": "Что сказал Осел, когда Фиона раскрыла ему свой секрет?",
        "options": ["Ну вот теперь всё ясно", "Зачем дар речи при таких секретах", "Надо рассказать Шреку немедленно", "Всё равно мы друзья"],
        "right_answer": "Зачем дар речи при таких секретах"
    },
    {
        "question": "С каким овощем сравнивают Шрека весь фильм?",
        "options": ["Картошка", "Огурец", "Капуста", "Лук"],
        "right_answer": "Лук"
    },
    {
        "question": "Что сказал Лорд Фаркуад Шреку, когда освободил болото?",
        "options": ["Твоя территория свободна", "Дарственная на болото – беженцы изгнаны", "Теперь твоя жизнь налажена", "Забирай ключи и проваливай"],
        "right_answer": "Дарственная на болото – беженцы изгнаны"
    },
    {
        "question": "Из чего сделана свадебная карета Шрека и Фионы?",
        "options": ["Яблоко", "Тыква", "Кабачок", "Лук"],
        "right_answer": "Лук"
    }
]

# Индикаторы текущих вопросов
current_question_idx = {}

# Хранение результатов участников
player_results = {}

bot_instance = None  # Глобальная переменная для экземпляра бот

async def send_result_to_savedec(username, result):
    global bot_instance
    message = f"Пользователь @{username} завершил игру:\nРезультат: {result}"
    try:
        await bot_instance.send_message(chat_id=SAVEDEC_USER_ID, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю SaveDec: {e}")

def generate_keyboard(options):
    """Создание клавиатуры с вариантами ответов."""
    keyboard_buttons = []
    for i, option in enumerate(options):
        # Используем индекс опции как callback_data
        keyboard_buttons.append([InlineKeyboardButton(option, callback_data=f'answer_{i}')])
    return InlineKeyboardMarkup(keyboard_buttons)

def generate_next_button():
    """Создаем кнопку 'Следующий вопрос'"""
    button = [[InlineKeyboardButton("Следующий вопрос", callback_data="next")]]
    return InlineKeyboardMarkup(button)

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт игры."""
    global bot_instance
    bot_instance = context.bot  # Сохраняем экземпляр бота
    
    user_id = update.effective_user.id
    username = update.effective_user.username  # Получаем никнейм пользователя
    current_question_idx[user_id] = 0
    player_results[user_id] = {'score': 0, 'errors': [], 'state': 'waiting'}  # Добавлено состояние ожидания следующего вопроса
    question = questions[current_question_idx[user_id]]
    await update.message.reply_text(question['question'], reply_markup=generate_keyboard(question['options']))

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка ответа и обработка дальнейших действий."""
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username  # Получаем никнейм пользователя
    data = query.data.split('_')
    action_type = data[0]

    if action_type == 'answer':
        # Обработка выбранного ответа
        question_number = current_question_idx[user_id]
        selected_option_idx = int(data[1])  # Индекс выбранной опции
        selected_option = questions[question_number]['options'][selected_option_idx]
        correct_answer = questions[question_number]['right_answer']

        if selected_option != correct_answer:
            error = {"question": questions[question_number]["question"], "wrong_answer": selected_option, "correct_answer": correct_answer}
            player_results[user_id]['errors'].append(error)  # Запоминаем ошибку

        if selected_option == correct_answer:
            player_results[user_id]['score'] += 1

        # Показываем следующую кнопку
        await query.answer()
        await query.edit_message_reply_markup(generate_next_button())

    elif action_type == 'next':
        # Обработка кнопки "Следующий вопрос"
        player_results[user_id]['state'] = 'playing'
        current_question_idx[user_id] += 1
        if current_question_idx[user_id] >= len(questions):
            # Игра закончена
            score = player_results[user_id]['score']
            errors = player_results[user_id].get('errors', [])
            error_messages = ""
            if errors:
                error_messages = "\n\nОшибочные ответы:\n"
                for err in errors:
                    error_messages += f"- Правильный ответ на вопрос '{err['question']}': **{err['correct_answer']}**, ваш ответ: *{err['wrong_answer']}*\n"
                
            final_message = f"Викторина завершена.\nВаш результат: {score}/{len(questions)}{error_messages}"
            await query.message.reply_text(final_message)
            
            # Отправляем результат пользователю savedec
            await send_result_to_savedec(username, f"{score}/{len(questions)}")
            
            del current_question_idx[user_id], player_results[user_id]
        else:
            # Следующий вопрос
            question = questions[current_question_idx[user_id]]
            await query.message.reply_text(question['question'], reply_markup=generate_keyboard(question['options']))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Настройка обработчиков команд
    start_handler = CommandHandler('start', start_game)
    answer_handler = CallbackQueryHandler(check_answer)

    app.add_handler(start_handler)
    app.add_handler(answer_handler)

    print("Запускаю бота...")
    app.run_polling()