import telebot
from telebot import types

f = open('token.ini', 'r', encoding='UTF-8')
TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
f.close()
bot = telebot.TeleBot(TOKEN)

# Создаем переменные для хранения состояния игры и поля
game = False
board = [' '] * 9

# Функция для отображения игрового поля
def display_board(board):
    line = '|'.join(board[0:3])
    print(line)
    print('-' * 5)
    line = '|'.join(board[3:6])
    print(line)
    print('-' * 5)
    line = '|'.join(board[6:9])
    print(line)

# Функция для проверки, является ли данное поле пустым
def is_empty(board, index):
    return board[index] == ' '

# Функция для проверки, является ли данное поле допустимым
def is_valid_move(board, index):
    return index >= 0 and index <= 8 and is_empty(board, index)

# Функция для проверки, есть ли победитель в данной игре
def check_winner(board):
    winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for winner in winners:
        if board[winner[0]] == board[winner[1]] == board[winner[2]] and board[winner[0]] != ' ':
            return board[winner[0]]
    return False

# Функция для совершения хода в игре
def make_move(board, index, symbol):
    board[index] = symbol

# Функция для обработки сообщения пользователя
@bot.message_handler(commands=['start'])
def start(message):
    global game
    global board
    game = True
    board = [' '] * 9
    reply_markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text='1', callback_data='1'),
        types.InlineKeyboardButton(text='2', callback_data='2'),
        types.InlineKeyboardButton(text='3', callback_data='3'),
        types.InlineKeyboardButton(text='4', callback_data='4'),
        types.InlineKeyboardButton(text='5', callback_data='5'),
        types.InlineKeyboardButton(text='6', callback_data='6'),
        types.InlineKeyboardButton(text='7', callback_data='7'),
        types.InlineKeyboardButton(text='8', callback_data='8'),
        types.InlineKeyboardButton(text='9', callback_data='9'),
    ]

    reply_markup.row(buttons[0],buttons[1],buttons[2])
    reply_markup.row(buttons[3], buttons[4], buttons[5])
    reply_markup.row(buttons[6], buttons[7], buttons[8])
    bot.send_message(message.chat.id, 'Добро пожаловать в игру крестики-нолики!', reply_markup=reply_markup)

# Функция для обработки нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global game
    global board
    if game:
        index = int(call.data) - 1
        if is_valid_move(board, index):
            make_move(board, index, 'X')
            winner = check_winner(board)
            if winner:
                reply_markup = types.ReplyKeyboardRemove()
                bot.send_message(call.message.chat.id, f'Выиграли {winner}!', reply_markup=reply_markup)
                game = False
            else:
                index = get_computer_move(board)
                make_move(board, index, 'O')
                winner = check_winner(board)
                if winner:
                    reply_markup = types.ReplyKeyboardRemove()
                    bot.send_message(call.message.chat.id, f'Выиграли {winner}!', reply_markup=reply_markup)
                    game = False
                else:
                    reply_markup = types.InlineKeyboardMarkup()
                    buttons = []
                    for i in range(0, 9):
                        if is_empty(board, i):
                            buttons.append(types.InlineKeyboardButton(text=' ', callback_data=str(i + 1)))
                        else:
                            buttons.append(types.InlineKeyboardButton(text=board[i], callback_data=str(i + 1)))
                    reply_markup.row(buttons[0], buttons[1], buttons[2])
                    reply_markup.row(buttons[3], buttons[4], buttons[5])
                    reply_markup.row(buttons[6], buttons[7], buttons[8])
                    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
        else:
            bot.answer_callback_query(call.id, 'Неверный ход. Попробуйте еще раз!')
    else:
        bot.answer_callback_query(call.id, 'Игра окончена. Нажмите /start, чтобы начать новую игру.')

# Функция для получения хода компьютера
def get_computer_move(board):
    for i in range(0, 9):
        if is_empty(board, i):
            board_copy = board[:]
            make_move(board_copy, i, 'O')
            if check_winner(board_copy):
                return i
    for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if is_empty(board, i):
            return i

# Запускаем бота
bot.polling()
