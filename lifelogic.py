from src.event import Event

class Cell:

    def __init__(self, alive = 0):
        self.wasalive = self.isalive = alive
        self.neighbours = []
        self.bornevent = Event()
        self.diedevent = Event()

    def switch(self):
        if self.isalive == 0:
            self.isalive = self.wasalive = 1
            self.bornevent.fire(self)
        else:
            self.isalive = self.wasalive = 0
            self.diedevent.fire(self)

    def update(self):
        a = sum(n.wasalive for n in self.neighbours)
        if self.wasalive and (a < 2 or a > 3):
            self.isalive = 0
            self.diedevent.fire(self)
            return True
        elif a == 3:
            self.isalive = 1
            self.bornevent.fire(self)
            return True
        return False

    def update_ended(self):
        self.wasalive = self.isalive

    def die(self):
        self.isalive = 0
        self.wasalive = 0
        self.diedevent.fire(self)

    def born(self):
        self.wasalive = 0
        self.isalive = 1
        self.bornevent.fire(self)

class Life:
    def __init__(self, nrow, ncolumn):
        self.nrow = nrow
        self.ncolumn = ncolumn
        self.isrunning = False
        self.cells = [[Cell() for x in range(ncolumn)] for y in range(nrow)]
        self.buildconnections()

    def buildconnections(self):
        for i in range(self.nrow):
            for j in range(self.ncolumn):
                self.cells[i][j].j = j
                self.cells[i][j].i = i
                u = (i - 1) % self.nrow
                d = (i + 1) % self.nrow
                r = (j + 1) % self.ncolumn
                l = (j - 1) % self.ncolumn
                self.cells[i][j].neighbours.append(self.cells[u][j])
                self.cells[i][j].neighbours.append(self.cells[d][j])
                self.cells[i][j].neighbours.append(self.cells[i][r])
                self.cells[i][j].neighbours.append(self.cells[i][l])
                self.cells[i][j].neighbours.append(self.cells[u][r])
                self.cells[i][j].neighbours.append(self.cells[u][l])
                self.cells[i][j].neighbours.append(self.cells[d][r])
                self.cells[i][j].neighbours.append(self.cells[d][l])

    def update(self):
        updated = False
        for row in self.cells:
            for c in row:
                if c.update():
                    updated = True
        for row in self.cells:
            for c in row:
                c.update_ended()
        return updated

    def clear(self):
        for row in self.cells:
            for c in row:
                c.die()

    def load(self, filepath):
        if sum(1 for line in open(filepath, 'r')) < self.nrow:
            return False
        with open(filepath, 'r') as f:
            i = 0
            for line in f:
                str = line.__str__()
                if len(str) < self.ncolumn:
                    return False
                for j in range(self.ncolumn):
                    if not (str[j] == '0' or str[j] == '1'):
                        return False
                    self.cells[i][j].isalive = self.cells[i][j].wasalive = int(str[j])
                i = i + 1
                if i == self.nrow:
                    break
        return True

    def save(self, filepath):
        with open(filepath, 'w') as f:
            for row in self.cells:
                for c in row:
                    f.write(str(c.isalive))
                f.write('\n')