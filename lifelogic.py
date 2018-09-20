from event import Event


class Cell:

    def __init__(self, alive=0):
        self.was_alive: int = alive
        self.is_alive: int = alive
        self.i: int = None
        self.j: int = None
        self.neighbours: [Cell] = []
        self.born_event = Event()
        self.died_event = Event()

    def switch(self) -> None:
        if self.is_alive == 0:
            self.born()
        else:
            self.die()

    def update(self) -> None:
        a = sum(n.was_alive for n in self.neighbours)
        if self.was_alive and not 2 <= a <= 3:
            self.is_alive = 0
            self.died_event.fire(self)
        elif a == 3:
            self.is_alive = 1
            self.born_event.fire(self)

    def update_ended(self) -> None:
        self.was_alive = self.is_alive

    def die(self) -> None:
        self.is_alive = 0
        self.was_alive = 0
        self.died_event.fire(self)

    def born(self) -> None:
        self.is_alive = 1
        self.was_alive = 1
        self.born_event.fire(self)


class Life:

    def __init__(self, nrow: int, ncolumn: int):
        self.row_count: int = nrow
        self.column_count: int = ncolumn
        self.is_running: bool = False
        self.cells: [[Cell]] = [[Cell() for x in range(ncolumn)] for y in range(nrow)]
        self.build_neighbourhoods()

    def build_neighbourhoods(self) -> None:
        for i in range(self.row_count):
            for j in range(self.column_count):
                self.cells[i][j].j = j
                self.cells[i][j].i = i
                u = (i - 1) % self.row_count
                d = (i + 1) % self.row_count
                r = (j + 1) % self.column_count
                l = (j - 1) % self.column_count
                self.cells[i][j].neighbours.append(self.cells[u][j])
                self.cells[i][j].neighbours.append(self.cells[d][j])
                self.cells[i][j].neighbours.append(self.cells[i][r])
                self.cells[i][j].neighbours.append(self.cells[i][l])
                self.cells[i][j].neighbours.append(self.cells[u][r])
                self.cells[i][j].neighbours.append(self.cells[u][l])
                self.cells[i][j].neighbours.append(self.cells[d][r])
                self.cells[i][j].neighbours.append(self.cells[d][l])

    def for_all_cells(self, func) -> None:
        # to call a method on every cell without a parameter
        for row in self.cells:
            for c in row:
                func(c)

    def are_cells_consistent(self) -> bool:
        for row in self.cells:
            for c in row:
                if c.is_alive != c.was_alive:
                    return False
        return True

    def update(self) -> bool:
        self.for_all_cells(Cell.update)
        updated = not self.are_cells_consistent()
        self.for_all_cells(Cell.update_ended)
        return updated

    def clear(self):
        for row in self.cells:
            for c in row:
                c.die()

    def load(self, file_path: str) -> bool:
        f = open(file_path, 'r')
        line_array: [str] = f.read().split('\n')
        if not self.is_loadable(line_array):
            return False
        for i in range(self.row_count):
            for j in range(self.column_count):
                self.cells[i][j].is_alive = self.cells[i][j].was_alive = int(line_array[i][j])
        return True

    def is_loadable(self, line_array: [str]) -> bool:
        if len(line_array) != self.row_count:
            return False
        for line in line_array:
            if len(line) != self.column_count:
                return False
            for character in line:
                if character not in ['0', '1']:
                    return False
        return True

    def save(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            for i in range(self.row_count):
                for j in range(self.column_count):
                    f.write(str(self.cells[i][j].is_alive))
                if i < self.row_count - 1:
                    f.write('\n')
