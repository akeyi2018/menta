import heapq
from datetime import datetime

class RouteSearchAlgorism:

    def heuristic(self, node, goal):
        # マンハッタン距離をヒューリスティック関数として使用
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def astar(self, maze, start, goal):
        rows = len(maze)
        cols = len(maze[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上の順

        # 始点からのコストと最短経路を無限大に初期化
        cost = [[float('inf')] * cols for _ in range(rows)]
        cost[start[0]][start[1]] = 0
        previous = [[None] * cols for _ in range(rows)]

        # 優先度キュー
        pq = [(0 + self.heuristic(start, goal), start)]

        while pq:
            _, node = heapq.heappop(pq)
            if node == goal:
                # ゴールに到達したら最短経路を追跡
                path = []
                while node:
                    path.append(node)
                    node = previous[node[0]][node[1]]
                return cost[goal[0]][goal[1]], path[::-1]  # 逆順なので反転させる

            for dx, dy in directions:
                x, y = node[0] + dx, node[1] + dy
                if 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0:
                    new_cost = cost[node[0]][node[1]] + 1
                    if new_cost < cost[x][y]:
                        cost[x][y] = new_cost
                        previous[x][y] = node
                        heapq.heappush(pq, (new_cost + self.heuristic((x, y), goal), (x, y)))

        return float('inf'), None  # ゴールに到達できない場合

    def print_maze_with_path(self, maze, path):
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if (i, j) == path[0]:
                    print('S', end=' ')  # Start
                elif (i, j) == path[-1]:
                    print('G', end=' ')  # Goal
                elif (i, j) in path:
                    print('*', end=' ')  # Path
                elif maze[i][j] == 1:
                    print('#', end=' ')  # Wall
                else:
                    print('.', end=' ')  # Empty
            print()

    def get_route_path(self, maze, path):
        results = []
        for i in range(len(maze)):
            inner = []
            for j in range(len(maze[0])):
                if (i,j) == path[0]:
                    inner.append(2)
                elif (i,j) == path[-1]:
                    inner.append(3)
                elif (i,j) in path:
                    inner.append(4)
                elif maze[i][j] == 1:
                    inner.append(1)
                else:
                    inner.append(0)
            results.append(inner)
        return results

class Maze:
   
    maze = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

class Main:

    def __init__(self) -> None:
        self.start = (0, 0)
        self.goals = [(13, 6), (11,16), (13,15)]
        
        self.route_search = RouteSearchAlgorism()
        self.maze = Maze()

    def get_results(self):
        # routes = []
        paths = []
        for goal in self.goals:
            shortest_path_length, shortest_path = self.route_search.astar(self.maze.maze, self.start, goal)
            if shortest_path_length != float('inf'):
                # print("最短経路の長さは:", shortest_path_length)
                # print("最短経路は:")
                # self.route_search.print_maze_with_path(self.maze.maze, shortest_path)
                paths.append(shortest_path)

                # res = self.route_search.get_route_path(self.maze.maze, shortest_path)
                # routes.append(res)
            else:
                print("ゴールに到達できませんでした。")
        return paths
    
    def get_move_results(self):
        routes = []


if __name__ == '__main__':
    print('start: ', datetime.now())
    app = Main()
    app.get_results()
    print('end: ', datetime.now())
