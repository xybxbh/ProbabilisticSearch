import random


class Cell(object):
    def __init__(self, type):
        self.type = type
        self.fn = self.false_negative(0.1, 0.3, 0.7, 0.9)
        self.belief = []
        self.belief.append(1/2500)
        self.target = False

    def false_negative(self, fn_flat, fn_hilly, fn_forest, fn_cave):
        if self.type == 'flat':
            return fn_flat
        if self.type == 'hilly':
            return fn_hilly
        if self.type == 'forest':
            return fn_forest
        if self.type == 'cave':
            return fn_cave

    def update_belief(self, coefficient):
        self.belief.append(self.belief[-1] * coefficient)

    def set_target(self):
        self.target = True

    def search_cell(self):
        if self.target == False:
            return False
        p = random.random()
        if p < self.fn:
            return False
        else:
            return True
