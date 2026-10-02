def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    from collections import deque

    if not maze or not maze[0]:
        return {"distance": -1, "path": []}

    rows = len(maze)
    cols = len(maze[0])

    conveyor_dirs = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }

    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if start is None or end is None:
        return {"distance": -1, "path": []}

    if start == end:
        return {"distance": 0, "path": [[start[0], start[1]]]}

    conveyor_memo = {}

    def simulate_conveyor(sr: int, sc: int):
        if (sr, sc) in conveyor_memo:
            return conveyor_memo[(sr, sc)]

        slide_path = [[sr, sc]]
        visited_conveyor = {(sr, sc)}
        curr_r, curr_c = sr, sc

        while maze[curr_r][curr_c] in conveyor_dirs:
            dr, dc = conveyor_dirs[maze[curr_r][curr_c]]
            nr, nc = curr_r + dr, curr_c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                conveyor_memo[(sr, sc)] = (False, None, [])
                return False, None, []

            if maze[nr][nc] == '#':
                conveyor_memo[(sr, sc)] = (False, None, [])
                return False, None, []

            if (nr, nc) in visited_conveyor:
                conveyor_memo[(sr, sc)] = (False, None, [])
                return False, None, []

            curr_r, curr_c = nr, nc
            slide_path.append([curr_r, curr_c])
            if maze[curr_r][curr_c] in conveyor_dirs:
                visited_conveyor.add((curr_r, curr_c))

        res = (True, (curr_r, curr_c), slide_path)
        conveyor_memo[(sr, sc)] = res
        return res

    queue = deque([start])
    visited = {start}
    dist = {start: 0}
    parent = {}

    found = False
    while queue:
        curr = queue.popleft()
        if curr == end:
            found = True
            break

        r, c = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            cell_val = maze[nr][nc]
            if cell_val == '#':
                continue

            if cell_val in conveyor_dirs:
                valid, landing, segment = simulate_conveyor(nr, nc)
                if not valid:
                    continue
                next_cell = landing
                path_segment = segment
            else:
                next_cell = (nr, nc)
                path_segment = [[nr, nc]]

            if next_cell not in visited:
                visited.add(next_cell)
                dist[next_cell] = dist[curr] + 1
                parent[next_cell] = (curr, path_segment)
                queue.append(next_cell)

    if not found:
        return {"distance": -1, "path": []}

    curr = end
    segments = []
    while curr != start:
        prev_cell, segment = parent[curr]
        segments.append(segment)
        curr = prev_cell

    full_path = [[start[0], start[1]]]
    for seg in reversed(segments):
        full_path.extend(seg)

    return {
        "distance": dist[end],
        "path": full_path
    }


if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}

    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}