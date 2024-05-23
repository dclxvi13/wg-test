import heapq
import random
from dataclasses import dataclass, field
from enum import Enum


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


@dataclass(order=True)
class PriorityQueueNode:
    priority: int
    point: Point = field(compare=False)


class CellType(Enum):
    WATER = "W"
    LAND = "L"


def generate_map(width: int, height: int, land_ratio: float = 0.3) -> list[list[CellType]]:
    total_cells = width * height
    land_cells = int(total_cells * land_ratio)

    map_grid = [[CellType.WATER for _ in range(width)] for _ in range(height)]

    start_x, start_y = random.randint(0, M - 1), random.randint(0, N - 1)
    queue = [(start_x, start_y)]
    map_grid[start_x][start_y] = CellType.LAND
    land_cells -= 1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while land_cells > 0:
        x, y = queue.pop()
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # the island must be surrounded by water,
            # so we make sure that we do not run into the border of the map
            if 1 <= nx < M - 1 and 1 <= ny < N - 1 and map_grid[nx][ny] == CellType.WATER:
                map_grid[nx][ny] = CellType.LAND
                queue.append((nx, ny))
                land_cells -= 1

    return map_grid


def print_map(map_grid: list[list[CellType]]):
    for row in map_grid:
        print("".join(map(lambda cell: cell.value, row)))


def is_valid(point: Point, width, height):
    return 0 <= point.x < width and 0 <= point.y < height


def heuristic(start: Point, end: Point):
    return abs(start.x - end.x) + abs(start.y - end.y)


def a_star(map_grid: list[list[CellType]], start: Point, end: Point) -> list[Point]:
    height = len(map_grid)
    width = len(map_grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    open_list: list[PriorityQueueNode] = []
    heapq.heappush(open_list, PriorityQueueNode(0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        current = heapq.heappop(open_list).point

        if current == end:
            return reconstruct_path(came_from, current)

        for dx, dy in directions:
            neighbor = Point(current.x + dx, current.y + dy)

            if is_valid(neighbor, width, height) and map_grid[neighbor.x][neighbor.y] == CellType.WATER:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, PriorityQueueNode(f_score[neighbor], neighbor))

    return []  # Path not found


def reconstruct_path(came_from: dict[Point, Point], current: Point) -> list[Point]:
    total_path = [current]

    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()

    return total_path


M, N = 50, 50  # Size of map
land_ratio = 0.3

generated_map = generate_map(M, N, land_ratio=land_ratio)
print_map(generated_map)

start_point = Point(0, 0)
end_point = Point(M - 1, N - 1)

if (generated_map[start_point.x][start_point.y] != CellType.WATER
        or generated_map[end_point.x][end_point.y] != CellType.WATER):
    print("Start or end point is not water. Adjust the points or regenerate the map.")
else:
    path = a_star(generated_map, start_point, end_point)
    if len(path) > 0:
        print(f"The shortest path from {start_point} to {end_point} is {len(path) - 1} steps.")
        print("Path:", path)
    else:
        print("No path found from start to end.")
