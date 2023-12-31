# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from multiprocessing import current_process
import queue
from select import select
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    node = problem.getStartState()
    stack = util.Stack()
    visited = []

    if problem.isGoalState(node):
        return []
    
    stack.push((node, []))

    while not stack.isEmpty():
        node, actions = stack.pop()
        
        if problem.isGoalState(node):
            return actions  # Return the list of actions if the goal state is reached

        if node not in visited:
            visited.append(node)  # Put to the visited list the actual node
            successors = problem.getSuccessors(node)
            for next_node, action, cost in successors:  # Look for each successor of the actual node
                if next_node not in visited:
                    stack.push((next_node, actions + [action]))  # Push the next node and the updated action list onto the stack
    return actions

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = problem.getStartState()
    queue = util.Queue()
    visited = []

    if problem.isGoalState(node):
        return
    
    queue.push((node, []))

    while not queue.isEmpty():
        node, actions = queue.pop()
        
        if problem.isGoalState(node):
            return actions  # Return the list of actions if the goal state is reached

        if node not in visited:
            visited.append(node)  # Put to the visited list the actual node
            successors = problem.getSuccessors(node)

            for next_node, action, cost in successors:  # Look for each successor of the actual node
                if next_node not in visited:
                    queue.push((next_node, actions + [action]))  # Push the next node and the updated action list onto the stack

    return actions

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState =problem.getStartState()

    queue_frontier = util.PriorityQueue()
    
    queue_frontier.push((startState,0), 0)

    cost_so_far = {startState:0}
    came_from = {}

    while not queue_frontier.isEmpty():
        
        current_node, current_cost = queue_frontier.pop()

        if problem.isGoalState(current_node):
            break
        
        for neighbor, action, weight in problem.getSuccessors(current_node):
            
            new_cost = cost_so_far[current_node] + weight

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                queue_frontier.push((neighbor, new_cost),new_cost)
                came_from[neighbor] = (current_node, action)
    
    path = []
    while current_node != startState:
        current_node_tuple = came_from[current_node]
        current_node = current_node_tuple[0]
        current_action = current_node_tuple[1]
        path.append(current_action)
    # path.append(startState)
    path.reverse()
    # print(path)
    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    open_list = [(problem.getStartState(), [], 0, 0)]  # State, path, g, f
    closed_list = set()

    while open_list:
        current_state, actions, g, f = min(open_list, key=lambda x: x[3])
        open_list.remove((current_state, actions, g, f))

        if problem.isGoalState(current_state):
            return actions

        closed_list.add(current_state)

        for next_state, action, cost in problem.getSuccessors(current_state):
            if next_state not in closed_list:
                new_path = actions + [action]
                new_g = g + cost
                new_f = new_g + heuristic(next_state, problem)
                open_list.append((next_state, new_path, new_g, new_f))

    return []  # No path found
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
