from snake.gen import Dicrections
from snake.gen import position
from snake.solving.base import BaseSolver
from snake.solving.path import PathSolver


class GreedySolver(BaseSolver):

    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc(self):
        s_copy, m_copy = self.snake.copy()

        self._path_solver.snake = self.snake
        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]

            self._path_solver.snake = s_copy
            path_to_tail = self._path_solver.longest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        head = self.snake.head()
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = position.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)
        return direc
