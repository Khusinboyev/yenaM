import pytz
import datetime
from function.functions import *
from databas import *
from key import *
from buttons.mButtons import *
from Statess.statess import From
from aiogram.dispatcher import FSMContext

sent_number = types.ReplyKeyboardMarkup(resize_keyboard=True)
sent_number.add(types.KeyboardButton(text="Raqamni yuborish📱", request_contact=True))

@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    user_id = message.chat.id
    sql.execute("""CREATE TABLE IF NOT EXISTS users ("user_id"  INTEGER,"date"  INTEGER, "lang" INTEGER, "tel_Num" INTEGER);""")
    db.commit()
    check = sql.execute(f"""SELECT user_id FROM users WHERE user_id = {user_id}""").fetchone()

    if check == None:
        sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y %H:%M')
        sql.execute(f"""INSERT INTO users (user_id, date, lang) VALUES ('{user_id}', '{sana}', '{message.from_user.language_code}')""")
        db.commit()

    check_Num = sql.execute(f"""SELECT tel_Num FROM users WHERE user_id = {user_id}""").fetchone()
    if check_Num[0] == None:
        await message.answer(f"""Assalomu alaykum! \n\nBotdan toʻliq foydalanish uchun raqamingizni yuboring!""", reply_markup=sent_number)
        await From.sent_num.set()
    else:
        await message.reply("Tanlang👇", reply_markup=frond_btn)

@dp.callback_query_handler( text="check")
async def check(call: CallbackQuery):
    user_id = call.from_user.id
    if await functions.check_on_start(user_id):
        await call.answer()
        await call.message.answer("Xush kelibsiz!", reply_markup=frond_btn)
    else:
        await call.answer(show_alert=True, text="Botimizdan foydalanish uchun kanalimizga azo bo'ling")



@dp.message_handler(state=From.sent_num, content_types=types.ContentType.CONTACT)
async def f(message: types.Message, state: FSMContext):
    sql.execute(f"""UPDATE users SET tel_Num =  '{message.contact.phone_number}' WHERE user_id = '{message.from_user.id}'""")
    db.commit()
    await message.reply("Tanlang👇", reply_markup=frond_btn)
    await state.finish()

@dp.message_handler(state=From.sent_num, content_types='any')
async def f(message: types.Message, state: FSMContext):
    await message.reply("☎️Quyidagi tugma orqali nomeringizni yuboring👇", reply_markup=sent_number)


