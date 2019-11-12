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
                            self.landscape.env[i][j].update_belief(1/(1-cell.belief[-1]*(1-cell.fn)))
                cell.update_belief(cell.fn/(cell.belief[-1]*cell.fn+1-cell.belief[-1]))
                count += 1

    def base_one_step_search(self, rule):
        motion_count = 0
        search_count = 0
        (x, y) = (0, 0)
        while True:
            if rule == 1:
                (next_x, next_y) = self.landscape.get_cell_with_highest_belief()
            else:
                (next_x, next_y) = self.landscape.get_cell_with_highest_p_of_finding()
            search_count += 1
            motion_count += abs(next_x - x) + abs(next_y - y)
            action_count = search_count + motion_count
            cell = self.landscape.env[next_x][next_y]
            (x, y) = (next_x, next_y)
            if cell.search_cell():
                return (next_x, next_y), action_count, motion_count, search_count # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == next_x and j == next_y:
                            pass    # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1/(1-cell.belief[-1]*(1-cell.fn)))
                cell.update_belief(cell.fn/(cell.belief[-1]*cell.fn+1-cell.belief[-1]))

    def one_step_search(self, rule):
        motion_count = 0
        search_count = 0
        if rule == 1:
            (x, y) = (0, 0)
        else:
            (x, y) = self.landscape.get_random_flat()
        while True:
            if rule == 1:
                (next_x, next_y) = self.landscape.get_cell_with_highest_belief_dist_factor((x, y), 0)
            else:
                (next_x, next_y) = self.landscape.get_cell_with_highest_p_of_finding_dist_factor((x, y), 0)
            cell = self.landscape.env[next_x][next_y]
            search_count += 1
            motion_count += abs(next_x - x) + abs(next_y - y)
            action_count = motion_count + search_count
            (x, y) = (next_x, next_y)
            if cell.search_cell():
                return (next_x, next_y), action_count, motion_count, search_count # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == next_x and j == next_y:
                            pass    # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1/(1-cell.belief[-1]*(1-cell.fn)))
                cell.update_belief(cell.fn/(cell.belief[-1]*cell.fn+1-cell.belief[-1]))

    def search_moving_target(self, rule):
        count = 0
        while True:
            if rule == 1:
                (x, y) = self.landscape.get_cell_with_highest_belief_moving_target()
            if rule == 2:
                (x, y) = self.landscape.get_cell_with_highest_p_of_finding_moving_target()
            cell = self.landscape.env[x][y]
            if cell.search_cell():
                count += 1
                return (x, y), count  # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass  # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1 / (1 - cell.belief[-1] * (1 - cell.fn)))
                cell.update_belief(cell.fn / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
                count += 1
                self.landscape.target_move()

    def search_moving_target_re(self, rule):
        count = 0
        while True:
            temp_belief = [[self.landscape.env[i][j].belief[-1] for j in range(self.landscape.dim)] for i in range(self.landscape.dim)]
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type != self.landscape.tracker_history:
                        valid_neighbor = []
                        if i - 1 >= 0:
                            valid_neighbor.append((i - 1, j))
                        if i + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i + 1, j))
                        if j - 1 >= 0:
                            valid_neighbor.append((i, j - 1))
                        if j + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i, j + 1))
                        for k in range(len(valid_neighbor)):
                            (valid_i, valid_j) = valid_neighbor[k]
                            self.landscape.env[valid_i][valid_j].belief[-1] += temp_belief[i][j] / len(valid_neighbor) # no append
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type == self.landscape.tracker:
                        self.landscape.env[i][j].belief[-1] = 0
            self.landscape.normalize()
            if rule == 1:
                (x, y) = self.landscape.get_cell_with_highest_belief()
            if rule == 2:
                (x, y) = self.landscape.get_cell_with_highest_p_of_finding()
            cell = self.landscape.env[x][y]
            if cell.search_cell():
                count += 1
                return (x, y), count  # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass  # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1 / (1 - cell.belief[-1] * (1 - cell.fn)))
                cell.update_belief(cell.fn / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
                count += 1
                self.landscape.target_move()

    def search_moving_target_onestep_base(self, rule):
        motion_count = 0
        search_count = 0
        (cur_x, cur_y) = (0, 0)
        while True:
            temp_belief = [[self.landscape.env[i][j].belief[-1] for j in range(self.landscape.dim)] for i in range(self.landscape.dim)]
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type != self.landscape.tracker_history:
                        valid_neighbor = []
                        if i - 1 >= 0:
                            valid_neighbor.append((i - 1, j))
                        if i + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i + 1, j))
                        if j - 1 >= 0:
                            valid_neighbor.append((i, j - 1))
                        if j + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i, j + 1))
                        for k in range(len(valid_neighbor)):
                            (valid_i, valid_j) = valid_neighbor[k]
                            self.landscape.env[valid_i][valid_j].belief[-1] += temp_belief[i][j] / len(valid_neighbor) # no append
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type == self.landscape.tracker:
                        self.landscape.env[i][j].belief[-1] = 0
            self.landscape.normalize()
            if rule == 1:
                (x, y) = self.landscape.get_cell_with_highest_belief()
            if rule == 2:
                (x, y) = self.landscape.get_cell_with_highest_p_of_finding()
            cell = self.landscape.env[x][y]
            search_count += 1
            motion_count += abs(x - cur_x) + abs(y - cur_y)
            action_count = motion_count + search_count
            if cell.search_cell():
                return (x, y), action_count, motion_count, search_count  # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass  # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1 / (1 - cell.belief[-1] * (1 - cell.fn)))
                cell.update_belief(cell.fn / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
                count += 1
                self.landscape.target_move()

    def search_moving_target_onestep(self, rule):
        motion_count = 0
        search_count = 0
        if rule == 1:
            (cur_x, cur_y) = (0, 0)
        else:
            (cur_x, cur_y) = self.landscape.get_random_flat()
        while True:
            temp_belief = [[self.landscape.env[i][j].belief[-1] for j in range(self.landscape.dim)] for i in range(self.landscape.dim)]
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type != self.landscape.tracker_history:
                        valid_neighbor = []
                        if i - 1 >= 0:
                            valid_neighbor.append((i - 1, j))
                        if i + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i + 1, j))
                        if j - 1 >= 0:
                            valid_neighbor.append((i, j - 1))
                        if j + 1 <= self.landscape.dim - 1:
                            valid_neighbor.append((i, j + 1))
                        for k in range(len(valid_neighbor)):
                            (valid_i, valid_j) = valid_neighbor[k]
                            self.landscape.env[valid_i][valid_j].belief[-1] += temp_belief[i][j] / len(valid_neighbor) # no append
            for i in range(self.landscape.dim):
                for j in range(self.landscape.dim):
                    if self.landscape.env[i][j].type == self.landscape.tracker:
                        self.landscape.env[i][j].belief[-1] = 0
            self.landscape.normalize()
            if rule == 1:
                (x, y) = self.landscape.get_cell_with_highest_belief_dist_factor((cur_x, cur_y), 0)
            if rule == 2:
                (x, y) = self.landscape.get_cell_with_highest_p_of_finding_dist_factor((cur_x, cur_y), 0)
            cell = self.landscape.env[x][y]
            search_count += 1
            motion_count += abs(x - cur_x) + abs(y - cur_y)
            action_count = motion_count + search_count
            (cur_x, cur_y) = (x, y)
            if cell.search_cell():
                return (x, y), action_count, motion_count, search_count  # ending condition
            else:
                for i in range(self.landscape.dim):
                    for j in range(self.landscape.dim):
                        if i == x and j == y:
                            pass  # update (x, y) at last
                        else:
                            self.landscape.env[i][j].update_belief(1 / (1 - cell.belief[-1] * (1 - cell.fn)))
                cell.update_belief(cell.fn / (cell.belief[-1] * cell.fn + 1 - cell.belief[-1]))
                count += 1
                self.landscape.target_move()


if __name__ == '__main__':
    total_rule1_count = total_rule2_count = 0
    total_rule1_count_base = total_rule2_count_base = 0
    for i in range(100):
        landscape = Landscape()
        bs = BayesianSearch(landscape)

        # (x, y), rule1_count = bs.search(1)
        (x, y), rule1_action_count, rule1_motion_count, rule1_search_count= bs.one_step_search(1)
        print("rule1:", rule1_action_count)
        total_rule1_count += rule1_action_count

        for i in range(landscape.dim):
            for j in range(landscape.dim):
                landscape.env[i][j].reset_belief()

        # (x, y), rule2_count = bs.search(2)
        (x, y), rule2_action_count, rule2_motion_count, rule2_search_count= bs.one_step_search(2)
        total_rule2_count += rule2_action_count
        print("rule2:", rule2_action_count)

        for i in range(landscape.dim):
            for j in range(landscape.dim):
                landscape.env[i][j].reset_belief()

        (x, y), rule1_action_count_base, rule1_motion_count_base, rule1_search_count_base = bs.base_one_step_search(1)
        total_rule1_count_base += rule1_action_count_base
        print("base_rule1:", rule1_action_count_base)

        for i in range(landscape.dim):
            for j in range(landscape.dim):
                landscape.env[i][j].reset_belief()

        (x, y), rule2_action_count_base, rule2_motion_count_base, rule2_search_count_base = bs.base_one_step_search(2)
        total_rule2_count_base += rule2_action_count_base
        print("base_rule2:", rule2_action_count_base)
    print("aver1:", total_rule1_count/100)
    print("aver2:", total_rule2_count/100)
    print("base_aver1:", total_rule1_count_base/100)
    print("base_aver2:", total_rule2_count_base/100)
