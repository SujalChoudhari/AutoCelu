import numpy as np
import random
import pygame
import math


class CellType:
    EMPTY = 0
    GREENS = 1
    REDS = 2


class Cell:
    MAX_HEALTH = 255
    health: int = MAX_HEALTH
    cell_state: int = CellType.EMPTY

    _same_touching = 0
    _opponent_touching = 0
    _average_env_health = 0

    GRID: list
    i: int = 0
    j: int = 0

    def __init__(self):
        pass

    def _update_touching(self):
        self._same_touching = 0
        self._opponent_touching = 0
        temp_sum_health = 0
        offsets = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        for x_offset, y_offset in offsets:
            if x_offset == 0 and y_offset == 0:
                continue
            new_i = (self.i + x_offset) % len(self.GRID)
            new_j = (self.j + y_offset) % len(self.GRID[0])
            neighbor_cell = self.GRID[new_i][new_j]
            temp_sum_health += neighbor_cell.health
            if neighbor_cell.cell_state == self.cell_state:
                self._same_touching += 1
            elif (
                neighbor_cell.cell_state != self.cell_state
                and neighbor_cell.cell_state != CellType.EMPTY
            ):
                self._opponent_touching += 1
        self._average_env_health = min(int(temp_sum_health / 8), 255)

    def _movement(self):
        if np.random.choice([True, False], p=[0.1, 0.9]):
            return
        offsets = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        random.shuffle(offsets)
        for x_offset, y_offset in offsets:
            new_i = (self.i + x_offset) % len(self.GRID)
            new_j = (self.j + y_offset) % len(self.GRID[0])
            neighbor_cell = self.GRID[new_i][new_j]
            if neighbor_cell.cell_state != self.cell_state:
                if neighbor_cell.cell_state != CellType.EMPTY:
                    self.health += 10
                neighbor_cell.make_this_of_type(self.cell_state)
                neighbor_cell.health = self.health
                self.make_this_of_type(CellType.EMPTY)
                self.i = new_i
                self.j = new_j
                return

    def _reproduce(self):
        if self._can_reproduce():
            offsets = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
            random.shuffle(offsets)

            for x_offset, y_offset in offsets:
                new_i = (self.i + x_offset) % len(self.GRID)
                new_j = (self.j + y_offset) % len(self.GRID[0])
                neighbor_cell = self.GRID[new_i][new_j]
                if neighbor_cell.cell_state != self.cell_state:
                    if neighbor_cell.cell_state != CellType.EMPTY:
                        self.health += 10
                    neighbor_cell.make_this_of_type(self.cell_state)
                    neighbor_cell.health
                    self.health -= 5  # Deduct health for reproduction cost
                    return True
            return False

    def _die(self):
        if self._can_die():
            temp_health = self.health
            self.make_this_of_type(CellType.EMPTY)
            self.health = temp_health

    def tick(self, GRID, i, j):
        if self.cell_state == CellType.EMPTY:
            return
        self.GRID = GRID
        self.i = i
        self.j = j

        self._update_touching()
        self.health -= self._same_touching - self._opponent_touching
        self._die()
        if self._reproduce():
            self._movement()

    def _can_reproduce(self):
        return (
            (self.health > 200 or self._average_env_health > 100)
            and np.random.choice([True, False], p=[0.4, 0.6])
        ) or self._same_touching == 0

    def _can_die(self):
        return self.health < 50

    def make_this_of_type(self, type: CellType):
        self.health = Cell.MAX_HEALTH
        self.cell_state = type

    def draw(self, screen, x, y, CELL_SIZE):
        intensity = max(0, min(self.health, 255))
        color = (
            intensity,
            intensity,
            intensity,
        )  # Default color for an empty cell
        if self.cell_state == CellType.GREENS:
            color = (0, intensity, 0)  # Green for alive cells
        elif self.cell_state == CellType.REDS:
            color = (intensity, 0, 0)  # Red for dead cells

        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
