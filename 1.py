from os import environ as env
from discord import Intents
from discord.ext import commands
import asyncio

from dotenv import load_dotenv
from relaybot import RelayBot

load_dotenv()

def main():
	relay_bot = RelayBot(
		env.get('RELAY_SOURCE_CHANNEL_ID'), 
		(env.get('RELAY_PRIORITY_DESTINATION_CHANNEL_ID'),
		env.get('RELAY_FALLBACK_DESTINATION_CHANNEL_ID')),
		env.get('RELAY_ROLE_ID'),
        env.get('RELAY_BOT_TOKEN')
	)
	loop = asyncio.get_event_loop()
	asyncio.set_event_loop(loop)
	loop.create_task(relay_bot.run())
	loop.run_forever()

def one():
	while True:
		print(1)
# print(env.get('RELAY_ROLE_ID'))
if __name__ == '__main__':
	main()