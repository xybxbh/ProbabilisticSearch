import random
from Cell import *


class Landscape(object):
    def __init__(self):
        self.dim = 50
        self.env = self.gen_landscape(0.2, 0.3, 0.3, 0.2)
        target_x = random.randint(0, self.dim - 1)
        target_y = random.randint(0, self.dim - 1)
        self.target_index = (target_x, target_y)
        self.env[target_x][target_y].set_target()
        
    def gen_landscape(self, p_flat, p_hilly, p_forest, p_cave):
        landscape = [['0' for col in range(self.dim)] for row in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                p = random.random()
                if p < p_flat:
                    landscape[i][j] = Cell('flat')
                elif p < p_flat + p_hilly:
                    landscape[i][j] = Cell('hilly')
                elif p < p_flat + p_hilly + p_forest:
                    landscape[i][j] = Cell('forest')
                elif p < p_flat + p_hilly + p_forest + p_cave:
                    landscape[i][j] = Cell('cave')
        return landscape

    def get_cell_with_highest_belief(self):
        current_belief = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_belief.append(self.env[i][j].belief[-1])
        index = current_belief.index(max(current_belief))
        return (index // self.dim, index % self.dim)

    def get_cell_with_highest_p_of_finding(self):
        current_pfind = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_pfind.append(self.env[i][j].belief[-1]*(1-self.env[i][j].fn))
        index = current_pfind.index(max(current_pfind))
        return (index // self.dim, index % self.dim)

