# CS 411 - Assignment 3 Starter Code
# Iteratie Deepening Search on 15 Puzzle
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))

class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path
    
    # This function get the depth of any nodes by backtracking and counting the number of parents
    def get_depth(self, node):
        depth = 0
        while (node.parent is not None):
            depth += 1
            node = node.parent
        return depth

    # This function checked for a cycle in a node
    def cycle_check(self, node):
        hashset = set()
        hashset.add(str(node.__hash__()))
        temp_hash_string = ""
        while (node.parent is not None):
            node = node.parent
            temp_hash_string = str(node.__hash__())
            if (temp_hash_string in hashset):
                return True
            hashset.add(temp_hash_string)
        return False
            
    # This function run depth_limited_search from 0 to inf in order to search the 16-puzzle
    def ids(self, root_node):
        depth_lim = 0
        result = "Failure"
        while result == "Failure" or result == "Cutoff": 
            result = self.run_depth_limited_search(root_node, depth_lim)
            depth_lim += 1
        return result

    # This function searching for goal states with depth_limit as a limit parameter for function to stop
    def run_depth_limited_search(self, root_node, depth_limit):
        start_time = time.time()
        frontier = deque([root_node])
        result = "Failure"
        max_memory = 0
        explored = set()
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            cur_node = frontier.pop()
            explored.add(cur_node)
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()
                result = "Solved"
                return path, len(explored), (end_time - start_time), max_memory
            if self.get_depth(cur_node) > depth_limit:
                result = "Cutoff"
            elif not self.cycle_check(cur_node):
                for child in self.get_children(cur_node):
                    frontier.append(child)
        return result
    
    # This function get all the misplay tiles between original states and the current node states excluding blank (number 0)
    def get_difference(self, cur_tiles):
        difference = 0
        goal_states = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        for i in range(0, 16):
            if goal_states[i] != cur_tiles[i] and cur_tiles[i] != '0':
                difference += 1
        return difference

    # This function get all the manhanttan distance of all square between original states and the current node states excluding blank (number 0)
    def manhattan_distance(self, cur_tiles):
        total_manhattan_distance = 0
        goal_states = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
        x_curr_square = 0
        y_curr_square = 0
        x_original = 0
        y_original = 0
        for i in range(0, len(cur_tiles)):
            curr_square = cur_tiles[i]
            x_curr_square = i % 4
            y_curr_square = i // 4
            for j in range(0, len(goal_states)):
                for k in range(0, 4):
                    if goal_states[j][k] == curr_square:
                        x_original = k
                        y_original = j
            if curr_square != '0':
                total_manhattan_distance += abs(x_original - x_curr_square) + abs(y_original - y_curr_square)
        return total_manhattan_distance

    # This function run A* for the misplayed tiles as h function
    # The g function is the depth funcion, with each depth cost 1
    # f(A*) = g(depth) + h(misplayed_tiles)
    def A_star_misplayed_titles(self, root_node):
        start_time = time.time()
        frontier = list([root_node])
        max_memory = 0
        explored = set()
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            minElement = frontier[0]
            min_f_value = self.get_difference(frontier[0].state.tiles) + self.get_depth(frontier[0])
            minIndex = 0
            # Choose the lowest f value
            for i in range(0, len(frontier)):
                if self.get_difference(frontier[i].state.tiles) + self.get_depth(frontier[i]) < min_f_value:
                    minElement = frontier[i]
                    min_f_value = self.get_difference(frontier[i].state.tiles) + self.get_depth(frontier[i])
                    minIndex = i
            cur_node = minElement
            explored.add(cur_node)
            # If goal reached, return goal
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()
                return path, len(explored), (end_time - start_time), max_memory
            frontier.remove(frontier[minIndex])
            # Add child to the frontier
            # We dont need the condition to choose smallest tentative g because we expanded a layer, all depth of children is 1 more
            # All children of the same node will have the same g(score)
            for child in self.get_children(cur_node):
                if child not in explored:
                    frontier.append(child)        
        return False
    
    # This function run A* for the A* manhantan distance as h function
    # The g function is the depth funcion, with each depth cost 1
    # f(A*) = g(depth) + h(manhantan distance)
    def A_star_manhattan_distance(self, root_node):
        start_time = time.time()
        frontier = list([root_node])
        max_memory = 0
        explored = set()
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            minElement = frontier[0]
            min_f_value = self.manhattan_distance(frontier[0].state.tiles) + self.get_depth(frontier[0]) 
            minIndex = 0
            # Choose the lowest f value
            for i in range(0, len(frontier)):
                if self.manhattan_distance(frontier[i].state.tiles) + self.get_depth(frontier[i]) < min_f_value:
                    minElement = frontier[i]
                    min_f_value = self.manhattan_distance(frontier[i].state.tiles) + self.get_depth(frontier[i]) 
                    minIndex = i
            cur_node = minElement
            explored.add(cur_node)
            # If goal reached, return goal
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()
                return path, len(explored), (end_time - start_time), max_memory
            frontier.remove(frontier[minIndex])
            # Add child to the frontier
            # We dont need the condition to choose smallest tentative g because we expanded a layer, all depth of children is 1 more
            # All children of the same node will have the same g(score)
            for child in self.get_children(cur_node):
                if child not in explored:
                    frontier.append(child)
        return False

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):
        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.A_star_manhattan_distance(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
    agent.solve("1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12")