# The-Great-Dalmuti

This game goes for many names, but the name "The Great Dalmuti" is the one my friend used for this, when she introduced the game to us one summer afternoon at Puolalanpuisto, Turku.
Source: https://en.wikipedia.org/wiki/The_Great_Dalmuti

The Great Dalmuti is a game which presents players the simplified mechanics of social classes;
It's hard to advance from slave to a king, it's equally easy to lose your status as a king.

This implementation uses simplified version of the rules. The Lesser Dalmuti and Lesser Slave are dropped, as well as taxation and revolution.

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

