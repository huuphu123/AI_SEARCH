import queue


class Box:
    def __init__(self, type, dependencies=None, typeFunction=None, activateValue=0):
        self.type = type
        self.dependencies = dependencies
        self.typeFunction = typeFunction
        self.activateValue = activateValue
        # 1: positive activate, -1 negative activate, 2: bridge open, -2 bridge close, 3: brigde initial, -3 teleport just activate


class State:
    def __init__(self, location, map, locationSwitch, isSplit=False, action=None, parent=None):
        self.location = location
        self.map = map
        self.locationSwitch = locationSwitch
        self.isSplit = isSplit
        self.parent = parent
        self.action = action
        if len(self.location) == 1:
            self.state = 1  # standing
        if len(self.location) == 2:
            if self.location[0][0] == self.location[1][0]:
                self.state = 2  # through X
            else:
                self.state = 3  # through Y
        if self.isSplit == True:
            if self.checkSplitUnion(self.location):
                self.isSplit = False

    def copyMap(self, otherMap):
        map = []
        for x in range(len(otherMap)):
            map.append([])
            for y in range(len(otherMap[0])):
                box_new = Box(otherMap[x][y].type, otherMap[x][y].dependencies, otherMap[x][y].typeFunction,
                              otherMap[x][y].activateValue)
                map[x].append(box_new)
                if box_new.activateValue == -3:
                    box_new.activateValue -= 1
        return map

    def checkSplitUnion(self, location):
        x, y = location
        if ((x[0] == y[0]) and (abs(x[1] - y[1]) == 1)) or ((x[1] == y[1]) and (abs(x[0] - y[0]) == 1)):
            return True

    def checkLegalMove(self, newLocation):
        for i in newLocation:
            if i[0] < 0 or i[0] >= len(self.map) or i[1] < 0 or i[1] >= len(self.map[0]):
                return False
            if self.map[i[0]][i[1]].type == '0':
                return False

        if len(newLocation) == 1:
            if self.map[newLocation[0][0]][newLocation[0][1]].type == 'C':
                return False
        return True

    def getX(self, tupple, newLocation):
        x, y = tupple
        cloneMap = self.copyMap(self.map)
        typeFunction = self.map[x][y].typeFunction
        listDependencies = self.map[x][y].dependencies

        if len(newLocation) == 1:
            if typeFunction == 1:  # close to open to closed
                for i in listDependencies:
                    if cloneMap[i[0]][i[1]].type == '0':
                        cloneMap[i[0]][i[1]].type = '1'
                        cloneMap[x][y].activateValue = 1
                        cloneMap[i[0]][i[1]].activateValue = 2
                    else:
                        cloneMap[i[0]][i[1]].type = '0'
                        cloneMap[x][y].activateValue = -1
                        cloneMap[i[0]][i[1]].activateValue = -2
            if typeFunction == 2:  # only close
                for i in listDependencies:
                    if cloneMap[i[0]][i[1]].type == '1':
                        cloneMap[i[0]][i[1]].type = '0'
                        cloneMap[x][y].activateValue = -1
                        cloneMap[i[0]][i[1]].activateValue = -2
            if typeFunction == 3:  # only open
                for i in listDependencies:
                    if cloneMap[i[0]][i[1]].type == '0':
                        cloneMap[i[0]][i[1]].type = '1'
                        cloneMap[x][y].activateValue = 1
                        cloneMap[i[0]][i[1]].activateValue = 2
        return (cloneMap, newLocation, False)

    def getO(self, tupple, newLocation):
        x, y = tupple
        cloneMap = self.copyMap(self.map)
        typeFunction = self.map[x][y].typeFunction
        listDependencies = self.map[x][y].dependencies

        if typeFunction == 1:  # close to open to closed
            for i in listDependencies:
                if cloneMap[i[0]][i[1]].type == '0':
                    cloneMap[i[0]][i[1]].type = '1'
                    cloneMap[x][y].activateValue = 1
                    cloneMap[i[0]][i[1]].activateValue = 2
                else:
                    cloneMap[i[0]][i[1]].type = '0'
                    cloneMap[x][y].activateValue = -1
                    cloneMap[i[0]][i[1]].activateValue = -2
        if typeFunction == 2:  # only close
            for i in listDependencies:
                if cloneMap[i[0]][i[1]].type == '1':
                    cloneMap[i[0]][i[1]].type = '0'
                    cloneMap[x][y].activateValue = -1
                    cloneMap[i[0]][i[1]].activateValue = -2
        if typeFunction == 3:  # only open
            for i in listDependencies:
                if cloneMap[i[0]][i[1]].type == '0':
                    cloneMap[i[0]][i[1]].type = '1'
                    cloneMap[x][y].activateValue = 1
                    cloneMap[i[0]][i[1]].activateValue = 2
        return (cloneMap, newLocation, False)

    def getT(self, tupple, newLocation):
        x, y = tupple
        # cloneMap = copy.deepcopy(self.map)
        cloneMap = self.copyMap(self.map)
        listDependencies = self.map[x][y].dependencies
        cloneLocation = []
        if len(newLocation) == 1:
            for i in listDependencies:
                cloneLocation.append(i)
                cloneMap[i[0]][i[1]].activateValue = -3
            return (cloneMap, cloneLocation, True)
        return (cloneMap, newLocation, False)

    def renderMap(self, newLocation):
        for i in self.locationSwitch:
            if i in newLocation:
                type = self.map[i[0]][i[1]].type
                if type == 'X':
                    return self.getX(i, newLocation)
                if type == 'O':
                    return self.getO(i, newLocation)
                if type == 'T':
                    return self.getT(i, newLocation)
        return (self.copyMap(self.map), newLocation, False)

    def moveUp(self, id=None):
        newLocation = []
        if not self.isSplit:
            if self.state == 1:  # standing
                newLocation = [(self.location[0][0] - 2, self.location[0][1]),
                               (self.location[0][0] - 1, self.location[0][1])]
            elif self.state == 2:  # through X
                newLocation = [(self.location[0][0] - 1, self.location[0][1]),
                               (self.location[1][0] - 1, self.location[1][1])]
            else:  # through Y
                newLocation = [(min(self.location[0][0], self.location[1][0]) - 1, self.location[0][1])]
        else:
            if id == 1:
                newLocation = [(self.location[0][0] - 1, self.location[0][1]), self.location[1]]
            if id == 2:
                newLocation = [self.location[0], (self.location[1][0] - 1, self.location[1][1])]
        # Check điều kiện để sinh State mới
        if self.checkLegalMove(newLocation) == False:
            return None
        map, location, isSplit = self.renderMap(newLocation)
        if self.isSplit:
            return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=self.isSplit,
                         action='UP')
        return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=isSplit, action='UP')

    def moveDown(self, id=None):
        newLocation = []
        if not self.isSplit:
            if self.state == 1:  # standing
                newLocation = [(self.location[0][0] + 1, self.location[0][1]),
                               (self.location[0][0] + 2, self.location[0][1])]
            elif self.state == 2:  # through X
                newLocation = [(self.location[0][0] + 1, self.location[0][1]),
                               (self.location[1][0] + 1, self.location[1][1])]
            else:  # through Y
                newLocation = [(max(self.location[0][0], self.location[1][0]) + 1, self.location[0][1])]
        else:
            if id == 1:
                newLocation = [(self.location[0][0] + 1, self.location[0][1]), self.location[1]]
            if id == 2:
                newLocation = [self.location[0], (self.location[1][0] + 1, self.location[1][1])]
        # Check điều kiện để sinh State mới
        if self.checkLegalMove(newLocation) == False:
            return None
        map, location, isSplit = self.renderMap(newLocation)
        if self.isSplit:
            return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=self.isSplit,
                         action='DOWN')
        return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=isSplit, action='DOWN')

    def moveLeft(self, id=None):
        newLocation = []
        if not self.isSplit:
            if self.state == 1:
                newLocation = [(self.location[0][0], self.location[0][1] - 2),
                               (self.location[0][0], self.location[0][1] - 1)]
            elif self.state == 2:
                newLocation = [(self.location[0][0], min(self.location[0][1], self.location[1][1]) - 1)]
            else:
                newLocation = [(self.location[0][0], self.location[0][1] - 1),
                               (self.location[1][0], self.location[1][1] - 1)]
        else:
            if id == 1:
                newLocation = [(self.location[0][0], self.location[0][1] - 1), self.location[1]]
            if id == 2:
                newLocation = [self.location[0], (self.location[1][0], self.location[1][1] - 1)]

        # Check điều kiện để sinh State mới
        if not self.checkLegalMove(newLocation):
            return None
        map, location, isSplit = self.renderMap(newLocation)
        if self.isSplit:
            return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=self.isSplit,
                         action='LEFT')
        return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=isSplit, action='LEFT')

    def moveRight(self, id=None):
        newLocation = []
        if not self.isSplit:
            if self.state == 1:
                newLocation = [(self.location[0][0], self.location[0][1] + 1),
                               (self.location[0][0], self.location[0][1] + 2)]
            elif self.state == 2:
                newLocation = [(self.location[0][0], max(self.location[0][1], self.location[1][1]) + 1)]
            else:
                newLocation = [(self.location[0][0], self.location[0][1] + 1),
                               (self.location[1][0], self.location[1][1] + 1)]
        else:
            if id == 1:
                newLocation = [(self.location[0][0], self.location[0][1] + 1), self.location[1]]
            if id == 2:
                newLocation = [self.location[0], (self.location[1][0], self.location[1][1] + 1)]

        # Check điều kiện để sinh State mới
        if self.checkLegalMove(newLocation) == False:
            return None
        map, location, isSplit = self.renderMap(newLocation)
        if self.isSplit:
            return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=self.isSplit,
                         action='RIGHT')
        return State(location=location, map=map, locationSwitch=self.locationSwitch, isSplit=isSplit, action='RIGHT')

    def isGoal(self):
        if len(self.location) == 1 and self.map[self.location[0][0]][self.location[0][1]].type == 'G':
            return True
        else:
            return False

    def stateToString(self):
        ret = ""
        for i in range(len(self.location)):
            temp_list = [self.location[0], self.location[-1]]
            temp_list.sort()
            ret += str(temp_list[i][0]) + ' ' + str(temp_list[i][1]) + ' '
        for i in self.locationSwitch:
            switch = self.map[i[0]][i[1]]
            ret += str(switch.type)
            ret += str(switch.activateValue)
        return ret

    def print(self):
        print("-" * (len(self.map[0]) * 2 + 2))
        for i in range(len(self.map)):
            print('|', end='')
            for j in range(len(self.map[0])):
                if (self.map[i][j].type == '0'):
                    print(' ', end=' ')
                else:
                    if (i, j) in self.location:
                        print('#', end=' ')
                    else:
                        print(self.map[i][j].type, end=' ')
            print('|', end='')
            print()
        print("-" * (len(self.map[0]) * 2 + 2))


class Bloxorz:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        contents = contents.splitlines()
        arrayShape = contents[0].split(' ')
        arrayIndex = contents[1].split(' ')
        self.locationSwitch = []
        self.shape = (int(arrayShape[0]), int(arrayShape[1]))
        self.indexBlock = [(int(arrayIndex[0]), int(arrayIndex[1]))]

        clone_contents = contents[2: (2 + self.shape[0])]
        self.initial = []
        for i in range(self.shape[0]):
            row_contents = clone_contents[i].split(' ')
            row = []
            for j in row_contents:
                row.append(Box(type=j))
            self.initial.append(row)

        clone_contents = contents[(2 + self.shape[0]):]
        for i in clone_contents:
            row_contents = i.split(' ')
            name_switch = row_contents[0]
            typeSwitch = row_contents[1]
            index_x = int(row_contents[2])
            index_y = int(row_contents[3])
            self.locationSwitch.append((index_x, index_y))

            listDependencies = row_contents[4:]
            dependencies = []
            while len(listDependencies) != 0:
                dependencies.append((int(listDependencies[0]), int(listDependencies[1])))
                if name_switch != 'T':
                    self.initial[(int(listDependencies[0]))][int(listDependencies[1])].activateValue = 3
                listDependencies = listDependencies[2:]
            if name_switch != 'T':
                self.initial[index_x][index_y].typeFunction = int(typeSwitch)
            else:
                self.initial[index_x][index_y].typeFunction = None
            self.initial[index_x][index_y].dependencies = dependencies
        self.listState = []

    def getSuccessors(self, state):
        result = []
        if not state.isSplit:
            if state.moveUp() != None:
                result.append(state.moveUp())
            if state.moveDown() != None:
                result.append(state.moveDown())
            if state.moveLeft() != None:
                result.append(state.moveLeft())
            if state.moveRight() != None:
                result.append(state.moveRight())
        else:
            for i in range(2):
                if state.moveUp(i + 1) != None:
                    result.append(state.moveUp(i + 1))
                if state.moveDown(i + 1) != None:
                    result.append(state.moveDown(i + 1))
                if state.moveLeft(i + 1) != None:
                    result.append(state.moveLeft(i + 1))
                if state.moveRight(i + 1) != None:
                    result.append(state.moveRight(i + 1))
        return result

    def print_result(self, state):
        if state.parent != None:
            self.print_result(state.parent)
        print("ACTION: ", state.action)
        print("BLOCK LOCATION: ", state.location)
        state.print()
        print()

    def get_list_state(self, state):
        if state.parent != None:
            self.get_list_state(state.parent)

        self.listState.append(state)

    def DFS(self):
        self.num_explored = 0
        start = State(location=self.indexBlock, map=self.initial, locationSwitch=self.locationSwitch)
        frontier = queue.LifoQueue()
        frontier.put(start)
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")
            state = frontier.get()
            self.num_explored += 1
            if state.isGoal():
                curState = state
                print("State explored: ", self.num_explored)
                self.get_list_state(curState)
                return state
            self.explored.add(state.stateToString())
            for check_state in self.getSuccessors(state):
                if check_state.stateToString() not in self.explored:
                    check_state.parent = state
                    frontier.put(check_state)

    def print(self):
        print("-" * ((self.shape[1]) * 2 + 2))
        for i in range(self.shape[0]):
            print('|', end='')
            for j in range(self.shape[1]):
                if (self.initial[i][j].type == '0'):
                    print(' ', end=' ')
                else:
                    print(self.initial[i][j].type, end=' ')
            print('|', end='')
            print()
        print("-" * ((self.shape[1]) * 2 + 2))
