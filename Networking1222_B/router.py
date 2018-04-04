import Dijkstra

class router():
    def __init__(self):
        graph_list = [[0, 7, float('inf'), 3, 3, 2],
                      [7, 0, 5, float('inf'), 1, 2],
                      [float('inf'), 5, 0, 6, float('inf'), 3],
                      [3, float('inf'), 6, 0, float('inf'), 1],
                      [3, 1, float('inf'), float('inf'), 0, float('inf')],
                      [2, 2, 3, 1, float('inf'), 0]]