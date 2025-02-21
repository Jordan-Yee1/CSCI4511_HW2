# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


#Reference the textbook Artificial Inelligence A Modern Approach, Russel and Norvig - for minimax implementation


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, but please don't change the method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]


    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood() 
        #The food is represented by a 2d array of T and F where there is a F border around the game stage and T for all food items, powerups not included
        #        currentFood = state.getFood()
        #       if currentFood[x][y] == True: ...
        #   OR prints as coordinates, if asList()
        newGhostStates = successorGameState.getGhostStates()    #Ghost states self.data.agentStates[1:] give xy coordinates and direction of ghost, from my understanding the direction of ghsot does not take a turn
        currentFood = currentGameState.getFood()         #use current food because new food would already be eaten

        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPositions = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
        
        ##WOW, just realized I was trying to get it to pass the standard pacman level, not the really simple test level with no walls. this is truly only something that I would do
        
        #Try manhatty first, if not then BFS

        # If somehing is dumb, but it works ... was it ever really a bad idea? (The answer is yes, but this should win with avg over 1000)

        #calculates the cloesest food via manhatty distance, gets stuck on walls where the food is on the other side, but the ghosts prevent timeout
        closest_food = min([manhattanDistance(newPos, food) for food in currentFood.asList()])

        #okay what about literally just try, if ghost next to you dont go there
        for ghost in newGhostPositions:
            if manhattanDistance(ghost, newPos) < 2:
                return -100
        #and uhhh if food is there, then go there
        for food in currentFood.asList():
            if food == newPos:
                return 50

        #get the negative, since the lowest cloesest food is actually the one we want, and the function returns the highest value move
        return 0 - closest_food

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #print("Num agents ", gameState.getNumAgents())
        value, action = self.max_value(gameState, 0) #(gamestate, current depth)
        print(value, action)
        return action
        #each iteration, max value gets pacman moves, then chains to min values of ghost moves
        #Then it will send the best action, get sucessor of that and send it to max value again 
    def max_value(self, gameState: GameState, curr_depth):
        
        best_value = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            value, ghost_action = self.min_value(gameState.generateSuccessor(0, action), 1, curr_depth) #Next game state after pacman, (The state after agent makes move, next agent)
         #   print(value)
            if value > best_value:
                best_value = value
                best_action = action
        return best_value, best_action
            
    def min_value(self, gameState: GameState, agent_idx, curr_depth):
        #Need to figure out how to add action  to this, do I have to ?
        #if gameState.isLose():
         #   return -1 #If this game state loses the game dont keep exploring
        #if gameState.isWin():
         #   return float('inf') #if game state wins, do this, dont need to keep exploring
            
        #yea im sure there is a cleaner way to write this, but im booted off two cups of coffee and do not really care
        #Should only trigger at the end of the ply, and since the ghosts go last per ply we add this here
        lowest_value = float('inf')
        lowest_action = None
        
        if agent_idx == gameState.getNumAgents()-1: #-1 because agent_idx is zero indexed but num agents presumeably is not
            curr_depth += 1 #End of ply reached
            if curr_depth == self.depth:
              #  print("curr_depth " , curr_depth, "  set depth ", self.depth)#Returning before last ghost makes move on ply 
                #If end ghost of final ply, calculate the evaluation after the ghost makes its move
                for action in gameState.getLegalActions(agent_idx):

                    value = self.evaluationFunction(gameState.generateSuccessor(agent_idx, action))   
                    if value < lowest_value:
                        lowest_value = value
                      #  print(lowest_value)

                        lowest_action = action
                     #   print(lowest_action)
            else: #else if end of ply but not depth, call max value to repeat process
                for action in gameState.getLegalActions(agent_idx):
                    value, pac_action = self.max_value(gameState.generateSuccessor(agent_idx, action), curr_depth)
                    if value < lowest_value:
                        lowest_value = value
                        lowest_action = action
        else: #Not the last ghost so call minimize again
            #Calling get legal action for current agent then applying that to the next one which is wrong
            for action in gameState.getLegalActions(agent_idx):
                #+1 to increment agent index to next ghost 
                value, ghost_action = self.min_value(gameState.generateSuccessor(agent_idx, action), agent_idx + 1, curr_depth) 
                if value < lowest_value:
                        lowest_value = value
                        lowest_action = action
      #  print(lowest_value, lowest_action)
        return lowest_value, lowest_action
        





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation (don't modify existing, but you can add to them)
better = betterEvaluationFunction
score = scoreEvaluationFunction
