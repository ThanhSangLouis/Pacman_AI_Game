from Algorithms.AStar import AStar
from Algorithms.AlphaBetaPruning import AlphaBetaAgent
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.Backtracking import Backtracking
from Algorithms.LocalSearch import local_search
from Algorithms.Minimax import minimaxAgent
from Algorithms.HillClimbing import hill_simple, hill_steepest, hill_random
from Algorithms.Greedy import Greedy
from Algorithms.BeamSearch import BeamSearch
from Algorithms.UCS import UCS
from Algorithms.IDASearch import IDAStar
from Algorithms.AlphaBetaPruning import AlphaBetaAgent as AlphaBetaPruning
from Algorithms.ReflexAgentWithAStar import ReflexAgentWithAStarWrapper
from Algorithms.SimulatedAnnealing import SimulatedAnnealingForPacMan, calc_heuristic

class SearchAgent:
    def __init__(self, _map, _food_Position, start_row, start_col, N, M):
        self.map = _map.copy()
        self.food_Position = _food_Position.copy()
        self.start_row = start_row
        self.start_col = start_col
        self.N = N
        self.M = M
        self.visited = [[0 for _ in range(M)] for _ in range(N)]
        self.prev_pos = None
        self.T = 1000
        self.stuck_counter = 0
        self.heuristic_map = calc_heuristic(self.map, self.N, self.M)  # ⭐⭐ Tính heuristic 1 lần duy nhất



    def execute(self, ALGORITHMS, visited=None, depth=4, Score=0):
        if ALGORITHMS == "BFS":
            return BFS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "DFS":
            return DFS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "A*":
            return AStar(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Local Search":
            return local_search(self.map, self.start_row, self.start_col, self.N, self.M, visited.copy())
        if ALGORITHMS == "Minimax":
            return minimaxAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
        if ALGORITHMS == "AlphaBetaPruning":
            return AlphaBetaAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
        if ALGORITHMS == "AlphaBeta":
            return AlphaBetaPruning(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Backtracking":
            return Backtracking(self.map, (self.start_row, self.start_col), self.N, self.M)
        if ALGORITHMS == "Hill Simple":
            return hill_simple(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Hill Steepest":
            return hill_steepest(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Hill Random":
            return hill_random(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Greedy":
            return Greedy(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Beam Search":
            return BeamSearch(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "UCS":
            return UCS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "IDA*":
            return IDAStar(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "ReflexAgentWithAStar":
            return ReflexAgentWithAStarWrapper(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "SimulatedAnnealing":
            move, self.prev_pos, self.T, self.stuck_counter = SimulatedAnnealingForPacMan(
                self.map, self.start_row, self.start_col, self.N, self.M,
                self.visited, self.heuristic_map, self.prev_pos, self.T, self.stuck_counter
            )
            if move:
                self.start_row = move[0][0]
                self.start_col = move[0][1]
            return move



