import time
import sys
from testcase_generation import *
from solver import *
from UI import UI
from Cups_UI import Cups


def main():
    if len(sys.argv) < 3:
        print()
        print("Please input 2 parameter ( tescase and algrithm) to run!")
        return

    node = None
    m = WaterSortSolver("./testcase/testcase"  + sys.argv[1] + '.txt')

    start2 = time.time()
    if sys.argv[2] == 'DFS':
        node = m.search('DFS')
    if sys.argv[2] == 'BFS':
        node = m.search('BFS')
    if sys.argv[2] == 'A*':
        node = m.search('A_Star')
    end2 = time.time()
    print("Searching time: ", str(end2 - start2))
    
    m.printResult(sys.argv[1])
    if int(sys.argv[1]) <= 9:
        UI(Cups(m.initial, m.num_cups, m.capacity, None, m.path, m.Color)).run()
    else:
        print(f'Open result/result_testcase{sys.argv[1]}.txt to check result')


if __name__ == '__main__':
    main()





