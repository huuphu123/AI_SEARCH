from dfs import *
import random


class GASolver:
    class Individual:
        def __init__(self, chromosome):
            self.chromosome = chromosome
            self.fitness_value = -1
            self.best_position = 1
            self.final_location = None

        def __getitem__(self, index):
            return self.chromosome[index]

        def __lt__(self, other):
            return self.fitness_value < other.fitness_value

    class Population:
        def __init__(self):
            self.individual_array = []
            self.best_individual = None
            self.size = 0
            self.sum_fitness = 0

        def __getitem__(self, index):
            return self.individual_array[index]

        def __contains__(self, individual):
            return individual in self.individual_array

        def add(self, list_idn):
            self.individual_array += list_idn
            self.size += len(list_idn)
            return self

    class MagicTableSolver:
        def magic_table_initial(self, magic_table, map):
            for x in range(len(map)):
                magic_table.append([])
                for y in range(len(map[0])):
                    if map[x][y].type == '0' and map[x][y].activateValue != 3:
                        magic_table[x].append(-2)
                    else:
                        magic_table[x].append(-1)
            return self

        def magic_table_calc(self, magic_table, map_game):
            x_g = y_g = 0
            for x in range(len(map_game)):
                for y in range(len(map_game[0])):
                    if map_game[x][y].type == 'G':
                        x_g = x
                        y_g = y
            self.calc_recur(magic_table, x_g, y_g)

        def get_element(self, magic_table, x_index, y_index):
            if not (0 <= x_index < len(magic_table) and 0 <= y_index < len(magic_table[0])):
                return None
            elif magic_table[x_index][y_index] < 0:
                return None
            else:
                return magic_table[x_index][y_index]

        def calc_recur(self, magic_table, x_g, y_g):
            queue_index = queue.Queue()
            queue_index.put((x_g, y_g))
            while not queue_index.empty():
                (x, y) = queue_index.get()
                if not (0 <= x < len(magic_table) and 0 <= y < len(magic_table[0])):
                    continue
                elif magic_table[x][y] == -2:
                    continue
                elif magic_table[x][y] != -1:
                    continue
                elif x == x_g and y == y_g:
                    magic_table[x_g][y_g] = 0
                else:
                    a = self.get_element(magic_table, x + 1, y)
                    b = self.get_element(magic_table, x - 1, y)
                    c = self.get_element(magic_table, x, y + 1)
                    d = self.get_element(magic_table, x, y - 1)
                    if not (x == x_g and y == y_g):
                        magic_table[x][y] = min([i for i in [a, b, c, d] if i is not None]) + 1
                queue_index.put((x + 1, y))
                queue_index.put((x - 1, y))
                queue_index.put((x, y + 1))
                queue_index.put((x, y - 1))

    def __init__(self, game):
        self.game = game
        self.population_size = 1000
        self.len_chromosome_min = 20
        self.len_chromosome_max = 30
        self.alphabet = ['R', 'r', 'L', 'l', 'U', 'u', 'D', 'd']
        self.x_para = 0.6
        self.y_para = 0.6
        self.goal_score = 5000000000
        self.magic_table = []
        self.magic_table_max = 0
        self.mts = self.MagicTableSolver()
        self.create_magic_table()

    def create_magic_table(self):
        mts = self.MagicTableSolver()
        mts.magic_table_initial(self.magic_table, self.game.initial)
        mts.magic_table_calc(self.magic_table, self.game.initial)
        self.magic_table_max = max([max(self.magic_table[i]) for i in range(len(self.magic_table))])

    def execute_individual(self, individual):
        cur_state = State(location=self.game.indexBlock, map=self.game.initial, locationSwitch=self.game.locationSwitch)
        cur_index, best_distance_position, best_distance = -1, 1, 1000
        refine_chromosome, state_key_list, state_key_set, special_location = [], [], set(), set()
        state_key_list.append(cur_state.stateToString())
        state_key_set.add(state_key_list[0])
        cur_state_list = [cur_state]
        for char_dna in individual.chromosome:
            id_cube = int('a' <= char_dna <= 'z') + 1
            move_dict = {'R': cur_state.moveRight, 'D': cur_state.moveDown, 'U': cur_state.moveUp, 'L': cur_state.moveLeft}
            next_state = move_dict[char_dna.upper()](id_cube)
            if next_state is not None:
                next_state_key = next_state.stateToString()
                if next_state_key in state_key_set:
                    cur_state_key = state_key_list[-1]
                    while cur_state_key != next_state_key:
                        state_key_list.pop()
                        refine_chromosome.pop()
                        state_key_set.remove(cur_state_key)
                        cur_state_list.pop()
                        cur_state_key = state_key_list[-1]
                        cur_index -= 1
                    cur_state = cur_state_list[-1]
                else:
                    cur_index += 1
                    cur_state = next_state
                    state_key_set.add(next_state_key)
                    state_key_list.append(next_state_key)
                    refine_chromosome.append(char_dna)
                    cur_state_list.append(cur_state)
                    cur_distance = (self.magic_table[cur_state.location[0][0]][cur_state.location[0][1]]
                                    + self.magic_table[cur_state.location[-1][0]][cur_state.location[-1][1]]) / 2
                    best_distance = cur_distance if cur_distance < best_distance else best_distance
                    best_distance_position = cur_index if best_distance == cur_distance else best_distance_position
            if cur_state.isGoal():
                individual.fitness_value = self.goal_score
                break
            self.check_special_location(cur_state, special_location)
        individual.best_position, individual.final_location = best_distance_position, cur_state.location
        individual.chromosome = refine_chromosome
        return cur_state, special_location

    def check_special_location(self, cur_state, special_location):
        # orange tile
        index_1 = (cur_state.location[0][0], cur_state.location[0][1])
        index_2 = (cur_state.location[-1][0], cur_state.location[-1][1])
        first_cube_location = cur_state.map[index_1[0]][index_1[1]]
        second_cube_location = cur_state.map[index_2[0]][index_2[1]]
        if first_cube_location.type == 'C':
            special_location.add((index_1, 'C'))
            special_location.add((index_2, 'C'))
        # activate X
        if first_cube_location.type == 'X' or second_cube_location.type == 'X':
            if len(cur_state.location) == 1:
                if first_cube_location.typeFunction == '3' \
                        or (first_cube_location.typeFunction == 1 and first_cube_location.activateValue == 1):
                    special_location.add((index_1, 'X'))
                elif first_cube_location.typeFunction == 1 and first_cube_location.activateValue == -1:
                    special_location.discard((index_1, 'X'))
        # activate O
        if first_cube_location.type == 'O' or second_cube_location.type == 'O':
            if first_cube_location.type == 'O' and first_cube_location.typeFunction != 2:
                if first_cube_location.activateValue == 1:
                    special_location.add((index_1, 'O'))
                else:
                    special_location.discard((index_1, 'O'))
            elif second_cube_location.type == 'O' and second_cube_location.typeFunction != 2:
                if second_cube_location.activateValue == 1:
                    special_location.add((index_2, 'O'))
                else:
                    special_location.discard((index_2, 'O'))
        # active bridge
        if first_cube_location.activateValue in {2, 3} or second_cube_location.activateValue in {2, 3}:

            if first_cube_location.activateValue in {2, 3}:
                special_location.add((index_1, 'B'))
            else:
                special_location.add((index_2, 'B'))
        # teleport
        if first_cube_location.activateValue == -3 or second_cube_location.activateValue == -3:
            if first_cube_location.activateValue == -3:
                special_location.add((index_1, 'T'))
            if second_cube_location.activateValue == -3:
                special_location.add((index_2, 'T'))

    def fitness_function(self, individual):
        execute_result = self.execute_individual(individual)
        if individual.fitness_value == self.goal_score:
            return self.goal_score
        (final_state, good_location) = execute_result
        distance = self.magic_table[final_state.location[0][0]][final_state.location[0][1]]
        distance += self.magic_table[final_state.location[-1][0]][final_state.location[-1][1]]
        distance /= 2
        internal_distance = 0
        if final_state.isSplit == 1:
            internal_distance += abs(final_state.location[0][0] - final_state.location[0][1]) + abs(
                final_state.location[-1][0] - final_state.location[-1][1])
        scoreC = sum([3000000 for x in good_location if x[1] == 'C'])
        scoreX = sum([3000000 for x in good_location if x[1] == 'X'])
        scoreB = sum([5000000 for x in good_location if x[1] == 'B'])
        scoreO = sum([3000000 for x in good_location if x[1] == 'O'])
        scoreN = sum([5000000 for x in good_location if x[1] == 'N'])
        scoreT = sum([3000000 for x in good_location if x[1] == 'T'])
        special_score = scoreC + scoreX + scoreO + scoreN + scoreB + scoreT
        bad_score = 0
        bridge_distance = 0
        goal_distance_weight = 1
        explore_weight = 0
        bridge_weight = 0
        for location in final_state.locationSwitch:
            if final_state.map[location[0]][location[1]].type not in ['O', 'X']:
                break
            for bridge_index in final_state.map[location[0]][location[1]].dependencies:
                if final_state.map[bridge_index[0]][bridge_index[1]].activateValue == '2' \
                        and (bridge_index, 'B') not in good_location:
                    bridge_distance += abs(final_state.location[0][0] - final_state.map[bridge_index[0]]) \
                                       + abs(final_state.location[0][1] - final_state.map[bridge_index[1]])
        if distance <= 10 and final_state.isSplit:
            internal_weight = 3
        else:
            internal_weight = 0.5
        return (self.magic_table_max - distance + bad_score) ** 2 * goal_distance_weight \
            + special_score \
            + (self.magic_table_max - internal_distance) ** 2 * internal_weight \
            + len(individual.chromosome) * explore_weight \
            + (self.magic_table_max - bridge_distance) ** 2 * bridge_weight

    def initialize_population(self, num_ind, anphabet, population):
        for i in range(num_ind):
            chromosome = []
            len_chromo = random.randint(self.len_chromosome_min, self.len_chromosome_max)
            for j in range(len_chromo):
                chromosome.append(random.choice(anphabet))
            population.individual_array.append(self.Individual(chromosome))
        population.size = num_ind

    def roulette_wheel_selection(self, population):
        r = random.random()
        p_sum = 0
        result = None
        for ind in population:
            if ind.select_for_parent:
                continue
            p_sum += (ind.fitness_value / population.sum_fitness)
            if r < p_sum:
                result = ind
                ind.select_for_parent = True
                population.sum_fitness -= ind.fitness_value
                break
        return result

    def rank_selection(self, population, num_ind):
        initial_size = population.size
        population.individual_array.sort(reverse=True)
        for i in range(num_ind, initial_size):
            population.sum_fitness -= population[i].fitness_value
        population.size = num_ind
        population.individual_array = population.individual_array[0:num_ind]
        population.best_individual = population.individual_array[0]
        return population

    def reproduce(self, old_population, x_para):
        selected_individuals = self.Population()
        for i in range(int(x_para * self.population_size)):
            ind = self.roulette_wheel_selection(old_population)
            selected_individuals.individual_array.append(ind)
            selected_individuals.size += 1
            selected_individuals.sum_fitness += ind.fitness_value
        return selected_individuals

    def cross_over(self, parents_set):
        offspring = []
        random.shuffle(parents_set.individual_array)
        for j in range(int(parents_set.size / 2)):
            parent_1 = parents_set[j * 2]
            parent_2 = parents_set[j * 2 + 1]
            offspring += self.best_position_cross(parent_1, parent_2)
        return offspring

    def mutation(self, offspring_list, y_para):
        random.shuffle(offspring_list)
        for i in range(0, int(len(offspring_list) * y_para)):
            len_chromo = len(offspring_list[i].chromosome)
            if len_chromo == 0:
                return
            if offspring_list[i].best_position + 1 > len_chromo - 1:
                r = random.randint(0, len_chromo - 1)
            else:
                r = random.randint(offspring_list[i].best_position + 1, len_chromo - 1)
            pre_char = offspring_list[i].chromosome[r]
            while pre_char == offspring_list[i].chromosome[r]:
                offspring_list[i].chromosome[r] = random.choice(self.alphabet)
            r = random.randint(1, 20)
            for j in range(r):
                offspring_list[j].chromosome.append(random.choice(self.alphabet))

    def compute_fitness(self, population):
        sum_fitness = 0
        max_fit_ind = -1
        count = 0
        for ind in population:
            count += 1
            ind.select_for_parent = False
            if ind.fitness_value == -1:
                ind.fitness_value = self.fitness_function(ind)
            sum_fitness += ind.fitness_value
            if max_fit_ind < ind.fitness_value:
                max_fit_ind = ind.fitness_value
                population.best_individual = ind
        population.sum_fitness = sum_fitness
        population.size = count

    def best_position_cross(self, individual_a, individual_b):
        offspring1 = self.Individual([])
        offspring2 = self.Individual([])
        cross_point_1 = individual_a.best_position
        cross_point_2 = individual_b.best_position
        if len(individual_a.chromosome) - 1 == individual_a.best_position:
            cross_point_1 = random.randint(0, len(individual_a.chromosome) // 2)
        if len(individual_b.chromosome) - 1 == individual_b.best_position:
            cross_point_2 = random.randint(0, len(individual_b.chromosome) // 2)
        offspring1.chromosome = individual_a[0:cross_point_1 + 1] + individual_b[cross_point_2 + 1:]
        offspring2.chromosome = individual_b[0:cross_point_2 + 1] + individual_a[cross_point_1 + 1:]
        offspring1.best_position = cross_point_1
        offspring2.best_position = cross_point_2
        return [offspring1, offspring2]

    def check_goal(self, population):
        if population.best_individual.fitness_value == self.goal_score:
            return population.best_individual
        else:
            return None

    def refine_result(self, individual):
        cur_state = State(location=self.game.indexBlock, map=self.game.initial, locationSwitch=self.game.locationSwitch)
        list_state = [cur_state]
        for ch in individual.chromosome:
            id_cube = int('a' <= ch <= 'z') + 1
            next_state = None
            if ch in ['R', 'r']:
                next_state = cur_state.moveRight(id_cube)
            elif ch in ['L', 'l']:
                next_state = cur_state.moveLeft(id_cube)
            elif ch in ['u', 'U']:
                next_state = cur_state.moveUp(id_cube)
            elif ch in ['d', 'D']:
                next_state = cur_state.moveDown(id_cube)
            if next_state is not None:
                cur_state = next_state
                list_state.append(cur_state)
        print(individual.chromosome)
        return list_state

    def solve(self):
        num_gen = 0
        pre_population = self.Population()
        self.initialize_population(self.population_size, self.alphabet, pre_population)
        self.compute_fitness(pre_population)
        check_end = self.check_goal(pre_population)
        while check_end is None:
            parents_pool = self.reproduce(pre_population, self.x_para)
            offspring_list = self.cross_over(parents_pool)
            self.mutation(offspring_list, self.y_para)
            pre_population.add(offspring_list)
            self.compute_fitness(pre_population)
            cur_population = self.rank_selection(pre_population, self.population_size)
            check_end = self.check_goal(cur_population)
            pre_population = cur_population
            num_gen += 1
            print("Num gen: " + str(num_gen))
            print(cur_population.best_individual.fitness_value)
        return self.refine_result(check_end)
