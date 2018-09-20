import unittest
from lifelogic import *


class LifeLogicTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LifeLogicTest, self).__init__(*args, **kwargs)
        # the following assignments depend on each other
        self.required_width = 5
        self.required_height = 5
        self.alivecells = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 2)]
        self.aliveafterstep = [(0, 2), (1, 2), (1, 3), (2, 1), (2, 3)]
        self.updated = True

    def setUp(self):
        self.life = Life(self.required_height, self.required_width)

    def tearDown(self):
        del self.life

    def give_cells_birth(self):
        for t in self.alivecells:
            self.life.cells[t[0]][t[1]].born()

    def test_number_of_cells(self):
        self.assertEqual(len(self.life.cells), self.required_height)
        for row in self.life.cells:
            self.assertEqual(len(row), self.required_width)

    def test_cells_are_dead(self):
        for row in self.life.cells:
            for c in row:
                assert c.is_alive == c.was_alive == 0

    def test_cells_state(self):
        self.give_cells_birth()
        for i in range(len(self.life.cells)):
            for j in range(len(self.life.cells[i])):
                c = self.life.cells[i][j]
                expected = 0
                if (i, j) in self.alivecells:
                    expected = 1
                    assert c.is_alive == c.was_alive == expected

    def test_cells_neighbourhood(self):
        c = self.life.cells
        avd = (0, 1, self.life.row_count - 1)  # allowed vertical distance
        ahd = (0, 1, self.life.column_count - 1)  # allowed horizontal distance
        forbidden = (0, 0)
        for i in range(len(c)):
            for j in range(len(c[i])):
                for k in range(len(c)):
                    for l in range(len(c[k])):
                        vd = abs(i - k)  # vertical distance
                        hd = abs(j - l)  # horizontal distance
                        if vd in avd and hd in ahd and (vd, hd) != forbidden:
                            assert c[k][l] in c[i][j].neighbours
                        else:
                            assert c[k][l] not in c[i][j].neighbours

    def test_clear_cells(self):
        self.give_cells_birth()
        self.life.clear()
        for row in self.life.cells:
            for c in row:
                assert c.is_alive == c.was_alive == 0

    def test_cells_after_step(self):
        self.give_cells_birth()
        assert self.life.update() == self.updated
        for i in range(len(self.life.cells)):
            for j in range(len(self.life.cells[i])):
                c = self.life.cells[i][j]
                expected = 0
                if (i, j) in self.aliveafterstep:
                    expected = 1
                assert c.is_alive == c.was_alive == expected


unittest.main()
