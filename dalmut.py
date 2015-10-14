import random

"""
THE GREAT DALMUTI
Heikki "Zokol" Juva 2015 - heikki@juva.lu

"""

## Exception raised when all players have skipped the round
class SkipException(Exception):
	pass

class RestartRound(Exception):
	pass

class Card:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return "Card: " + str(self.value)
	
	def __str__(self):
		return str(self.value)

class Player:
	def __init__(self, name):
		self.name = name
		self.hand = []
		self.position = "TBD"
		self.stats = {"Dalmut": [], "Trader": [], "Slave": []}

	def __str__(self):
		card_list = []
		for card in self.hand:
			card_list.append(card.__str__())
		return str(self.name) + " " + self.position + " : " + ", ".join(card_list)

	def sort_hand(self):
		self.hand.sort(key=lambda card: card.value, reverse=True)

	def receive_card(self, card):
		self.hand.append(card)
		self.sort_hand()

	def take_card(self, id):
		return self.hand.pop(id)

	def take_highest_card(self):
		self.sort_hand()
		return self.take_card(0)

	def take_lowest_card(self):
		self.sort_hand()
		return self.take_card(len(self.hand)-1)

	def count_cards(self, order):
		return len([card for card in self.hand if card.value == order])

	# Return those cards that player has many and those that are as low number as possible
	def take_best_cards(self, limit, count):
		self.sort_hand()

		best = [-1, -1] # First is the card order, second is the 'point-value'
		if limit > self.hand[0].value:
			highest_card = self.hand[0].value + 1
		else:
			highest_card = limit
		#print(higest_card)
		#print(self.count_cards(higest_card))
		for i in reversed(range(highest_card)):
			if count == -1:
				points = self.count_cards(i) * i
				if best[1] < points:
						best[0] = i
						best[1] = points
			elif self.count_cards(i) == count:
				best[0] = i
				break

		if best[0] == -1: raise SkipException # No cards -> skip

		picked_cards = [card for card in self.hand if card.value == best[0]]
		if count != -1: picked_cards = picked_cards[:count]

		self.hand = [card for card in self.hand if card not in picked_cards]

		self.sort_hand()
		return picked_cards

	def play_hand(self, table):
		if len(table) > 0:
			count = len(table[-1])
			limit = table[-1][0].value
		else:
			count = -1
			limit = 99
		return self.take_best_cards(limit, count)

	def empty_hand(self):
		self.hand = []

class Stack:
	def __init__(self, largest_number):
		self.stack = []
		for value in range(1, largest_number + 1):
			for i in range(value): 
				self.stack.append(Card(value))
	
	def __str__(self):
		card_list = []
		for card in self.stack:
			card_list.append(card.__str__())
		return ", ".join(card_list)

	def __len__(self):
		return len(self.stack)

	def shuffle(self):
		random.shuffle(self.stack)

	def lift_top_card(self):
		return self.stack.pop(0)

	def add(self, card):
		self.stack.append(card)

class Game:
	def __init__(self, number_of_players, number_of_games, number_of_rounds):
		self.table = []
		self.players = []
		for p in range(number_of_players):
			self.players.append(Player("Player " + str(p)))

		self.reset_stack()

		# Determine initial position for players
		# Each player lifts one card from stack
		# Lowest card holder is the Great Dalmut
		# Highest card holder is the slave
		# Everyone in between are traders
		self.initial_pos()
		print("Intial position for players determined")
		self.print_players()

		# Main loop
		#starting_player = self.players[0]
		for i in range(number_of_games):
			self.reset_stack()
			self.play_game(self.players, number_of_rounds)
			#self.order_players(starting_player)

		print("Game over")
		print("RESULTS:")
		self.print_stats()

	def reset_stack(self):
		self.empty_players_hands()

		# Create stack
		self.stack = Stack(12) # Create stack with the highest number being 12
		print("Number of cards:", len(self.stack))
		print("Stack")
		print(self.stack)
		print("-----------------------")
		print("")

		# Shuffle stack
		print("Stack shuffled")
		self.stack.shuffle()
		print(self.stack)
		print("-----------------------")
		print("")

	def play_game(self, playing_order, number_of_rounds):

		print("-----------------------")
		print("")

		print("Cards dealt")
		self.deal_cards()
		self.print_players()

		print("-----------------------")
		print("")

		round_i = 0
		while round_i < number_of_rounds:
			round_i += 1
			print("Play round", round_i)
			#print(playing_order)
			playing_order = self.play_round(playing_order)
			#print(playing_order)
			playing_order[0].stats["Dalmut"].append(round_i)
			for player in playing_order[1: -1]:
				player.stats["Trader"].append(round_i)
			playing_order[-1].stats["Slave"].append(round_i)
			print("Players card count:", self.count_player_cards(playing_order))
			self.empty_table()
			self.deal_cards()
			print("Players card count:", self.count_player_cards(playing_order))
			#if not new_order[0].hand: return new_order #XXX ????
			self.table = []
			self.print_players()
			self.print_stats()

	def print_players(self):
		for p in self.players:
			print(p)

	def print_stats(self):
		for p in self.players:
			print (p.name, "Dalmut:", len(p.stats["Dalmut"]), "Trader:", len(p.stats["Trader"]), "Slave:", len(p.stats["Slave"]))

	def print_table(self):
		top_cards = self.table[-1]
		print(str(len(top_cards)), "x", top_cards[0], "on the table")

	def initial_pos(self):
		for player in self.players:
			if len(self.stack) > 0: player.receive_card(self.stack.lift_top_card())
			else: print("Too small stack to deal, not enough cards for everyone")

		self.players.sort(key = lambda player: player.hand[0].value)
		for player in self.players:
			player.position = "Trader"
			player.stats["Trader"].append(0)
		self.players[0].position = "Dalmut"
		self.players[-1].position = "Slave"
		self.players[0].stats["Dalmut"].append(0)
		self.players[-1].stats["Slave"].append(0)

	def deal_cards(self):
		print("Number of cards in stack:", len(self.stack))
		card_id = 0
		while card_id < len(self.stack):
			for player in self.players:
				player.receive_card(self.stack.lift_top_card())
				card_id += 1

	def count_player_cards(self, players):
		total = 0
		for player in players:
			total += len(player.hand)
		return total

	def empty_players_hands(self):
		for player in self.players:
				player.empty_hand()

	def empty_table(self):
		card_count = 0
		for cards in self.table:
			for card in cards:
				card_count += len(cards)
				self.stack.add(cards.pop(cards.index(card)))
		print("Number of cards on table", card_count)
		self.table = []

	def play_round(self, players):
		#starting_index = self.players.index(starting_player)
		#transposed_players = self.players[starting_index:] + self.players[:starting_index]	
		new_order = []
		skip_counter = 0
		new_dalmut = False
		while True:
			try:
				for player in players:
					if skip_counter == len(players) - 1:
						#return player
						## Every other player skipped, transpose player-list to let current player to start the next round
						starting_index = self.players.index(player)
						transposed_players = self.players[starting_index:] + self.players[:starting_index]	
						players = transposed_players
						skip_counter = 0
						self.empty_table()
						raise RestartRound
					try:
						#print(player)
						
						## If someone runs out of cards, here we determine who gets which position for the next game
						"""
						print("Hand empty:", not player.hand)
						print("Player finished:", player in new_order)
						print("Is new dalmut found:", new_dalmut)
						"""
						if player in new_order:
							pass
						elif not player.hand and not new_dalmut: 
							#print("New Dalmut found!!")
							new_order.append(player) # First player runs out of cards
							new_dalmut = True
						elif not player.hand and new_dalmut and len(players) - 1 > len(new_order):
							new_order.append(player) # Player runs out of cards, who is not the first and not the last
						elif not player.hand and len(players) - 1 == len(new_order):  # Last player runs out of cards
							new_order.append(player)
							#print("NEW ORDER:", new_order)
							return new_order
						else:
							self.table.append(player.play_hand(self.table)) ## Let the next playr to play the hand and place it on the table
							self.print_table()

						#skip_counter = 0
					except SkipException:
						print("Skip")
						skip_counter += 1
			except RestartRound:
				print("Restarting round with new order")
				pass

if __name__ == '__main__':
	game = Game(10, 3, 900)