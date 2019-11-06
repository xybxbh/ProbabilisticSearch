from Landscape import *


class BayesianSearch(object):
    def __init__(self, landscape):
        self.landscape = landscape

    def search(self):
        while True:
            (x, y) = self.landscape.get_cell_with_highest_belief()
            cell = self.landscape[x][y]
            if cell.search_cell():
                return (x, y)   # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass    # update (x, y) at last
                        else:
                            self.landscape[i][j].update_belief(1 / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
                        cell.update_belief(cell.fn / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
