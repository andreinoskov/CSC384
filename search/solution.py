#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
import math  # for infinity
import heapq
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems

def sokoban_goal_state(state):
    '''
    @return: Whether all boxes are stored.
    '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True

def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.

    # Will take the simplest approach. Basically will take the manhatten distance of a box to each storage point and find the minimum.
    # Will then repeat the process for each box.
    mandist = 0

    for box in state.boxes:
        minim = math.inf
        #create a list of all manhatten distances between storagepoints
        for storage in state.storage:
            potdist = abs(box[0]-storage[0])+ abs(box[1]-storage[1])
            if potdist < minim:
                minim = potdist
        # increment mandist and creal list for next box
        mandist = mandist + minim
    
    return mandist

# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    #I have no idea about this function as it wasn't specified in the assumption
    # will use Euler distance because it is the most trivial heuristic I can think
    # of.
    eudist = 0
    for box in state.boxes:
        listmindist = []
        #create a list of all manhatten distances between storagepoints
        for storage in state.storage:
            potdist = math.sqrt((box[0]-storage[0])**2+(box[1]-storage[1])**2)
            listmindist.append(potdist)

        # increment mandist and creal list for next box
        eundist = eudist + min(potdist)
        listmindist = []
    
    return mandist

# helper function for heur_alt which sees if box is in a corner

def cornbox(state, storage):
    ''' Takes a state as an input and returns True if it haxs a box that is not in corner'''
    #boxnothome = []
    for box in state.boxes:
        if box not in storage:
            if (box[0] == 0 or box[0] == state.width-1) and (box[1] == 0 or box[1] == state.height-1):
                return True
    #        else:
    #            boxnothome.append(box)
    '''
    for box in boxnothome:
        if (box[0]-1, box[1]) in state.obstacles and (box[0], box[1]+1) in state.obstacles:
            return True
        if (box[0]+1, box[1]) in state.obstacles and (box[0], box[1]-1) in state.obstacles:
            return True
        if (box[0]-1, box[1]-1) in state.obstacles and (box[0], box[1]-1) in state.obstacles:
            return True
        if (box[0]+1, box[1]+1) in state.obstacles and (box[0], box[1]+1) in state.obstacles:
            return True
    '''
    return False

def edgeboxind(state, box, storage):
    if storage[0] != box [0] and (box[0] == 0 or box[0] == state.width-1):
         return True
    if storage[1] != box [1] and (box[1] == 0 or box[1] == state.height-1):
         return True
    else:
        return False

def edgeboxtot(state, boxes, storagelist):
    for storage in storagelist:
        for box in boxes:
            if not edgeboxind(state, box, storage):
                return False
    return True

        


 
def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    
    mandist = 0

    mandist = 0
    storagelist = list(state.storage)
    if edgeboxtot(state, state.boxes, state.storage):
        mandist = math.inf

    elif cornbox(state, state.storage):
        mandist = math.inf
    
    else:
        for box in state.boxes:
            minim = math.inf
            stor = None
        #create a list of all manhatten distances between storagepoints
            for storage in storagelist:
                potdist = abs(box[0]-storage[0])+ abs(box[1]-storage[1])

                for obstacle in state.obstacles:
                    if obstacle[0] in range(min([box[0], storage[0]]), max([box[0], storage[0]])) and obstacle[1] in range(min([box[1], storage[1]]), max([box[1], storage[1]])):
                        potdist = potdist + 2

                for robot in state.robots:
                    if robot[0] in range(min([box[0], storage[0]]), max([box[0], storage[0]])) and robot[1] in range(min([box[1], storage[1]]), max([box[1], storage[1]])):
                        potdist = potdist + 2
                        
                if potdist < minim:
                    minim = potdist
                    stor = storage
        # increment mandist and creal list for next box
            mandist = mandist + minim
            storagelist.remove(stor)
    
    return mandist

    '''
    mandist = 0
    storagelist = list(state.storage)
    if edgeboxtot(state, state.boxes, state.storage):
        mandist = math.inf

    elif cornbox(state, state.storage):
        mandist = math.inf
    
    else:
        for box in state.boxes:
            minim = math.inf
            stor = None
        #create a list of all manhatten distances between storagepoints
            for storage in storagelist:
                for robot in state.robots:
                    potdist = abs(box[0]-storage[0])+ abs(box[1]-storage[1])+ abs(robot[1]-storage[1]) + abs(robot[0]-storage[0])
                    if potdist < minim:
                        minim = potdist
                        stor = storage
        # increment mandist and creal list for next box
            mandist = mandist + minim
            storagelist.remove(stor)
    
    return mandist
    '''

    '''
    mandist = 0
    mindist = math.inf
    storagelist = []
    boxlist = []
    

    for box in state.boxes:
        if box not in state.storage:
            boxlist.append(box)

    for storage in state.storage:
        if storage not in state.boxes:
            storagelist.append(storage)
            
    if storagelist == []:
        return 0
    
        
    elif cornbox(state, boxlist):
        mandist = math.inf
        return mandist
                    

    else:
        if edgeboxtot(state, boxlist, storagelist):
            mandist = math.inf
            return mandist
        dist = 0
        for storage in storagelist:
            for box in boxlist:
                potdist = abs(box[0]-storage[0])+abs(box[1]-storage[1])
                
                if potdist < mindist:
                    mindist = potdist

            #surrounding = ((box[0] + 1, box[1]-1), (box[0] + 1, box[1]), (box[0] + 1, box[1]+1), (box[0] , box[1]-1), (box[0] , box[1]+1) , (box[0] - 1, box[1]-1) ,(box[0] - 1, box[1]),(box[0] - 1, box[1] +1))
            dist += mindist #+ len(set(surrounding)&set(state.obstacles))
        mindist = dist

    
    return mindist
    '''

    """
    altdist = 0
    mindist = []
    minret = 0
    lengthlist = len(state.boxes)
    for box in state.boxes:
        for storage in state.storage:
            potdist = math.sqrt((box[0]-storage[0])**2+(box[1]-storage[1])**2) + abs(box[0]-storage[0]) +abs(box[1]-storage[1])
            mindist.append(potdist)
    
    minret = minret + min(mindist)
    
    return minret
    """
    #while i < len(state.boxes):
     #   u = min(mindist)
      #  altdist = altdist + u
       # minindex = mindist.index(u)
        #j = 0
        
        #while j < len(mindist):
         #   if j%lengthlist == minindex:
           #     mindist.pop(j)
          #  j = j + 1

        #lengthlist = lengthlist - 1
        
       # i = i + 1
    #altdist = sum(mindist)
    #return altdist

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    return sN.gval + weight*sN.hval

# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound):
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of weighted astar algorithm
    '''
    
    goalstate, Stat = False, None
    searcher = SearchEngine('custom')
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    searcher.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn, fval_function = wrapped_fval_function)
    goalstate, Stat = searcher.search(timebound)
    return goalstate, Stat
                

                
def iterative_astar(initial_state, heur_fn, weight=1, timebound=5):  # uses f(n), see how autograder initializes a search line 88
    # IMPLEMENT
    '''Provides an implementation of realtime a-star, as described in the HW1 handout'''
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of realtime astar algorithm'''
    time = os.times()[0]
    goalstate, Stat = False, None
    goalstate2 = True
    searcher = SearchEngine('custom')
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    searcher.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn, fval_function = wrapped_fval_function)
    goalstate, Stat = searcher.search(timebound)
    pastgval = math.inf
    fintime = os.times()[0]
    newweight = weight
    while fintime - time < timebound and goalstate != False and pastgval< goalstate.gval: # and goalstate2 != goalstate:
        newweight = 3/4* newweight
        wrapped_fval_function = (lambda sN: fval_function(sN, newweight))
        searcher.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn, fval_function = wrapped_fval_function)
        goalstate2 = goalstate
        pastgval = goalstate.gval
        goalstate, Stat = searcher.search(timebound)
        fintime = os.times()[0]
    return goalstate, Stat
    

def hval (sNode):
    return sNode.hval

def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    time = os.times()[0]
    goalstate, Stat = False, None
    pastgval = math.inf
    searcher = SearchEngine('best_first')
    searcher.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn, fval_function = hval)
    goalstate, Stat = searcher.search(timebound)
    fintime = os.times()[0]
    while fintime-time < timebound and goalstate != False and pastgval < goalstate.gval:# and goalstate2 != goalstate:
        gval = goalstate.gval
        costbound = (goalstate.gval, goalstate.gval, goalstate.gval)
        pastgval = goalstate.gval
        fintime = os.times()[0]
        newtimebound = timebound - (fintime - time)
        goalstate, Stat = searcher.search(timebound, costbound)
    return goalstate, Stat
                
                
            
    

    




