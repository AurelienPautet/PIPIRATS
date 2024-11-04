#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""


#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################


class BFS (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__(self:     Self,
                 *args:    Any,
                 **kwargs: Any
                 ) -> Self:
        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        self.actions = []
        # Print phase of the game
        print("Constructor")

    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing(self:       Self,
                      maze:       Maze,
                      game_state: GameState,
                      ) -> None:
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        print("dfsdf")
        trans = self.traversal(maze, game_state.player_locations[self.name])
        print(trans)
        print(game_state.cheese[0])
        print("route", self.find_route(
            trans[1], game_state.player_locations[self.name], game_state.cheese[0]))
        self.actions = maze.locations_to_actions(self.find_route(
            trans[1], game_state.player_locations[self.name], game_state.cheese[0]))

    @override
    def turn(self:       Self,
             maze:       Maze,
             game_state: GameState,
             ) -> Action:
        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Print phase of the game
        print("Turn", game_state.turn)

        # Return an action
        return self.actions.pop(0)

    def traversal(self:   Self,
                  graph:  Graph,
                  source: Integral
                  ) -> Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:
        """
            This method performs a DFS traversal of a graph.
            It returns the explored vertices with associated distances.
            It also returns the routing table, that is, the parent of each vertex in the traversal.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """

        # Initialize distances and routing table
        distances = {source: 0}
        routing_table = {source: None}

        queue = [source]

        while len(queue) > 0:
            current = queue.pop(0)
            voisins = graph.get_neighbors(current)
            for vois in voisins:
                if vois not in distances:
                    distances[vois] = distances[current] + 1
                    queue.append(vois)
                    routing_table[vois] = current

        return (distances, routing_table)

    def find_route(self:          Self,
                   routing_table: Dict[Integral, Optional[Integral]],
                   source:        Integral,
                   target:        Integral
                   ) -> List[Integral]:
        """
            This method finds the route from the source to the target using the routing table.
            In:
                * self:          Reference to the current object.
                * routing_table: The routing table.
                * source:        The source vertex.
                * target:        The target vertex.
            Out:
                * route: The route from the source to the target.
        """
        route = [target]
        while (route[-1] != source):
            print(route[-1])
            nexts = routing_table[route[-1]]
            if nexts is None or type(nexts) is not int:
                break
            route.append(nexts)
        List.reverse(route)
        return route
        #############################################################################################################################################

    @ override
    def postprocessing(self:       Self,
                       maze:       Maze,
                       game_state: GameState,
                       stats:      Dict[str, Any],
                       ) -> None:
        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")

#####################################################################################################################################################
#####################################################################################################################################################
