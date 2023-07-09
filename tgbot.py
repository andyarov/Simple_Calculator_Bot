import telebot

bot = telebot.TeleBot("telegram.token")

value = ""
# create keyboard
keyboard = telebot.types.InlineKeyboardMarkup()
# create 1st row with buttons
button_C = telebot.types.InlineKeyboardButton("C", callback_data="C")
button_AC = telebot.types.InlineKeyboardButton("AC", callback_data="AC")
button_open = telebot.types.InlineKeyboardButton("(", callback_data="(")
button_close = telebot.types.InlineKeyboardButton(")", callback_data=")")
keyboard.row(button_open, button_C, button_AC, button_close)
# create 2nd row with buttons
button_7 = telebot.types.InlineKeyboardButton('7', callback_data="7")
button_8 = telebot.types.InlineKeyboardButton('8', callback_data="8")
button_9 = telebot.types.InlineKeyboardButton('9', callback_data="9")
button_mult = telebot.types.InlineKeyboardButton('*', callback_data="*")
keyboard.row(button_7, button_8, button_9, button_mult)
# create 3rd row with buttons
button_4 = telebot.types.InlineKeyboardButton('4', callback_data="4")
button_5 = telebot.types.InlineKeyboardButton('5', callback_data="5")
button_6 = telebot.types.InlineKeyboardButton('6', callback_data="6")
button_div = telebot.types.InlineKeyboardButton('/', callback_data="/")
keyboard.row(button_4, button_5, button_6, button_div)
# create 4th row with buttons
button_1 = telebot.types.InlineKeyboardButton('1', callback_data="1")
button_2 = telebot.types.InlineKeyboardButton('2', callback_data="2")
button_3 = telebot.types.InlineKeyboardButton('3', callback_data="3")
button_plus = telebot.types.InlineKeyboardButton('+', callback_data="+")
keyboard.row(button_1, button_2, button_3, button_plus)
# create 5th row with buttons
button_0 = telebot.types.InlineKeyboardButton('0', callback_data="0")
button_dot = telebot.types.InlineKeyboardButton(',', callback_data=".")
button_minus = telebot.telebot.types.InlineKeyboardButton('-', callback_data="-")
button_result = telebot.types.InlineKeyboardButton('=', callback_data="=")
keyboard.row(button_0, button_dot, button_minus, button_result)

@bot.message_handler(commands = ["start"] )
def start(message):
    # send message with a value and display buttons
    global value
    if value == "":
        bot.send_message(message.chat.id, "0", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: True)
def callback_func(callback):
    # takes the value passed by the user
    # try to calculate value and edit the message with a new value
    global value
    data = callback.data
    # try to calculate a value
    if data == "C":
        value = value[:-1]
    elif data == "AC":
        value = ""
    elif data == "=":
        try:
            result = eval(value)
            # formatting the result
            if result % 1 == 0:
                result = int(result)
            else:
                result = round(result, 2)
            value = str(result)
        except ZeroDivisionError:
            value = "Деление на ноль!"
        except SyntaxError:
            value = "0"
        except:
            value = "Ошибка!"
    else:
        value += data

    # edit the message with a new value
    if value == "":
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="0",
                              reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=value,
                              reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)