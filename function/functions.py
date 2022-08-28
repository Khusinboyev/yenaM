from sqlite3 import connect
from key import *
from databas import *
from aiogram import *
from aiogram.types import *
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml

class functions:
	@staticmethod
	async def check_on_start(user_id):
		rows = sql.execute("SELECT id FROM channels").fetchall()
		error_code = 0
		for row in rows:
			r = await dp.bot.get_chat_member(chat_id=row[0], user_id=user_id)
			if r.status in ['member', 'creator', 'admin']:
				pass
			else:
				error_code = 1
		if error_code == 0:
			return True
		else:
			return False

class panel_func:
	@staticmethod
	async def channel_add(id):
		sql.execute("""CREATE TABLE IF NOT EXISTS channels(id)""")
		db.commit()
		sql.execute("INSERT INTO channels VALUES(?);", id)
		db.commit()


	@staticmethod
	async def channel_delete(id):
		sql.execute(f'DELETE FROM channels WHERE id = "{id}"')
		db.commit()

	@staticmethod
	async def channel_list():
		sql.execute("SELECT id from channels")
		str = ''
		for row in sql.fetchall():
			id = row[0]
			try:
				all_details = await dp.bot.get_chat(chat_id=id)
				title = all_details["title"]
				channel_id = all_details["id"]
				info = all_details["description"]
				str+= f"------------------------------------------------\nKanal useri: > {id}\nKamal nomi: > {title}\nKanal id si: > {channel_id}\nKanal haqida: > {info}\n"
			except:
				str+= "Kanalni admin qiling"
		return str


async def forward_send_msg(chat_id: int, from_chat_id: int, message_id: int) -> bool:
	try:
		await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
	except exceptions.BotBlocked:
		pass
	except exceptions.ChatNotFound:
		pass
	except exceptions.UserDeactivated:
		pass
	except exceptions.TelegramAPIError:
		pass
	else:
		return True
	return False


async def send_message_chats(chat_id: int, from_chat_id: int, message_id: int) -> bool:
	try:
		await dp.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
	except exceptions.BotBlocked:
		pass
	except exceptions.ChatNotFound:
		pass
	except exceptions.UserDeactivated:
		pass
	except exceptions.TelegramAPIError:
		pass
	else:
		return True
	return False

async def get_site_content(URL):
	async with aiohttp.ClientSession() as session:
		async with session.get(URL) as resp:
			text = await resp.read()

	return BeautifulSoup(text.decode('utf-8'), 'lxml')


async def one_data_get(id):
	try:
		URL = f"https://mandat.dtm.uz/Home2022/AfterFilter?name={id}&region=0"
		soup = await get_site_content(URL)
	except:

		URL = f"http://mandat.dtm.uz/Home2022/AfterFilter?name={id}&region=0"
		soup = await get_site_content(URL)


	id = soup.find("td").text
	name = soup.find_all("td", limit=2)[-1].text
	ball = soup.find_all("td", limit=5)[-1].text
	text = f"<b>🎓 Imtihon natijangiz👇:\n\n🆎F.I.SH:</b> {name}\n<b>🆔ID raqami:</b> {id}\n<b>📊To'plangan ball</b>: {ball}\n\n@mandatjavobbot"
	return [text, name]

async def two_data_get(id):
	try:
		URL = f"http://mandat.dtm.uz/Home2022/AfterFilter?name={id}&region=0"
	except:
		URL = f"http://mandat.dtm.uz/Home2022/AfterFilter?name={id}&region=0"


	text = URL
	return text



#################################      natija 2 uchun

async def get_data(id):
	try:
		URL = f"https://mandat.dtm.uz/Transfer2022/AfterFilter?name={id}&region=0"
		soup = await get_site_content(URL)
	except:

		URL = f"http://mandat.dtm.uz/Transfer2022/AfterFilter?name={id}&region=0"
		soup = await get_site_content(URL)


	id = soup.find("td").text
	name = soup.find_all("td", limit=2)[-1].text
	ball = soup.find_all("td", limit=5)[-1].text
	text = f"<b>🎓 Imtihon natijangiz👇:\n\n🆎F.I.SH:</b> {name}\n<b>🆔ID raqami:</b> {id}\n<b>📊To'plangan ball</b>: {ball}"

	url = soup.find("a", class_='btn btn-info')['href']
	try:
		URL = f"https://mandat.dtm.uz{url}"
		soup3 = await get_site_content(URL)
	except:
		URL = f"http://mandat.dtm.uz{url}"
		soup3 = await get_site_content(URL)
	dat3 = f"<b>✅ Yo'nalish boʻyicha o'tish ball: </b>{soup3.find_all('td')[3].text}"

	return [text, dat3]


