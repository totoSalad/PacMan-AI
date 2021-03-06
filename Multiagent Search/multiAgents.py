# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        curFood = currentGameState.getFood()
        curFoodList = curFood.asList()
        curPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newFoodList = newFood.asList()

        ghostPositions = successorGameState.getGhostPositions()
        distance = float("inf")
        scared = newScaredTimes[0] > 0
        for ghost in ghostPositions:
          d = manhattanDistance(ghost, newPos)
          distance = min(d, distance)
        
        distance2 = float("inf")        
        distance3 = float("-inf")
        distance4 = float("inf")
        for food in newFoodList:
          d = manhattanDistance(food, newPos)
          d0 = manhattanDistance(food, curPos)
          distance2 = min(d, distance2)
          distance3 = max(d, distance3)

        cond = len(newFoodList) < len(curFoodList)
        count = len(newFoodList)
        if cond:
          count = 10000
        if distance < 2:
          distance = -100000
        else:
          distance = 0
        if count == 0:
          count = -1000
        if scared:
          distance = 0
        return distance + 1.0/distance2 + count - successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        
        v = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = minimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction
        
def minimax(agent, agentList, state, depth, evalFunc):
  
  if depth <= 0 or state.isWin() == True or state.isLose() == True:
    return evalFunc(state)
    
  if agent == 0:
    v = float("-inf")
  else:
    v = float("inf")
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  for j in range(len(successors)):
    successor = successors[j];
    
    if agent == 0:
      
      v = max(v, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
    elif agent == agentList[-1]:
      
      v = min(v, minimax(agentList[0], agentList, successor, depth - 1, evalFunc))
    else:
     
      v = min(v, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
  
  return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        v = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = minimaxPrune(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction, alpha, beta)
            
            if temp > v:
              v = temp
              bestAction = successor[0]
            if v > beta:
              return bestAction
            alpha = max(alpha, v)
        return bestAction
        

def minimaxPrune(agent, agentList, state, depth, evalFunc, alpha, beta):
  
  if depth <= 0 or state.isWin() == True or state.isLose() == True:
    return evalFunc(state)
    
  if agent == 0:
    v = float("-inf")
  else:
    v = float("inf")
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  for successor in successors:
    
    if agent == 0:
      
      v = max(v, minimaxPrune(agentList[agent+1], agentList, successor, depth, evalFunc, alpha, beta))
      if v> beta:
        return v
      alpha = max (alpha, v)
    elif agent == agentList[-1]:
      
      v = min(v, minimaxPrune(agentList[0], agentList, successor, depth - 1, evalFunc, alpha, beta))
      if v<alpha:
        return v
      beta = min(beta, v)
    else:
     
      v = min(v, minimaxPrune(agentList[agent+1], agentList, successor, depth, evalFunc, alpha, beta))
      if v<alpha:
        return v
      beta = min(beta, v)
  return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        v = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = expectimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction
        

def expectimax(agent, agentList, state, depth, evalFunc):
  
  if depth <= 0 or state.isWin() == True or state.isLose() == True:
    return evalFunc(state)
    
  if agent == 0:
    v = float("-inf")
  else:
    v = 0
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  p = 1.0/len(successors)
  for j in range(len(successors)):
    successor = successors[j];
    
    if agent == 0:
      
      v = max(v, expectimax(agentList[agent+1], agentList, successor, depth, evalFunc))
    elif agent == agentList[-1]:
      
      v += p * expectimax(agentList[0], agentList, successor, depth - 1, evalFunc)
    else:
     
      v += p * expectimax(agentList[agent+1], agentList, successor, depth, evalFunc)
  
  return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    

    food = currentGameState.getFood()
    foodList = food.asList()
    pos = currentGameState.getPacmanPosition()
        
    ghostStates = currentGameState.getGhostStates()
    foodList = food.asList()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()

    distance = float("inf")
    scared = 0
    times = 1
    for time in scaredTimes:
      times += time
      if time > 2:
        scared+=1
    
    avgDist = 1
    ghostCount = 0
    for ghost in ghostPositions:
      d = manhattanDistance(ghost, pos)
      avgDist += d
      if d <= 15:
        ghostCount+=1
      distance = min(d, distance)

    avgDist = float(avgDist)/len(ghostPositions)
    distance2 = float("inf")  

    for food in foodList:
      d = manhattanDistance(food, pos)
      distance2 = min(d, distance2)
      
    distance2+=1
    count = len(foodList) + 1

    legalMoves = len(currentGameState.getLegalActions(0)) +1
        
    if distance < 2:
      distance = -100000
    else:
      distance = 0
    
    score = currentGameState.getScore() + 1
    return distance + 1.0/distance2 + 10000.0/count - 50000*ghostCount + 50000*scared - 1000/times + 1.0/avgDist + 1000.0*score

# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = expectimax(1, range(gameState.getNumAgents()), successor[1], 3, contestEvaluationFunction)
            
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction


def contestEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    food = currentGameState.getFood()
    foodList = food.asList()
    pos = currentGameState.getPacmanPosition()
    grid = currentGameState.getWalls()
    ghostStates = currentGameState.getGhostStates()
    foodList = food.asList()
    capsules = len(currentGameState.getCapsules()) +1
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    from game import Actions

    q = util.Queue()
    q.push((pos, 0))
    dists = {}
    inq = set()
    inq.add(pos)
    while not q.isEmpty():
      cur,cost = q.pop()
      dists[cur] = cost
      for neighbor in Actions.getLegalNeighbors(cur, grid):
        if not neighbor in dists and not neighbor in inq:
          inq.add(neighbor)
          q.push((neighbor, cost + 1))

    distance = float("inf")
    scared = 0
    times = 1
    for time in scaredTimes:
      times += time
      if time > 2:
        scared+=1
    
    avgDist = 1
    ghostCount = 0
    for ghost in ghostStates:
      d = manhattanDistance(ghost.getPosition(), pos)
      avgDist += d
      if d <= 5 and ghost.scaredTimer <= 0:
        ghostCount+=1
      distance = min(d, distance)

    avgDist = float(avgDist)/len(ghostPositions)
    distance2 = float("inf")  

    for food in foodList:
      d = dists[food]
      distance2 = min(d, distance2)
      
    distance2+=1
    count = len(foodList) + 1

        
    if distance < 2:
      distance = -100000
    else:
      distance = 0
   
    if currentGameState.isWin():
      return 100000000000000000000000000
    
 
    
    score = currentGameState.getScore()
    return distance - 100*distance2 - 10000.0/count - 20000*ghostCount  - 1000/times + 1.0/avgDist + 10000000.0*score + 10000/capsules
