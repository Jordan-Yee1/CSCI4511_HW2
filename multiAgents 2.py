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


#Reference the textbook Artificial Inelligence A Modern Approach, Russel and Norvig - for minimax & expectimax implementation


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
       
        
        value, action = self.max_value(gameState, 0, 0) #(gamestate, current depth, agent)
        return action
        #each iteration, max value gets pacman moves, then chains to min values of ghost moves
        #Then it will send the best action, get sucessor of that and send it to max value again 
    
    
    def max_value(self, gameState : GameState, agent_idx, curr_depth):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None#If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring

        best_value = float('-inf')
        best_action = None
        
        if curr_depth == self.depth:
            return  self.evaluationFunction(gameState), None
        else:
            for action in gameState.getLegalActions(agent_idx):
                value, ghost_action = self.min_value(gameState.generateSuccessor(agent_idx, action), agent_idx + 1, curr_depth) #Next game state after pacman, (The state after agent makes move, next agent)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action
        
    def min_value(self, gameState : GameState, agent_idx, curr_depth):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None #If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring
        
        lowest_value = float('inf')
        lowest_action = None

        if agent_idx == gameState.getNumAgents()-1: #-1 because agent_idx is zero indexed but num agents presumeably is not
            for action in gameState.getLegalActions(agent_idx):
                value, pac_action = self.max_value(gameState.generateSuccessor(agent_idx, action), 0, curr_depth + 1)
                if value < lowest_value:
                    lowest_value = value
                    lowest_action = action
        else:
            for action in gameState.getLegalActions(agent_idx):
                value, ghost_action = self.min_value(gameState.generateSuccessor(agent_idx, action), agent_idx + 1, curr_depth)
                if value < lowest_value:
                    lowest_value = value
                    value = action
        
        return lowest_value, lowest_action

#Only referencing below definitions rom Geek4Geek : https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
#Alpha is the best value that the maximizer currently can guarantee at that level or above. 
#Beta is the best value that the minimizer currently can guarantee at that level or below.
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, action = self.max_value(gameState, 0, 0, float('-inf'), float('inf')) #(gamestate, current depth, agent, alpha, beta)
        return action
    
    def max_value(self, gameState : GameState, curr_depth, agent_idx, alpha, beta):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None#If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring

        if curr_depth == self.depth:
            return  self.evaluationFunction(gameState), None
        
        best_value = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(agent_idx):
            ret_val = self.min_value(gameState.generateSuccessor(agent_idx, action), curr_depth, agent_idx + 1, alpha, beta) #ret val needed because max returns tuple but not min and we only care about value
            
            if ret_val[0] > best_value: #new child better choice?
                best_value = ret_val[0]
                best_action = action

            if best_value > beta:
                best_action = action
                return best_value, best_action
            alpha = max(alpha, best_value)
        return best_value, best_action


    def min_value(self, gameState : GameState, curr_depth, agent_idx, alpha, beta):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None #If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring
        
        worst_value = float('inf')
        worst_action = None

        for action in gameState.getLegalActions(agent_idx):
            ret_val = self.value(gameState.generateSuccessor(agent_idx, action), curr_depth, agent_idx, alpha, beta)
            worst_value = min(worst_value, ret_val[0])
            beta = min(beta, worst_value)
            if worst_value < alpha:
                worst_action = action
                return worst_value, worst_action
        return worst_value, worst_action

        
    def value(self, gameState : GameState, curr_depth, agent_idx, alpha, beta):
        if agent_idx == gameState.getNumAgents()-1: #If the next agent is pacman, i.e. current agent is last agent
            return self.max_value(gameState, curr_depth + 1, 0, alpha, beta)
        return self.min_value(gameState, curr_depth, agent_idx + 1, alpha, beta)
    



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
        value, action = self.max_value(gameState, 0, 0) #(gamestate, current depth, agent)
        return action
        #each iteration, max value gets pacman moves, then chains to min values of ghost moves
        #Then it will send the best action, get sucessor of that and send it to max value again 
    
    
    def max_value(self, gameState : GameState, agent_idx, curr_depth):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None#If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring

        best_value = float('-inf')
        best_action = None
        
        if curr_depth == self.depth:
            return  self.evaluationFunction(gameState), None
        else:
            for action in gameState.getLegalActions(agent_idx):
                value, ghost_action = self.chance_value(gameState.generateSuccessor(agent_idx, action), agent_idx + 1, curr_depth) #Next game state after pacman, (The state after agent makes move, next agent)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_value, best_action
        
    def chance_value(self, gameState : GameState, agent_idx, curr_depth):
        if gameState.isLose():
            return  self.evaluationFunction(gameState), None #If this game state loses the game dont keep exploring
        if gameState.isWin():
            return self.evaluationFunction(gameState), None #if game state wins, do this, dont need to keep exploring
        
        average_value = 0
        #Instead of returning just values, return the weighted values of the get legal actions
        if agent_idx == gameState.getNumAgents()-1: #-1 because agent_idx is zero indexed but num agents presumeably is not
            for action in gameState.getLegalActions(agent_idx):
                value, pac_action = self.max_value(gameState.generateSuccessor(agent_idx, action), 0, curr_depth + 1)
                average_value +=  (1/len(gameState.getLegalActions(agent_idx))) * value
        else:
            for action in gameState.getLegalActions(agent_idx):
                value, ghost_action = self.chance_value(gameState.generateSuccessor(agent_idx, action), agent_idx + 1, curr_depth)
                average_value +=  (1/len(gameState.getLegalActions(agent_idx))) * value
        return average_value, None
    
        
# Games of chance can be handled by expectiminimax, an extension to the minimax 
# algorithm that evaluates a chance node by taking the average utility of all its children,
# weighted by the probability of each child.
#(Russel and Norvig)



def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    My initial thought is use the manhatten distance again, I thought that was a good idea. The main problem with that algorithm though was that it didnt account for walls, and the cloesest food could be on the other side of the wall. Essentially, my next improvement would be to figure out, if there is a wall and a food on the other side, how do I get pacman to go around the wall.

    I think using BFS would work for this since at eveery pos I can check for walls, BFS code referenced from my own BFS code in HW1, okay so BFS is way too slow and also kind of doesnt work

    UPDATE
    Okay so I just used my cloesest food code from ealier and subtracted that from eval. This suprising worked for almost all the games, but I noticed that if pacman got themselves into a corner or somewhere with walls on three sides then it would get stuck and a ghost went end up catching it. So I just added a check so that if pacman has three walls on any side then give a significant penalty to that state
    """
    "*** YOUR CODE HERE ***"
    eval = currentGameState.getScore()

    #Check if start is goal
    if currentGameState.isWin(): return float('inf')
    if currentGameState.isLose(): return float('-inf')
    

    x,y = currentGameState.getPacmanPosition()
    walls = currentGameState.getWalls()
    
    ctr = 0
    if walls[x+1][y]: ctr += 1
    if walls[x][y+1]: ctr += 1
    if walls[x-1][y]: ctr += 1
    if walls[x][y-1]: ctr += 1

    if ctr >= 3:
        eval -= 1000

    closest_food = min([manhattanDistance(currentGameState.getPacmanPosition(), food) for food in currentGameState.getFood().asList()])
    
    return eval - closest_food



# Abbreviation (don't modify existing, but you can add to them)
better = betterEvaluationFunction
score = scoreEvaluationFunction
