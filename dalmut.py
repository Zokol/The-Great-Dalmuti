import random

"""
THE GREAT DALMUTI
Heikki "Zokol" Juva 2015 - heikki@juva.lu


This game goes for many names, but the name "The Great Dalmuti" is the one my friend used for this, when she introduced the game to us one summer afternoon at Puolalanpuisto, Turku.

The Great Dalmuti is a game which presents players the simplified mechanics of social classes;
It's hard to advance from slave to a king, it's equally easy to lose your status as a king.

Prequcitions:
Pack of cards: numbers 1-12, the value of the card determines also how many of that card there is in the pack. (One with value 1, two with value 2, etc.. finally twelve with value 12).
Players 3-10, basically you could play this game with more players, but at some point the players-cards-ratio is too high to keep the game meaningfull.

Game start and player order determination:
Pack is shuffled and players are dealt one card each. The player who has the lowest value card is now the "Dalmuti", player with the lowest value card is now the "slave". Every other player are "traders" and will arrange according to their card values, the player having the lowest value is positioned next to the Dalmuti and the player with the next lowest value card is positioned next to him/her.
Cards are finally returned to the pack and it's shuffled again.

Gameplay:
The whole pack is dealt to players equally, or as equally it is possible to deal the pack with given number of players.

Round:
Dalmuti starts the first round. He/she selects cards from hand which are the same value, for example five 7s, usually it is preferred to select the high value cards at the start of the game.
The next player has to put down the same number of lower number cards than are on the top of the stack. For example, if the previous player put down five 7s, you have to put five 6s or five 5s.
If player has no cards to put down (no suitable cards in hand), player has to skip. Player can also skip if he/she doesn't want to put down anything, even if it would be possible.
Round continues as long as players have something to put on the table. The player who puts the last cards on the table (everyone after that player skips), this player can then start the next round, placing any number of any card he/she has in hand.

Game:
Rounds are played as long as at least two players have cards in their hand. 
When some player is the first to empty his/hers hand, this player is now the Dalmuti in the next game and starts the next round.
The next player who gets rid of all cards is trader in the next game, and plays after the dalmuti.
Playing order for the rest of the players in the next game is determined by the order which they get their hands empty.
The last player having hards in his/hers hand is the "slave" for the next round, and plays last.

The game has no definite ending, you just have to agree on end the game after certain time or number of rounds.

Point system:
This implementation of The Great Dalmuti evaluates the players on the basis of how many times they get the status of "Dalmuti", "Trader" or "Slave".

Player AI:
The simplified AI engine introduced here (in Player.play_best_card()) selects always just the most common and highest value cards in hand.
The reasoning behind selecting this logic is that it's usually adviceable to play your high-cards first. In some situations, it may also be advantage to have multiple high-cards, which other players can't possibly match because of the number of cards requested (for example, you have four 5s, other players only have three cards each. This means that other players have no possibility to match your hand in this round, meaning also that you can start the next one.)

"""

## Exception raised when all players have skipped the round
class SkipException(Exception):
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
		self.stats = {"Dalmut": 0, "Trader": 0, "Slave": 0}

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

class Game:
	def __init__(self, number_of_players, number_of_games):
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
		playing_order = self.players
		for i in range(number_of_games):
			self.reset_stack()
			playing_order = self.play_game(playing_order)
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

	def play_game(self, playing_order):


		print("-----------------------")
		print("")

		print("Cards dealt")
		self.deal_cards()
		self.print_players()

		print("-----------------------")
		print("")

		round_i = 0
		while round_i < 10:
			round_i += 1
			print("Play round", round_i)
			print(playing_order)
			playing_order = self.play_round(playing_order)
			print(playing_order)
			playing_order[0].stats["Dalmut"] += 1
			for player in playing_order[1: -1]:
				player.stats["Trader"] += 1
			playing_order[-1].stats["Slave"] += 1
			#if not new_order[0].hand: return new_order #XXX ????
			self.table = []
			self.print_players()

	def print_players(self):
		for p in self.players:
			print(p)

	def print_stats(self):
		for p in self.players:
			print (p.name, p.stats)

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
			player.stats["Trader"] += 1
		self.players[0].position = "Dalmut"
		self.players[-1].position = "Slave"
		self.players[0].stats["Dalmut"] += 1
		self.players[-1].stats["Slave"] += 1

	def deal_cards(self):
		card_id = 0
		while card_id < len(self.stack):
			for player in self.players:
				player.receive_card(self.stack.lift_top_card())
				card_id += 1

	def empty_players_hands(self):
		for player in self.players:
				player.empty_hand()

	def play_round(self, players):
		#starting_index = self.players.index(starting_player)
		#transposed_players = self.players[starting_index:] + self.players[:starting_index]	
		new_order = []
		skip_counter = 0
		while True:
			for player in players:
				if skip_counter == len(players) - 1:
					return player
				try:
					print(player)
					self.table.append(player.play_hand(self.table))
					if not player.hand and not new_dalmut: new_order.append(players.pop(players.index(player)))
					elif not player.hand and new_dalmut and len(players) > 1: new_order.append(players.pop(players.index(player)))
					elif not player.hand and len(players) == 1: 
							new_order.append(players.pop(players.index(player)))
							print(new_order)
							return new_order
					self.print_table()
					skip_counter = 0
				except SkipException:
					print("Skip")
					skip_counter += 1

if __name__ == '__main__':
	game = Game(5, 3)