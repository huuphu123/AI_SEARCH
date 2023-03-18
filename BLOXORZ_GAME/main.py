from UI import UI
from dfs import Bloxorz
from ga import GASolver
import time, sys


def main():
    if len(sys.argv) < 3:
        print()
        print("Please input 2 parameter ( tescase and algrithm) to run!")
        return
    list_state = None
    m = Bloxorz('testcase/stage' + sys.argv[1] + '.txt')
    start2 = time.time()
    if sys.argv[2] == 'DFS':
        result_state = m.DFS()
        end2 = time.time()
        m.print_result(result_state)
        list_state = m.listState
    if sys.argv[2] == 'GA':
        ga = GASolver(m)
        list_state = ga.solve()
        end2 = time.time()   
    print("Searching time: ", str(end2 - start2))
    UI(m.initial, list_state).run()


if __name__ == '__main__':
    main()
