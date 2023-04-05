
import discord, re

class RelayBot(discord.Client):	
	def __init__(self, source_channel, destination_channels, role_id,token):
		discord.Client.__init__(
			self,
			command_prefix='.', 
			self_bot=True, 
			status=discord.Status.offline,
			intents=discord.Intents.default()
		)
		# client = discord.Client(intents=discord.Intents.default())
		self.__source_channel = source_channel
		self.__destination_channels = destination_channels
		self.__role_id = role_id
		self._token = token
		# print(token)
		print('Bot Instantiated Successfully')
	# Message tunnels, the source is the key, the destination is the value
	message_tunnels = {
		'736371400213921903': '1091050140112003112'
	}
	def run(self):
		super().run(self._token)

	# The Maximum Price you are willing to pay for an item per unit
	# If the price is higher than this, the bot will not @ you, and if set up, will send the message to the failover channel

	# Format: 'item name': maximum price per unit
	# it is important to note that the item name must be in lowercase, and must be the same as the item name in the auction house
	
	maximum_unit_prices = {
		'tnt': (10000 / 64) + 2,
		'ender pearl': (20000 / 16) + 2,
		'obsidian': (30000 / 64) +2,
		'monster egg': (44800000 / 64) +2,
        '❉ Lame Maléfique ❉': 15000000,
        '⚔ Lame de l\'Infini ⚔': 15000000,
        'Bow': 100000,
        'Spawner - Skeleton': (12800000 / 64) +2,
        'Spawner - Spider': (6400000 / 64) +2,
        'Spawner - Magma Cube': 100000000,
        'Spawner - Creeper': 100000000,
    }

	__expr = {
		'qty': re.compile('\(x\d+\)'),
		'seller': re.compile('``[\w_]{3,48}``'),
		'item': re.compile('nte ``.{1,32}`` \('),
		'price': re.compile('\*\*[\d\s]+✸\*\*$')
	}

	


	async def on_ready(self):
		print ('Bot Started Successfully')


	async def on_message(self, message):
		if str(message.channel.id) in self.message_tunnels.keys():
			channel = self.get_channel(int(self.message_tunnels[message.channel.id]))
			await channel.send(message.content)

		if message.channel.id != int(self.__source_channel): return
		
		item_string = len(message.embeds) > 0 and message.embeds[0].to_dict()['fields'][0]['value'] or None
		
		if not item_string: return
		
		item = {
			'seller': self.__expr['seller'].search(item_string).group()[2:-2],
			'name': self.__expr['item'].search(item_string).group()[6:-4].lower(),
			'qty': int(self.__expr['qty'].search(item_string).group()[2:-1]),
			'price': int(self.__expr['price'].search(item_string).group()[2:-3].replace(' ', ''))
		}

		unit_price = item['price'] / item['qty']

		
		affordable = (item['name'] in self.maximum_unit_prices.keys()) and (self.maximum_unit_prices[item['name']] > unit_price)
			
		channel = self.get_channel(self.__destination_channels[int(not affordable)])

		embed_dict = message.embeds[0].to_dict()


		await channel.send(f"""{affordable and '<@&' + self.__role_id+ '>, ' or ''} **un nouvelle item a été publié a l'hdv !** ```yaml
[Item à vendre]# {item['name']}

[Vendeur]# {item['seller']}

[Quantité]# {item['qty']}

[Prix]# {item['price']}✸
[Prix à l'unité]# {unit_price}✸


{len(embed_dict['fields']) > 1 and '[Enchantments]# '+ embed_dict['fields'][1]['value'][4:-2]  or ''}
```""")
		
	def get_channel(self, id):
		return discord.utils.get(self.get_all_channels(), id=int(id))