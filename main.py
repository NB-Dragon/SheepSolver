import time
from business.SheepSolver import SheepSolver

if __name__ == '__main__':
    sheep_solver = SheepSolver()
    sheep_solver.init_card_data()
    start_time = time.time()
    sheep_solver.solve()
    end_time = time.time()
    sheep_solver.print_result()
    print("计算用时: {}".format(end_time - start_time))
