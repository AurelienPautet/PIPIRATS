# External imports
from Dijkstra import Dijkstra
from pyrat import Game
import sys
import os
import pprint

#  Add needed directories to the path
sys.path.append(os.path.join("..", "players"))

# PyRat imports
#  Customize the game elements
CONFIG = {"mud_percentage": 90,
          "nb_cheese": 1,
          "random_seed": 42,
          "trace_length": 1000}
# Instantiate a game with specified arguments
game = Game(**CONFIG)

# Instantiate a player and add it to the game
player = Dijkstra()
game.add_player(player)

# Start the game and
stats = game.start()
# Show statistics
pprint.pprint(stats)
