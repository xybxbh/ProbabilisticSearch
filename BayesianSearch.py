from Landscape import *
import math
from decimal import *

class BayesianSearch(object):
    def __init__(self, landscape):
        self.landscape = landscape

    def search(self, rule):
        count = 0
        while True:
            if rule == 1:
                (x, y) = self.landscape.get_cell_with_highest_belief()
            if rule == 2:
                (x, y) = self.landscape.get_cell_with_highest_p_of_finding()
            # print(x, y)
            # print(self.landscape.env[x][y].belief)
            cell = self.landscape.env[x][y]
            if cell.search_cell():
                count += 1
                return (x, y), count   # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass    # update (x, y) at last
                        else:
                            # print((i, j), (x, y))
                            # print(cell.belief)
                            # print(cell.fn)
                            # print(cell.belief[-1]*(1-cell.fn))
                            # print(Decimal(1)-Decimal(cell.belief[-1]*(1-cell.fn)))
                            # print(1/(1-cell.belief[-1]*(1-cell.fn)))
                            self.landscape.env[i][j].update_belief(1/(1-cell.belief[-1]*(1-cell.fn)))
                cell.update_belief(cell.fn/(cell.belief[-1]*cell.fn+1-cell.belief[-1]))
                count += 1

if __name__ == '__main__':
    total_rule1_count = total_rule2_count = 0
    for i in range(100):
        landscape = Landscape()
        bs = BayesianSearch(landscape)

        (x, y), rule1_count = bs.search(1)
        print("rule1:", rule1_count)
        total_rule1_count += rule1_count

        for i in range(landscape.dim):
            for j in range(landscape.dim):
                landscape.env[i][j].reset_belief()
        (x, y), rule2_count = bs.search(2)
        total_rule2_count += rule2_count
        print("rule2:", rule2_count)
    print("aver1:", total_rule1_count/100)
    print("aver2:", total_rule2_count/100)