import queue
from node import *
from Color import Color
import os

class WaterSortSolver:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        contents = contents.splitlines()
        self.num_cups = int(contents[0])
        self.capacity = int(contents[1])
        self.set = set()
        self.Color = {}
        self.path = []
        self.state = []

        contents = contents[2:]
        self.initial = []
        for i in range(self.num_cups):
            if i >= len(contents):
                self.initial.append('')
            else:
                row = contents[i].replace(' ', '')
                self.initial.append(row)
                for symbol in row:
                    self.set.add(symbol)
        index = 2
        for i in self.set:
            if index >= 30:
                self.Color[i] = Color[0]
            else:
                self.Color[i] = Color[index]
            index += 1


    def numColorSimilar(self, row):
        clone_row = row[:]
        if len(clone_row) == 0:
            count = 0
        else:
            count = 1
            top_color = clone_row[-1]
            clone_row = clone_row[:-1]
            while len(clone_row) != 0:
                check_color = clone_row[-1]
                clone_row = clone_row[:-1]
                if check_color == top_color:
                    count += 1
                else:
                    break
        return count

    def getLegalMove(self, state, i, j):
        len_i = len(state[i])
        len_j = len(state[j])

        if len_i == 0 or len_j == self.capacity or (len_i != 0 and len_j != 0 and state[i][-1] != state[j][-1]):
            return None
        else:

            num = self.numColorSimilar(state[i])
            sum_check = num + len_j
            if sum_check > self.capacity:
                return i, j, self.capacity - len_j
            else:
                return i, j, num

    def move(self, state, legal_move_tuple):
        clone_state = []
        for cup in state:
            clone_state.append(cup)

        i, j, num_to_move = legal_move_tuple

        while num_to_move != 0:
            color_out = clone_state[i][-1]
            clone_state[i] = clone_state[i][:-1]
            clone_state[j] += color_out
            num_to_move -= 1
        return clone_state

    def successors(self, state):
        result = []
        for i in range(self.num_cups):
            num_met_empty_cup = 0
            for j in range(self.num_cups):
                if i == j:
                    continue
                if len(state[j]) == 0:
                    if num_met_empty_cup > 0 or len(set([color for color in state[i]])) == 1:
                        continue
                    else:
                        num_met_empty_cup += 1
                legal_move = self.getLegalMove(state, i, j)
                if legal_move is not None:
                    result.append((self.move(state, legal_move), legal_move))
        return result

    ############################################################################################

    def isGoal(self, state):
        count = 0
        for i in range(self.num_cups):
            if self.numColorSimilar(state[i]) == self.capacity or self.numColorSimilar(state[i]) == 0:
                count += 1
        if count == self.num_cups:
            return True
        else:
            return False

    def printState(self, state):
        # Print current status
        if state is None:
            print(None)
            return None
        a = ''
        space = " " * 3
        for j in range(self.capacity - 1, -1, -1):
            for i in range(self.num_cups):
                if len(state[i]) > j:
                    color = state[i][j]
                else:
                    color = "."
                a += "|" + ("%s" % color).center(4) + "|" + space
            a += "\n"
        for i in range(self.num_cups):
            a += "\\" + "_".center(4, "_") + "/" + space
        return a

    def stateToString(self, state):
        ret_str = str()
        index = 0
        for cup in state:
            ret_str += str(index)
            ret_str += cup
            index += 1
        return ret_str
    

    def printResult(self, testcase):
        path = 'result/result_testcase' + testcase + '.txt'
        if os.path.isfile(path):
            os.remove(path)
        a = 0
        with open(path,"w") as f:
            for i in self.state:
                if a != 0:
                    f.write(f'CUP {str(i.action[0])} -> CUP {str(i.action[1])}')
                    f.write("\n")
                a += 1
                f.write(self.printState(i.state))                
                f.write("\n")
                f.write("\n")

    
    def get_path(self,node):
        if node.parent is not None:
            self.get_path(node.parent)
        self.path.append(node.action)
        self.state.append(node)

    def h_function(self, state):
        h_value = 0

        for cup in state:
            cup_value = 0
            cur_index = 0

            while cur_index < len(cup) - 1:
                if cup[cur_index] != cup[cur_index + 1]:
                    cup_value += 1
                cur_index += 1
            h_value += cup_value

        list_color__at_bottom = []
        for cup in state:
            if len(cup) > 0:
                list_color__at_bottom.append(cup[0])
        h_value += len(list_color__at_bottom) - len(set(list_color__at_bottom))
        return h_value

    def search(self, type_search):

        num_explored = 0

        if type_search == 'BFS':
            start = NodeForBFS(state=self.initial)
            frontier = queue.Queue()
        elif type_search == 'DFS':
            start = NodeForBFS(state=self.initial)
            frontier = queue.LifoQueue()
        elif type_search == 'A_Star':
            start = NodeForAStar(state=self.initial, parent=None, action=None,
                                 g_value=0, f_value=self.h_function(self.initial))
            frontier = queue.PriorityQueue()
        else:
            raise "Check typeSearch!"

        if self.isGoal(start.state):
            return start
        frontier.put(start)
        explored = set()  # set of string encoded by each state
        result = None

        while not frontier.empty() and num_explored < 45000:
            cur_node = frontier.get()
            num_explored += 1

            if self.isGoal(cur_node.state):
                result = cur_node
                self.get_path(cur_node)
                self.path = self.path[1:]
                return result
            
            explored.add(self.stateToString(cur_node.state))

            for state, legal_move in self.successors(cur_node.state):
                if self.stateToString(state) not in explored:
                    if type_search in ['BFS', 'DFS']:
                        child = NodeForBFS(state=state, parent=cur_node, action=legal_move)
                    elif type_search == 'A_Star':
                        next_g_value = cur_node.g_value + 1
                        next_f_value = 3 * self.h_function(state) + 1 * next_g_value
                        child = NodeForAStar(state=state, parent=cur_node, action=legal_move,
                                             g_value=next_g_value, f_value=next_f_value)
                    frontier.put(child)

        if result is None:
            print("No solution")

        print("number explored node: " + str(num_explored))
        return result


