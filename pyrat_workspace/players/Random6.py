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
import random

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random6 (Player):

    """
        This player is an improvement of the Random2 player.
        Here, we add elements that help us explore better the maze.
        More precisely, we keep a list (in a global variable to be updated at each turn) of cells that have already been visited in the game.
        Then, at each turn, we choose in priority a random move among those that lead us to an unvisited cell.
        If no such move exists, we move randomly.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

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

        # We create an attribute to keep track of visited cells
        self.visited_cells = set()
        self.trajectory = []
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################


    @override
    def preprocessing(self: Self, maze: Maze, game_state: GameState) -> None:
        self.newmaze = self.simplify_maze(maze,game_state)
        self.trajectory.append(game_state.player_locations[self.name])

        return None
    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

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

        # Mark current cell as visited
        if game_state.player_locations[self.name] not in self.visited_cells:
            self.visited_cells.add(game_state.player_locations[self.name])
        self.trajectory.append(game_state.player_locations[self.name])
        # Return an action
        action = self.find_next_action(self.newmaze, game_state)
        return action

    #############################################################################################################################################
    #                                                               OTHER METHODS                                                               #
    #############################################################################################################################################

    def find_next_action ( self:       Self,
                           maze:       Maze,
                           game_state: GameState,
                         ) ->          Action:

        """
            This method returns an action to perform among the possible actions, defined in the Action enumeration.
            Here, the action is chosen randomly among those that don't hit a wall, and that lead to an unvisited cell if possible.
            If no such action exists, we choose randomly among all possible actions that don't hit a wall.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Go to an unvisited neighbor in priority
        neighbors = maze.get_neighbors(game_state.player_locations[self.name])
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.visited_cells]
        if len(unvisited_neighbors) > 0:
            (minei,dist) = (unvisited_neighbors[0],self.distance(self.newmaze,unvisited_neighbors[0],game_state.cheese[0]))
            for cheese in game_state.cheese:
                for neib in unvisited_neighbors:
                    if(self.distance(self.newmaze,neib,cheese)<dist):
                        (minei,dist) = (neib,self.distance(self.newmaze,neib,cheese))
                neighbor = minei
        # If there is no unvisited neighbor, choose one randomly
        else:
            self.trajectory.pop()
            neighbor = self.trajectory.pop()
        
        # Retrieve the corresponding action
        action = maze.locations_to_action(game_state.player_locations[self.name], neighbor)
        return action
    
    def simplify_maze(self:Self,maze: Maze,gamestate: GameState)-> Maze:
        """
        This function simplifies the maze by removing all dead ends
        """
        newmaze = maze
        had_changed = True
        while had_changed:
            had_changed = False
            for location in newmaze.vertices:
                if (len(newmaze.get_neighbors(location)) <= 1 and location not in gamestate.cheese and location!=gamestate.player_locations[self.name]):
                    newmaze.remove_vertex(location)
                    had_changed = True
        return newmaze
    

    def distance(self:Self,maze: Maze,start,end):
        """
        This function returns the distance between two points in the maze
        """
        diff = maze.coords_difference(start,end)

        return (diff[0]**2 + diff[1]**2)**0.5   
#####################################################################################################################################################
#####################################################################################################################################################
