import random

from Puzzle15.graphs.puzzle15_vertex import Puzzle15Vertex


class Puzzle15Graph:

    @staticmethod
    def get_neighbors(vertex: Puzzle15Vertex):
        return vertex.get_neighbors()

    @staticmethod
    def is_edge(vertex1: Puzzle15Vertex, vertex2: Puzzle15Vertex):
        return vertex1 in vertex2.get_neighbors()

    @staticmethod
    def get_random_start():
        start_state = [i for i in range(16)]

        random.shuffle(start_state)
        while not Puzzle15Graph.is_valid(start_state):
            random.shuffle(start_state)

        return Puzzle15Vertex(start_state)

    @staticmethod
    def is_valid(state: list):
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j] != 0:
                    inversions += 1

        return inversions % 2 == 0

    @staticmethod
    def get_dummy_start():
        dummy_start = [1, 2, 3, 4, 5, 6, 7, 8, 0, 10, 11, 12, 13, 14, 9, 15]
        return Puzzle15Vertex(dummy_start)

    @staticmethod
    def get_end():
        end_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        return Puzzle15Vertex(end_state)
